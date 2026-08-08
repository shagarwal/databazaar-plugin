# pii-phones-only

## Overview
Prepared from proprietary input. 5 rows × 3 columns.

- Rows: 5
- Columns: 3
- Format: csv (parquet available)
- Generated: 2026-05-04T19:28:27+00:00

## Schema
| Column | Type | Description | Null % | Examples |
|---|---|---|---|---|
| lead_id | integer |  | 0.0% | 1, 2, 3 |
| phone | string |  | 0.0% | 415-555-0100, (212) 555-0199, +1-310-555-0188 |
| source | string |  | 0.0% | web, web, web |


## Sources
- User-supplied file: pii-phones-only.csv — file:///home/hermes/agentdatamarketplace/skills/databazaar/evals/fixtures/pii-phones-only.csv — user-supplied — retrieved 2026-05-04T19:28:27+00:00

## Methodology
prepare mode v0.2.0; schema inferred via sampling; PII scan + tier-1 redaction applied.

## Known gaps & limitations
Schema inferred via sampling — review types before publish. PII scan covers tier-1 patterns only; review references/pii-patterns.md for tier-2 review patterns.

## Intended use & out-of-scope
Proprietary dataset prepared for listing on databazaar.io.

## Provenance & reproducibility
- Provenance hash: `sha256:f363009d296fc14d61d9738e9e8beab43f83daf4f64a62a5bb4c0fff124fb876`
- Skill version: `0.2.0`
- Generated: `2026-05-04T19:28:27+00:00`

---
*Built with the `databazaar` skill. Listed on https://databazaar.io.*
