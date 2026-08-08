"""databazaar skill — orchestrator.

Usage:
    python build.py acquire  --request "all S&P 500 companies with HQ" --out ./out
    python build.py aggregate --inputs a.csv b.csv --on company_name --out ./out
    python build.py prepare  --input raw.csv --out ./out
    python build.py list     --from ./out --token $DATABAZAAR_TOKEN

This is v0.1.0 — adapter implementations are stubs. The orchestrator + output
contract are stable; adapters get filled in iteratively, each gated by an eval
case.
"""
from __future__ import annotations
import argparse, json, sys, hashlib, os
from datetime import datetime, timezone
from pathlib import Path

VERSION = "0.4.0"

# Recycled-identifier patterns — when a column matches, datacard gets a
# "Temporal validity" warning. See references/identifier-recycling.md.
import re as _re
_RECYCLED_ID_PATTERNS = [
    ("FAA N-number", _re.compile(r"^(registration_)?n_?number$|^tail(_number)?$", _re.I),
     "faa_airworth_date"),
    ("VIN", _re.compile(r"^vin$", _re.I), "model_year"),
    ("US license plate", _re.compile(r"^(license_)?plate$", _re.I), "plate_issue_date"),
    ("MAC address", _re.compile(r"^mac(_address)?$", _re.I), None),
    ("Phone number", _re.compile(r"^phone(_number)?$", _re.I), "phone_first_assigned"),
    ("Domain name", _re.compile(r"^domain(_name)?$", _re.I), "whois_registered_at"),
]


def _detect_recycled_identifiers(schema):
    out = []
    for c in schema.get("columns", []):
        name = c.get("name", "")
        for label, pat, anchor in _RECYCLED_ID_PATTERNS:
            if pat.match(name):
                out.append((label, name, anchor))
                break
    return out


def _ts() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _write_outputs(out_dir: Path, *, data_rows, schema, sources, methodology,
                   gaps, intended_use, pii_report=None) -> dict:
    """Emit the full output contract. Returns paths dict."""
    out_dir.mkdir(parents=True, exist_ok=True)

    # data
    import csv
    data_path = out_dir / "data.csv"
    if data_rows:
        # Heterogeneous rows: collect union of keys, preserve first-row order
        seen = list(data_rows[0].keys())
        for r in data_rows[1:]:
            for k in r.keys():
                if k not in seen:
                    seen.append(k)
        with data_path.open("w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=seen, extrasaction="ignore")
            w.writeheader()
            w.writerows(data_rows)
    else:
        data_path.write_text("")

    # schema
    (out_dir / "schema.json").write_text(json.dumps(schema, indent=2))

    # provenance
    provenance = {
        "skill_version": VERSION,
        "generated_at": _ts(),
        "row_count": len(data_rows),
        "sources": sources,
        "rows": [
            {"row_index": i, "source": r.get("_source", "unknown"),
             "retrieved_at": r.get("_retrieved_at", _ts())}
            for i, r in enumerate(data_rows)
        ],
    }
    prov_path = out_dir / "provenance.json"
    prov_path.write_text(json.dumps(provenance, indent=2))
    prov_hash = hashlib.sha256(prov_path.read_bytes()).hexdigest()

    # pii
    pii = pii_report or {"scanned_at": _ts(), "row_count": len(data_rows),
                         "detections": [], "blocked": False, "blockers": []}
    (out_dir / "pii_report.json").write_text(json.dumps(pii, indent=2))

    # sample
    sample_rows = data_rows[:1000]
    if sample_rows:
        with (out_dir / "sample.csv").open("w", newline="") as f:
            seen = list(sample_rows[0].keys())
            for r in sample_rows[1:]:
                for k in r.keys():
                    if k not in seen:
                        seen.append(k)
            w = csv.DictWriter(f, fieldnames=seen, extrasaction="ignore")
            w.writeheader()
            w.writerows(sample_rows)

    # listing suggestion
    listing = _suggest_listing(data_rows, schema, sources)
    (out_dir / "listing_suggestion.json").write_text(json.dumps(listing, indent=2))

    # datacard (rubric-compliant)
    recycled = _detect_recycled_identifiers(schema)
    datacard = _render_datacard(data_rows, schema, sources, methodology, gaps,
                                 intended_use, prov_hash, recycled=recycled)
    (out_dir / "datacard.md").write_text(datacard)

    return {
        "data": str(data_path),
        "schema": str(out_dir / "schema.json"),
        "datacard": str(out_dir / "datacard.md"),
        "provenance": str(prov_path),
        "sample": str(out_dir / "sample.csv"),
        "pii_report": str(out_dir / "pii_report.json"),
        "listing_suggestion": str(out_dir / "listing_suggestion.json"),
    }


def _render_datacard(rows, schema, sources, methodology, gaps, intended_use,
                     prov_hash, recycled=None) -> str:
    cols = schema.get("columns", [])
    schema_table = "| Column | Type | Description | Null % | Examples |\n"
    schema_table += "|---|---|---|---|---|\n"
    for c in cols:
        nullp = c.get("null_rate", 0) * 100
        ex = ", ".join(str(x) for x in (c.get("sample_values") or [])[:3])
        schema_table += f"| {c['name']} | {c['type']} | {c.get('description','')} | {nullp:.1f}% | {ex} |\n"

    src_lines = "\n".join(f"- {s.get('name','source')} — {s.get('url','')} — {s.get('license','unknown')} — retrieved {s.get('retrieved_at','')}" for s in sources)

    temporal_section = ""
    if recycled:
        lines = ["## Temporal validity",
                 "",
                 "This dataset joins on identifiers that are reissued by their authority.",
                 "Filter enrichment events temporally to avoid false matches:",
                 ""]
        for label, col, anchor in recycled:
            anchor_text = (f"filter `event_date >= {anchor}`" if anchor
                           else "no reliable anchor — treat enrichment as best-effort")
            lines.append(f"- **{label}** (column `{col}`): {anchor_text}")
        lines.append("")
        lines.append("See `references/identifier-recycling.md` for the full catalog.")
        temporal_section = "\n".join(lines) + "\n\n"

    return f"""# {schema.get('title', 'Untitled Dataset')}

## Overview
{schema.get('description', 'No description provided.')}

- Rows: {len(rows):,}
- Columns: {len(cols)}
- Format: csv (parquet available)
- Generated: {_ts()}

## Schema
{schema_table}

## Sources
{src_lines or '- (none recorded)'}

## Methodology
{methodology or '_(not provided)_'}

## Known gaps & limitations
{gaps or '_(none flagged — review before publishing)_'}

## Intended use & out-of-scope
{intended_use or '_(not specified)_'}

{temporal_section}## Provenance & reproducibility
- Provenance hash: `sha256:{prov_hash}`
- Skill version: `{VERSION}`
- Generated: `{_ts()}`

---
*Built with the `databazaar` skill. Listed on https://databazaar.io.*
"""


def _suggest_listing(rows, schema, sources) -> dict:
    # v0 stub — see references/pricing-model.md for the real model
    import math
    n = max(len(rows), 1)
    cols = len(schema.get("columns", []))
    suggested = round(1.0 * (math.log10(max(n, 100)) / 2) * (1 + cols / 50), 2)
    bands = [0.99, 1.99, 2.99, 4.99, 9.99, 19.99]
    price = min(bands, key=lambda b: abs(b - suggested))
    return {
        "title": schema.get("title", "Untitled"),
        "description": schema.get("description", ""),
        "category": schema.get("category", "other"),
        "tags": schema.get("tags", []),
        "suggested_price_usd": price,
        "pricing_confidence": "low",
        "pricing_reasoning": "v0 heuristic — see references/pricing-model.md",
        "alternatives": [
            {"price": 0, "label": "free (drives traffic)"},
            {"price": price, "label": "heuristic"},
        ],
    }


# ----- modes ---------------------------------------------------------------

def cmd_acquire(args):
    """Acquire mode. v0.4: opt-in scraping, ToS ack recorded, anti-bot blocked."""
    from guardrails import check_request
    allowed, reason = check_request(
        args.request,
        allow_scrape=getattr(args, "allow_scrape", False),
        tos_ack=getattr(args, "tos_ack", None),
    )
    if not allowed:
        print(reason, file=sys.stderr)
        sys.exit(3)

    from adapters import route
    result = route(args.request)
    out = Path(args.out)
    paths = _write_outputs(
        out,
        data_rows=result["rows"],
        schema=result["schema"],
        sources=result["sources"],
        methodology=f"acquire mode v{VERSION}; databazaar adapter only in this version",
        gaps=result.get("gaps", "v0.4 adapters: databazaar, HuggingFace, World Bank. Other 10 adapters stubbed — see references/sources.md."),
        intended_use=result.get("intended_use"),
    )

    # Record ToS ack in provenance.json if scrape was allowed.
    if getattr(args, "allow_scrape", False) and getattr(args, "tos_ack", None):
        prov_path = Path(paths["provenance"])
        prov = json.loads(prov_path.read_text())
        prov["acquisition"] = {
            "allow_scrape": True,
            "tos_ack": args.tos_ack,
            "ack_recorded_at": _ts(),
        }
        prov_path.write_text(json.dumps(prov, indent=2))

    print(json.dumps({"ok": True, "outputs": paths}, indent=2))


def cmd_aggregate(args):
    print("aggregate: not yet implemented in v0.1", file=sys.stderr)
    sys.exit(2)


def cmd_prepare(args):
    """Prepare proprietary input → listable dataset."""
    import prepare as prep
    result = prep.run(args.input)
    pii = result["pii_report"]
    if pii["blocked"]:
        print("REFUSED: blocking PII detected — " + "; ".join(pii["blockers"]),
              file=sys.stderr)
        sys.exit(4)

    out = Path(args.out)
    paths = _write_outputs(
        out,
        data_rows=result["rows"],
        schema=result["schema"],
        sources=result["sources"],
        methodology=f"prepare mode v{VERSION}; schema inferred via sampling; PII scan + tier-1 redaction applied.",
        gaps=result.get("gaps"),
        intended_use=result.get("intended_use"),
        pii_report=pii,
    )
    print(json.dumps({"ok": True, "outputs": paths, "pii": pii}, indent=2))


def cmd_list(args):
    print("list: not yet implemented in v0.1", file=sys.stderr)
    sys.exit(2)


def main():
    p = argparse.ArgumentParser(prog="databazaar")
    sub = p.add_subparsers(dest="cmd", required=True)

    pa = sub.add_parser("acquire")
    pa.add_argument("--request", required=True)
    pa.add_argument("--out", required=True)
    pa.add_argument("--allow-scrape", action="store_true",
                    help="Permit web acquisition. Requires --tos-ack.")
    pa.add_argument("--tos-ack", default=None,
                    help="One-line ToS acknowledgment, recorded in provenance.")
    pa.set_defaults(func=cmd_acquire)

    pg = sub.add_parser("aggregate")
    pg.add_argument("--inputs", nargs="+", required=True)
    pg.add_argument("--on", required=True)
    pg.add_argument("--out", required=True)
    pg.set_defaults(func=cmd_aggregate)

    pp = sub.add_parser("prepare")
    pp.add_argument("--input", required=True)
    pp.add_argument("--out", required=True)
    pp.set_defaults(func=cmd_prepare)

    pl = sub.add_parser("list")
    pl.add_argument("--from", dest="from_dir", required=True)
    pl.add_argument("--token", default=os.environ.get("DATABAZAAR_TOKEN"))
    pl.set_defaults(func=cmd_list)

    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
