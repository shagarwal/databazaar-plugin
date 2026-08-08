# pii-mixed-redact

## Overview
Prepared from proprietary input. 7 rows × 4 columns.

- Rows: 7
- Columns: 4
- Format: csv (parquet available)
- Generated: 2026-05-04T19:28:27+00:00

## Schema
| Column | Type | Description | Null % | Examples |
|---|---|---|---|---|
| id | integer |  | 0.0% | 1, 2, 3 |
| email | string |  | 0.0% | u1@x.com, u2@x.com, u3@x.com |
| phone | string |  | 0.0% | 415-555-0001, 415-555-0002, 415-555-0003 |
| city | string |  | 0.0% | SF, SF, SF |


## Sources
- User-supplied file: pii-mixed-redact.csv — file:///home/hermes/agentdatamarketplace/skills/databazaar/evals/fixtures/pii-mixed-redact.csv — user-supplied — retrieved 2026-05-04T19:28:27+00:00

## Methodology
prepare mode v0.2.0; schema inferred via sampling; PII scan + tier-1 redaction applied.

## Known gaps & limitations
Schema inferred via sampling — review types before publish. PII scan covers tier-1 patterns only; review references/pii-patterns.md for tier-2 review patterns.

## Intended use & out-of-scope
Proprietary dataset prepared for listing on databazaar.io.

## Provenance & reproducibility
- Provenance hash: `sha256:ab852b2196b60e1b3ffa5ac3bbf3cf3995ec10e376224ceaa90871ca999818df`
- Skill version: `0.2.0`
- Generated: `2026-05-04T19:28:27+00:00`

---
*Built with the `databazaar` skill. Listed on https://databazaar.io.*
