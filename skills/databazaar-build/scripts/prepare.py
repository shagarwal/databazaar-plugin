"""prepare mode — turn proprietary input into a listable dataset.

Steps:
1. Load input file (csv/json/jsonl supported in v0.2; xlsx/parquet/sql later).
2. Schema inference (types via sampling, null rates, sample values).
3. PII scan against references/pii-patterns.md tier-1 patterns.
4. Auto-redact tier-1 emails/phones; BLOCK on SSN/credit-card/API-key.
5. Emit normal output contract via build._write_outputs.
"""
from __future__ import annotations
import csv, json, re
from datetime import datetime, timezone
from pathlib import Path

# Tier-1 PII patterns (subset; see references/pii-patterns.md)
EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
US_PHONE_RE = re.compile(r"\b(?:\+?1[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b")
SSN_RE = re.compile(r"\b\d{3}-\d{2}-\d{4}\b")
APIKEY_RE = re.compile(r"\b(?:sk-|pk_|dbz_live_|AKIA)[A-Za-z0-9]{16,}\b")

BLOCKING_PATTERNS = [
    ("ssn", SSN_RE),
    ("api_key", APIKEY_RE),
]
REDACTING_PATTERNS = [
    ("email", EMAIL_RE, "<email>"),
    ("phone", US_PHONE_RE, "<phone>"),
]


def _ts() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def load_rows(path: Path) -> list[dict]:
    text = path.read_text()
    if path.suffix.lower() == ".csv":
        return list(csv.DictReader(text.splitlines()))
    if path.suffix.lower() == ".jsonl":
        return [json.loads(line) for line in text.splitlines() if line.strip()]
    if path.suffix.lower() == ".json":
        d = json.loads(text)
        if isinstance(d, list):
            return d
        if isinstance(d, dict):
            for key in ("data", "rows", "listings", "items"):
                if key in d and isinstance(d[key], list):
                    return d[key]
        raise ValueError("JSON input must be a list, or a dict with data/rows/listings/items array")
    raise ValueError(f"Unsupported format: {path.suffix}")


def infer_schema(rows: list[dict], title: str) -> dict:
    if not rows:
        return {"title": title, "columns": []}
    cols = list(rows[0].keys())
    out_cols = []
    n = len(rows)
    for c in cols:
        vals = [r.get(c) for r in rows]
        non_null = [v for v in vals if v not in (None, "", "NaN", "null")]
        null_rate = 1 - (len(non_null) / max(1, n))

        # Type inference
        t = "string"
        if non_null:
            try:
                [int(str(v)) for v in non_null[:50]]
                t = "integer"
            except (ValueError, TypeError):
                try:
                    [float(str(v)) for v in non_null[:50]]
                    t = "number"
                except (ValueError, TypeError):
                    t = "string"

        out_cols.append({
            "name": c,
            "type": t,
            "description": "",
            "null_rate": round(null_rate, 3),
            "sample_values": [str(v) for v in non_null[:3]],
        })
    return {
        "title": title,
        "description": f"Prepared from proprietary input. {n} rows × {len(cols)} columns.",
        "category": "other",
        "tags": [],
        "columns": out_cols,
    }


def scan_pii(rows: list[dict]) -> dict:
    detections = []
    blockers = []

    # Sample up to 1000 rows for scanning (fast + good coverage)
    sample = rows[:1000]

    for col in (rows[0].keys() if rows else []):
        col_str = " ".join(str(r.get(col, "")) for r in sample)

        # Blocking patterns (refuse entirely)
        for pname, pat in BLOCKING_PATTERNS:
            matches = pat.findall(col_str)
            if matches:
                detections.append({
                    "column": col, "pattern": pname, "tier": 1,
                    "match_count": len(matches), "action": "blocked",
                })
                blockers.append(f"{pname} in column '{col}'")

        # Redacting patterns
        for pname, pat, _ in REDACTING_PATTERNS:
            matches = pat.findall(col_str)
            if matches:
                detections.append({
                    "column": col, "pattern": pname, "tier": 1,
                    "match_count": len(matches), "action": "redacted",
                })

    return {
        "scanned_at": _ts(),
        "row_count": len(rows),
        "detections": detections,
        "blocked": bool(blockers),
        "blockers": blockers,
    }


def redact_rows(rows: list[dict]) -> list[dict]:
    out = []
    for r in rows:
        new = {}
        for k, v in r.items():
            sv = str(v) if v is not None else ""
            for _, pat, repl in REDACTING_PATTERNS:
                sv = pat.sub(repl, sv)
            new[k] = sv
        new.setdefault("_source", "user-supplied")
        new.setdefault("_retrieved_at", _ts())
        out.append(new)
    return out


def run(input_path: str, title: str = None) -> dict:
    p = Path(input_path)
    title = title or p.stem
    rows = load_rows(p)
    schema = infer_schema(rows, title)
    pii = scan_pii(rows)
    redacted = redact_rows(rows)
    return {
        "rows": redacted,
        "schema": schema,
        "sources": [{
            "name": f"User-supplied file: {p.name}",
            "url": f"file://{p.resolve()}",
            "license": "user-supplied",
            "retrieved_at": _ts(),
        }],
        "pii_report": pii,
        "intended_use": "Proprietary dataset prepared for listing on databazaar.io.",
        "gaps": "Schema inferred via sampling — review types before publish. PII scan covers tier-1 patterns only; review references/pii-patterns.md for tier-2 review patterns.",
    }
