# pii-emails-only

## Overview
Prepared from proprietary input. 5 rows × 3 columns.

- Rows: 5
- Columns: 3
- Format: csv (parquet available)
- Generated: 2026-05-04T19:28:27+00:00

## Schema
| Column | Type | Description | Null % | Examples |
|---|---|---|---|---|
| user_id | integer |  | 0.0% | 1, 2, 3 |
| email | string |  | 0.0% | user1@example.com, user2@example.com, user3@example.com |
| city | string |  | 0.0% | SF, NYC, LA |


## Sources
- User-supplied file: pii-emails-only.csv — file:///home/hermes/agentdatamarketplace/skills/databazaar/evals/fixtures/pii-emails-only.csv — user-supplied — retrieved 2026-05-04T19:28:27+00:00

## Methodology
prepare mode v0.2.0; schema inferred via sampling; PII scan + tier-1 redaction applied.

## Known gaps & limitations
Schema inferred via sampling — review types before publish. PII scan covers tier-1 patterns only; review references/pii-patterns.md for tier-2 review patterns.

## Intended use & out-of-scope
Proprietary dataset prepared for listing on databazaar.io.

## Provenance & reproducibility
- Provenance hash: `sha256:35477e7a88cfb2438363f1ade0bd3705e8fb8d5b19ba5975984c5226d640de4d`
- Skill version: `0.2.0`
- Generated: `2026-05-04T19:28:27+00:00`

---
*Built with the `databazaar` skill. Listed on https://databazaar.io.*
