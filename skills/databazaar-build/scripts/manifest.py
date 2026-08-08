"""Binary-asset manifest builder for datasets that include photos, PDFs, audio.

Walks an `assets/` subtree, hashes each file (sha256, first 16 bytes hex), and
emits `manifest.json` with row → asset mapping. Optional dedup by content hash.

Usage:
    python manifest.py --dir ./out --row-key listing_id [--dedup]

Reads `data.csv` to find which rows have assets. Each row is expected to have
either:
  - `asset_dir` column = relative path under assets/ (e.g. `assets/<id>/`)
  - or files at `assets/<row_key_value>/`

Produces `manifest.json`:
{
  "generated_at": "...",
  "row_key": "listing_id",
  "total_files": 10816,
  "total_size_bytes": 1253456789,
  "deduped": false,
  "entries": [
    {"row_key": "controller_242027373", "path": "assets/controller_242027373/9042896402.jpg",
     "size": 184231, "sha256_16": "ab12cd34..."}
  ]
}
"""
from __future__ import annotations
import argparse, csv, hashlib, json, sys, time
from pathlib import Path
from collections import defaultdict


def hash_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()[:16]


def build(out_dir: Path, row_key: str, dedup: bool) -> dict:
    data_csv = out_dir / "data.csv"
    assets_dir = out_dir / "assets"
    if not assets_dir.exists():
        return {"generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "row_key": row_key, "total_files": 0, "entries": []}

    # Map row_key value → list of files
    rows = list(csv.DictReader(data_csv.open()))
    keys = {r.get(row_key, "").strip() for r in rows if r.get(row_key)}
    keys.discard("")

    entries = []
    seen_hashes = {}
    total_size = 0
    duplicates = 0
    for sub in sorted(assets_dir.iterdir()):
        if not sub.is_dir():
            continue
        if sub.name not in keys:
            # asset for unknown row — flag but include
            pass
        for f in sorted(sub.rglob("*")):
            if not f.is_file():
                continue
            sz = f.stat().st_size
            h = hash_file(f)
            rel = f.relative_to(out_dir).as_posix()
            if dedup and h in seen_hashes:
                duplicates += 1
                continue
            seen_hashes[h] = rel
            total_size += sz
            entries.append({
                "row_key": sub.name,
                "path": rel,
                "size": sz,
                "sha256_16": h,
            })

    manifest = {
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "row_key": row_key,
        "total_files": len(entries),
        "total_size_bytes": total_size,
        "duplicates_removed": duplicates if dedup else 0,
        "deduped": dedup,
        "entries": entries,
    }
    return manifest


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", required=True)
    ap.add_argument("--row-key", required=True,
                    help="Column name whose value names the per-row asset subdir")
    ap.add_argument("--dedup", action="store_true",
                    help="Drop files with duplicate sha256")
    args = ap.parse_args()
    m = build(Path(args.dir), args.row_key, args.dedup)
    out = Path(args.dir) / "manifest.json"
    out.write_text(json.dumps(m, indent=2))
    print(f"manifest: {m['total_files']} files, {m['total_size_bytes']/1e6:.1f} MB"
          + (f", {m['duplicates_removed']} dups removed" if args.dedup else ""))


if __name__ == "__main__":
    main()
