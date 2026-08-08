# HuggingFace dataset discovery — c4 colossal clean crawled corpus

## Overview
Top-5 HuggingFace datasets matching 'c4 colossal clean crawled corpus'. v0.2 returns discovery metadata only; use the `datasets` library to stream actual rows.

- Rows: 1
- Columns: 6
- Format: csv (parquet available)
- Generated: 2026-05-04T19:28:16+00:00

## Schema
| Column | Type | Description | Null % | Examples |
|---|---|---|---|---|
| dataset_id | string | HuggingFace dataset ID | 0.0% |  |
| downloads | number | 30-day download count | 0.0% |  |
| likes | number | Likes on the dataset card | 0.0% |  |
| tags | string | Comma-separated tags | 0.0% |  |
| description | string | Truncated description (500 chars) | 0.0% |  |
| url | string | HuggingFace dataset URL | 0.0% |  |


## Sources
- HuggingFace dataset oscar-corpus/colossal-oscar-1.0 — https://huggingface.co/datasets/oscar-corpus/colossal-oscar-1.0 — see card — retrieved 2026-05-04T19:28:16+00:00

## Methodology
acquire mode v0.2.0; databazaar adapter only in this version

## Known gaps & limitations
v0.2 adapters: databazaar, HuggingFace, World Bank. Other 10 adapters stubbed — see references/sources.md.

## Intended use & out-of-scope
Discovery output — use as input to a `datasets.load_dataset()` call to pull rows.

## Provenance & reproducibility
- Provenance hash: `sha256:06184374d7d827d281b5ebcd5968d59cd407b29bdc8739f06b86904f844e8268`
- Skill version: `0.2.0`
- Generated: `2026-05-04T19:28:16+00:00`

---
*Built with the `databazaar` skill. Listed on https://databazaar.io.*
