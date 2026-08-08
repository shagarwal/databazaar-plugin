"""databazaar.io catalog adapter.

The only fully-working adapter in v0.1. Talks to https://api.databazaar.io
anonymously (read-only). Free listings can be fully downloaded; paid listings
return metadata + sample only.
"""
from __future__ import annotations
import json, urllib.request, urllib.parse, csv, io
from datetime import datetime, timezone

API_BASE = "https://api.databazaar.io"


def _get(path: str, **params) -> dict:
    qs = "?" + urllib.parse.urlencode(params) if params else ""
    req = urllib.request.Request(
        f"{API_BASE}{path}{qs}",
        headers={"User-Agent": "databazaar-skill/0.1.0 (+https://databazaar.io)"},
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read())


def _ts() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def can_handle(request: str) -> float:
    """Confidence that databazaar can serve this request."""
    # v0 heuristic: search the catalog and use the top-result's tag overlap.
    try:
        results = _get("/datasets", query=request, limit=5).get("data", [])
    except Exception:
        return 0.0
    if not results:
        return 0.0
    return min(1.0, 0.5 + 0.1 * len(results))  # rough — improve in v1


def fetch(request: str) -> dict:
    """Pick best-matching listing, return rows + schema + provenance."""
    results = _get("/datasets", query=request, limit=10).get("data", [])
    if not results:
        return {
            "rows": [],
            "schema": {"title": request, "description": "No databazaar listing matched.", "columns": []},
            "sources": [],
            "gaps": "No databazaar listing matched the request.",
        }

    pick = results[0]
    listing_id = pick["id"]
    pricing = pick.get("pricing_type", "buy_it_now")
    is_free = (pricing == "free") or (pick.get("price") in (0, "0", None) and pricing != "buy_it_now")
    rows = []

    # For free listings, prefer the full download. Paid → sample only.
    fetch_paths = ["/download-url"] if is_free else ["/sample", "/download-url"]

    for path in fetch_paths:
        try:
            resp = _get(f"/datasets/{listing_id}{path}")
            url = resp.get("download_url") or resp.get("sample_url")
            if not url:
                continue
            with urllib.request.urlopen(url, timeout=120) as r:
                content = r.read().decode("utf-8", errors="replace")
            fmt = pick.get("schema", {}).get("format", "csv")
            if fmt == "json":
                parsed = json.loads(content)
                if isinstance(parsed, dict) and "listings" in parsed:
                    rows = parsed["listings"]
                elif isinstance(parsed, dict) and "data" in parsed:
                    rows = parsed["data"]
                elif isinstance(parsed, list):
                    rows = parsed
            else:
                reader = csv.DictReader(io.StringIO(content))
                rows = list(reader)
            if rows:
                break
        except Exception:
            continue

    # Tag every row with provenance
    retrieved = _ts()
    for r in rows:
        if isinstance(r, dict):
            r["_source"] = f"databazaar:{listing_id}"
            r["_retrieved_at"] = retrieved

    schema = {
        "title": pick.get("title", request),
        "description": pick.get("description", ""),
        "category": pick.get("category", "other"),
        "tags": pick.get("tags", []),
        "columns": pick.get("schema", {}).get("columns", []),
    }
    sources = [{
        "name": f"databazaar.io listing {listing_id}",
        "url": f"https://databazaar.io/datasets/{listing_id}",
        "license": pick.get("license", "see listing"),
        "retrieved_at": retrieved,
    }]
    return {
        "rows": rows,
        "schema": schema,
        "sources": sources,
        "intended_use": "Derived from a databazaar.io listing — see source for original use case.",
    }
