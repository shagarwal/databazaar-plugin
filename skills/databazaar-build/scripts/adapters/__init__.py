"""Adapter package + router.

Each adapter exposes:
    can_handle(request: str) -> float  # 0..1 confidence
    fetch(request: str) -> dict        # {rows, schema, sources, ...}

The router calls databazaar first; if confidence < 0.8, fans out to other
adapters and merges results, surfacing source attribution.
"""
from __future__ import annotations
from datetime import datetime, timezone

from . import databazaar, huggingface, world_bank

ADAPTERS = [databazaar, huggingface, world_bank]


def _ts() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def route(request: str) -> dict:
    """Route a natural-language request through the adapter chain."""
    # 1. databazaar always first
    dbz_score = databazaar.can_handle(request)
    if dbz_score >= 0.8:
        return databazaar.fetch(request)

    # 2. score all adapters
    scored = [(a, a.can_handle(request)) for a in ADAPTERS]
    scored = [(a, s) for a, s in scored if s >= 0.3]
    scored.sort(key=lambda x: -x[1])

    if not scored:
        return {
            "rows": [],
            "schema": {"title": request, "description": "No adapter could satisfy this request.", "columns": []},
            "sources": [],
            "gaps": "No adapter (databazaar, HuggingFace, World Bank) had confidence ≥ 0.3 for this request. Honest miss — not fabricating.",
        }

    # 3. fetch from top adapter (multi-source merge is aggregate mode's job)
    top, score = scored[0]
    result = top.fetch(request)
    result["_routing"] = {
        "chosen": top.__name__.split(".")[-1],
        "score": score,
        "considered": [{"adapter": a.__name__.split(".")[-1], "score": s} for a, s in scored],
    }
    return result


__all__ = ["databazaar", "huggingface", "world_bank", "route", "ADAPTERS"]
