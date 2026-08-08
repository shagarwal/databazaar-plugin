# clean-products

## Overview
Prepared from proprietary input. 20 rows × 4 columns.

- Rows: 20
- Columns: 4
- Format: csv (parquet available)
- Generated: 2026-05-04T19:28:26+00:00

## Schema
| Column | Type | Description | Null % | Examples |
|---|---|---|---|---|
| sku | string |  | 0.0% | P0001, P0002, P0003 |
| name | string |  | 0.0% | Widget 1, Widget 2, Widget 3 |
| price_usd | number |  | 0.0% | 10.99, 11.99, 12.99 |
| in_stock | string |  | 0.0% | True, True, False |


## Sources
- User-supplied file: clean-products.json — file:///home/hermes/agentdatamarketplace/skills/databazaar/evals/fixtures/clean-products.json — user-supplied — retrieved 2026-05-04T19:28:26+00:00

## Methodology
prepare mode v0.2.0; schema inferred via sampling; PII scan + tier-1 redaction applied.

## Known gaps & limitations
Schema inferred via sampling — review types before publish. PII scan covers tier-1 patterns only; review references/pii-patterns.md for tier-2 review patterns.

## Intended use & out-of-scope
Proprietary dataset prepared for listing on databazaar.io.

## Provenance & reproducibility
- Provenance hash: `sha256:8f9a14804f1ac17b70af253419b1e70a14194ab297f5f85a2935385c80983fa0`
- Skill version: `0.2.0`
- Generated: `2026-05-04T19:28:26+00:00`

---
*Built with the `databazaar` skill. Listed on https://databazaar.io.*
