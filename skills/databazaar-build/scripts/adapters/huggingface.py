"""HuggingFace Datasets adapter.

Uses the public HF Hub API (no auth needed for public datasets) to:
1. Search for datasets matching the request.
2. Pull dataset card + a small streaming sample.

Live calls; no caching in v0.2. For deterministic eval runs add fixtures
under evals/fixtures/huggingface/.
"""
from __future__ import annotations
import json, urllib.request, urllib.parse
from datetime import datetime, timezone

API = "https://huggingface.co/api"


def _ts() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _get(path: str, **params) -> object:
    qs = "?" + urllib.parse.urlencode(params) if params else ""
    req = urllib.request.Request(
        f"{API}{path}{qs}",
        headers={"User-Agent": "databazaar-skill/0.2.0 (+https://databazaar.io)"},
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read())


def can_handle(request: str) -> float:
    """ML/NLP/text/image dataset signals → high; structured-data signals → low."""
    t = request.lower()
    ml_signals = ["model", "training", "embedding", "nlp", "tokenized", "image",
                  "vision", "speech", "audio", "huggingface", "hf datasets",
                  "instruction", "preference", "rlhf", "benchmark",
                  "question answering", "language model", "sentiment",
                  "translation", "summarization", "classification", "corpus",
                  "qa dataset", "fine-tuning", "fine tuning"]
    structured_signals = ["country", "panel", "indicator", "year", "by state"]
    if any(s in t for s in ml_signals):
        return 0.85
    if any(s in t for s in structured_signals):
        return 0.2
    # Default: try a search and use result count as signal
    try:
        results = _get("/datasets", search=request, limit=5)
        return min(0.6, 0.2 + 0.1 * len(results))
    except Exception:
        return 0.0


def fetch(request: str) -> dict:
    results = []
    queries_tried = [request]
    try:
        results = _get("/datasets", search=request, limit=5)
    except Exception as e:
        return {
            "rows": [],
            "schema": {"title": request, "columns": []},
            "sources": [],
            "gaps": f"HuggingFace search failed: {e}",
        }

    # Fallback: HF's search is keyword-fuzzy; long phrases often miss.
    # Retry with the longest single token.
    if not results:
        tokens = sorted(
            (t for t in request.split() if len(t) > 3),
            key=len, reverse=True,
        )
        for t in tokens[:3]:
            queries_tried.append(t)
            try:
                results = _get("/datasets", search=t, limit=5)
            except Exception:
                continue
            if results:
                break

    if not results:
        return {
            "rows": [],
            "schema": {"title": request, "columns": []},
            "sources": [],
            "gaps": "No HuggingFace dataset matched the request.",
        }

    pick = results[0]
    ds_id = pick.get("id") or pick.get("modelId")
    retrieved = _ts()

    # Surface dataset metadata as a single-row "discovery" record. Streaming
    # actual dataset rows requires the `datasets` library; v0.2 returns
    # metadata + the HF link so users can pull themselves.
    rows = [{
        "dataset_id": ds_id,
        "downloads": pick.get("downloads", 0),
        "likes": pick.get("likes", 0),
        "tags": ", ".join(pick.get("tags", [])),
        "description": pick.get("description", "")[:500],
        "url": f"https://huggingface.co/datasets/{ds_id}",
        "_source": f"huggingface:{ds_id}",
        "_retrieved_at": retrieved,
    }]

    schema = {
        "title": f"HuggingFace dataset discovery — {request}",
        "description": (
            f"Top-{len(results)} HuggingFace datasets matching '{request}'. "
            "v0.2 returns discovery metadata only; use the `datasets` library "
            "to stream actual rows."
        ),
        "category": "ai-ml",
        "tags": pick.get("tags", [])[:10],
        "columns": [
            {"name": "dataset_id", "type": "string", "description": "HuggingFace dataset ID"},
            {"name": "downloads", "type": "number", "description": "30-day download count"},
            {"name": "likes", "type": "number", "description": "Likes on the dataset card"},
            {"name": "tags", "type": "string", "description": "Comma-separated tags"},
            {"name": "description", "type": "string", "description": "Truncated description (500 chars)"},
            {"name": "url", "type": "string", "description": "HuggingFace dataset URL"},
        ],
    }
    sources = [{
        "name": f"HuggingFace dataset {ds_id}",
        "url": f"https://huggingface.co/datasets/{ds_id}",
        "license": pick.get("cardData", {}).get("license", "see card"),
        "retrieved_at": retrieved,
    }]
    return {
        "rows": rows,
        "schema": schema,
        "sources": sources,
        "intended_use": "Discovery output — use as input to a `datasets.load_dataset()` call to pull rows.",
    }
