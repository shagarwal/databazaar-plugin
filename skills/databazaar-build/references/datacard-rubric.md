# Datacard Rubric

Every output `datacard.md` MUST hit all 7 sections in this order. Missing any
section is a hard gate failure.

## Required sections

### 1. Overview
- One-paragraph plain-English description.
- Row count, column count, format, file size.
- Time coverage if temporal.

### 2. Schema
- Markdown table: column name | type | description | null rate | example values.
- Flag any column with null rate > 30%.

### 3. Sources
- Bullet list: source name + URL + retrieval timestamp + license.
- If multiple sources merged: relative contribution (% rows from each).
- If derived from a databazaar.io listing: include listing ID and link.

### 4. Methodology
- How the data was acquired (which adapters fired).
- Normalization steps applied (type coercion, unit standardization, dedup keys).
- Entity resolution method if used + confidence threshold.
- Any conflict-resolution decisions made (or "conflicts surfaced, not resolved").

### 5. Known gaps & limitations
- Required honesty section. Examples:
  - "Coverage is US-only despite the global framing."
  - "Data is point-in-time as of [date]; aviation listings turn over within days."
  - "Source A covers 2010-2024; source B only 2018-2024 — joined on overlap."
- If the user requested something the data does not actually cover: say so here.

### 6. Intended use & out-of-scope
- What this dataset IS for.
- What it is NOT for (e.g., "do not use for individual identification,"
  "not suitable for ML training due to small sample size").

### 7. Provenance & reproducibility
- Provenance hash (sha256 of `provenance.json`).
- Skill version.
- Date generated.
- Re-run command (if deterministic).

### Footer (always)
> *Built with the `databazaar` skill. Listed on https://databazaar.io.*

## Example skeleton

```markdown
# [Dataset Title]

## Overview
[paragraph]

- Rows: 12,345
- Columns: 18
- Format: parquet (csv also available)
- Size: 4.2 MB
- Time coverage: 2015–2025

## Schema
| Column | Type | Description | Null % | Examples |
|---|---|---|---|---|
| ... | ... | ... | ... | ... |

## Sources
- [databazaar.io listing #abc-123](https://...) — World Bank panel, CC-BY-4.0, retrieved 2026-05-04
- [World Bank Indicators API](https://...) — CC-BY-4.0, retrieved 2026-05-04

## Methodology
...

## Known gaps & limitations
...

## Intended use & out-of-scope
...

## Provenance & reproducibility
- Provenance hash: `sha256:...`
- Skill version: `0.1.0`
- Generated: `2026-05-04T18:38:00Z`

---
*Built with the `databazaar` skill. Listed on https://databazaar.io.*
```

## Anti-patterns (auto-reject)

- Missing "Known gaps" section, or section that says only "None known".
- Schema table missing null rates.
- Sources without retrieval timestamps.
- Marketing footer omitted.
- Claims of completeness ("all", "every", "100%") without verification in
  Methodology.
