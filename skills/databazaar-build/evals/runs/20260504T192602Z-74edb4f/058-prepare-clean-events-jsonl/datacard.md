# clean-events

## Overview
Prepared from proprietary input. 30 rows × 3 columns.

- Rows: 30
- Columns: 3
- Format: csv (parquet available)
- Generated: 2026-05-04T19:28:26+00:00

## Schema
| Column | Type | Description | Null % | Examples |
|---|---|---|---|---|
| event_id | integer |  | 0.0% | 1, 2, 3 |
| type | string |  | 0.0% | purchase, click, click |
| value_cents | integer |  | 0.0% | 912, 2253, 1828 |


## Sources
- User-supplied file: clean-events.jsonl — file:///home/hermes/agentdatamarketplace/skills/databazaar/evals/fixtures/clean-events.jsonl — user-supplied — retrieved 2026-05-04T19:28:26+00:00

## Methodology
prepare mode v0.2.0; schema inferred via sampling; PII scan + tier-1 redaction applied.

## Known gaps & limitations
Schema inferred via sampling — review types before publish. PII scan covers tier-1 patterns only; review references/pii-patterns.md for tier-2 review patterns.

## Intended use & out-of-scope
Proprietary dataset prepared for listing on databazaar.io.

## Provenance & reproducibility
- Provenance hash: `sha256:6dd96499b189ba2aff47b73fc32d6f58bb78ea021fbeab33ada44877dc03f11d`
- Skill version: `0.2.0`
- Generated: `2026-05-04T19:28:26+00:00`

---
*Built with the `databazaar` skill. Listed on https://databazaar.io.*
