"""Pre-publish integrity validation for databazaar listings.

Catches the silent-merge-failure class of bugs (data.csv has fewer rows than
provenance/stats claim). Run as the last gate before `list` mode.

Usage:
    python validate.py --dir ./out [--paid]

Exit codes:
    0  — all checks passed
    1  — validation failure (block publish)
    2  — usage error
"""
from __future__ import annotations
import argparse, csv, json, sys
from pathlib import Path


def _load_json(p: Path):
    if not p.exists():
        return None
    return json.loads(p.read_text())


def validate(out_dir: Path, paid: bool = False) -> tuple[bool, list[str]]:
    errors: list[str] = []

    data_csv = out_dir / "data.csv"
    if not data_csv.exists():
        return False, ["data.csv missing"]

    # Row count from CSV (proper csv.reader to handle embedded newlines)
    with data_csv.open() as f:
        rdr = csv.reader(f)
        try:
            next(rdr)  # header
        except StopIteration:
            return False, ["data.csv has no header"]
        actual_rows = sum(1 for _ in rdr)

    prov = _load_json(out_dir / "provenance.json")
    stats = _load_json(out_dir / "_stats.json")
    schema = _load_json(out_dir / "schema.json")

    # 1. data.csv vs provenance.row_count
    if prov is not None:
        prov_count = prov.get("row_count")
        if prov_count is not None and prov_count != actual_rows:
            errors.append(
                f"row count mismatch: data.csv has {actual_rows} but "
                f"provenance.json claims {prov_count}"
            )
        per_row = prov.get("rows") or []
        if per_row and len(per_row) != actual_rows:
            errors.append(
                f"provenance.rows length {len(per_row)} != data.csv rows {actual_rows}"
            )

    # 2. data.csv vs _stats.json["rows"]
    if stats and "rows" in stats:
        if stats["rows"] != actual_rows:
            errors.append(
                f"_stats.json rows={stats['rows']} != data.csv rows {actual_rows}"
            )

    # 3. Sum of per-source counts in stats == row count (when single-source-per-row)
    if stats and "sources" in stats and isinstance(stats["sources"], dict):
        src_total = sum(stats["sources"].values())
        # Allow src_total >= actual_rows because cross-listed rows can have multiple sources.
        # But src_total < actual_rows means we lost rows during merge.
        if src_total < actual_rows:
            errors.append(
                f"sum of source counts {src_total} < data.csv rows {actual_rows} "
                f"(likely merge failure)"
            )

    # 4. Per-row source attribution for paid listings
    if paid and prov is not None:
        per_row = prov.get("rows") or []
        if not per_row:
            errors.append("paid listing requires provenance.rows entries; none found")
        else:
            unknown = sum(1 for r in per_row if not r.get("source") or r["source"] == "unknown")
            if unknown:
                errors.append(
                    f"paid listing: {unknown}/{len(per_row)} rows have empty/unknown source"
                )
            no_ts = sum(1 for r in per_row if not r.get("retrieved_at"))
            if no_ts:
                errors.append(
                    f"paid listing: {no_ts}/{len(per_row)} rows missing retrieved_at"
                )

    # 5. Datacard enumerates every source named in provenance
    datacard = (out_dir / "datacard.md")
    if datacard.exists() and prov:
        text = datacard.read_text().lower()
        prov_sources = {s.get("name", "").lower() for s in (prov.get("sources") or [])}
        prov_sources.discard("")
        missing = [s for s in prov_sources if s and s not in text]
        if missing:
            errors.append(
                f"datacard.md missing source attribution for: {', '.join(missing)}"
            )

    # 6. Manifest <-> assets dir consistency (if manifest present)
    manifest_path = out_dir / "manifest.json"
    if manifest_path.exists():
        manifest = _load_json(manifest_path)
        assets_dir = out_dir / "assets"
        if not assets_dir.exists():
            errors.append("manifest.json present but assets/ directory missing")
        else:
            entries = manifest.get("entries", []) if isinstance(manifest, dict) else []
            missing_files = []
            for e in entries[:500]:  # spot check first 500
                p = out_dir / e.get("path", "")
                if not p.exists():
                    missing_files.append(e.get("path"))
            if missing_files:
                errors.append(
                    f"manifest references missing files (first 5): {missing_files[:5]}"
                )

    return (len(errors) == 0), errors


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", required=True, help="output directory")
    ap.add_argument("--paid", action="store_true",
                    help="apply stricter checks for paid listings")
    args = ap.parse_args()
    ok, errors = validate(Path(args.dir), paid=args.paid)
    if ok:
        print("validate: ok")
        sys.exit(0)
    print("validate: FAILED", file=sys.stderr)
    for e in errors:
        print(f"  - {e}", file=sys.stderr)
    sys.exit(1)


if __name__ == "__main__":
    main()
