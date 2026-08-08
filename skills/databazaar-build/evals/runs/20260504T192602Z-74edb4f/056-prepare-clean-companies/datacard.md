# clean-companies

## Overview
Prepared from proprietary input. 5 rows × 4 columns.

- Rows: 5
- Columns: 4
- Format: csv (parquet available)
- Generated: 2026-05-04T19:28:26+00:00

## Schema
| Column | Type | Description | Null % | Examples |
|---|---|---|---|---|
| company | string |  | 0.0% | Acme, Globex, Initech |
| founded | integer |  | 0.0% | 1985, 2001, 1999 |
| employees | integer |  | 0.0% | 1200, 340, 55 |
| revenue_usd | integer |  | 0.0% | 450000000, 72000000, 8500000 |


## Sources
- User-supplied file: clean-companies.csv — file:///home/hermes/agentdatamarketplace/skills/databazaar/evals/fixtures/clean-companies.csv — user-supplied — retrieved 2026-05-04T19:28:26+00:00

## Methodology
prepare mode v0.2.0; schema inferred via sampling; PII scan + tier-1 redaction applied.

## Known gaps & limitations
Schema inferred via sampling — review types before publish. PII scan covers tier-1 patterns only; review references/pii-patterns.md for tier-2 review patterns.

## Intended use & out-of-scope
Proprietary dataset prepared for listing on databazaar.io.

## Provenance & reproducibility
- Provenance hash: `sha256:de41f3fec9a014de0f63357bf1397146281ea6bb728ec9fb5ca45c060632fd2a`
- Skill version: `0.2.0`
- Generated: `2026-05-04T19:28:26+00:00`

---
*Built with the `databazaar` skill. Listed on https://databazaar.io.*
