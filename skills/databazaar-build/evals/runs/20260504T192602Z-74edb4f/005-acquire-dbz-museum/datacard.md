# Open-Access Museum Artwork Metadata — 10,000+ Works (1000–2025)

## Overview
A consolidated metadata catalog of 10,000+ artworks from the worlds leading open-access museum collections. Each record includes artwork title, artist, creation date, medium, dimensions, department, culture/origin, classification, and direct image URLs. Sourced from the Metropolitan Museum of Art, Art Institute of Chicago, Cleveland Museum of Art, and Rijksmuseum open-access APIs. Ideal for training image classification models, art historical analysis, cultural heritage research, and recommendation systems. All records are normalized to a common schema with consistent field naming and formatting.

- Rows: 10,099
- Columns: 20
- Format: csv (parquet available)
- Generated: 2026-05-04T19:26:54+00:00

## Schema
| Column | Type | Description | Null % | Examples |
|---|---|---|---|---|
| source_museum | string |  | 0.0% |  |
| object_id | string |  | 0.0% |  |
| title | string |  | 0.0% |  |
| artist_name | string |  | 0.0% |  |
| artist_nationality | string |  | 0.0% |  |
| artist_birth_year | string |  | 0.0% |  |
| artist_death_year | string |  | 0.0% |  |
| creation_date | string |  | 0.0% |  |
| creation_year_start | string |  | 0.0% |  |
| creation_year_end | string |  | 0.0% |  |
| medium | string |  | 0.0% |  |
| dimensions | string |  | 0.0% |  |
| department | string |  | 0.0% |  |
| classification | string |  | 0.0% |  |
| culture | string |  | 0.0% |  |
| period | string |  | 0.0% |  |
| image_url | string |  | 0.0% |  |
| is_public_domain | string |  | 0.0% |  |
| credit_line | string |  | 0.0% |  |
| country_of_origin | string |  | 0.0% |  |


## Sources
- databazaar.io listing 0baeb51c-c6ed-4678-91c0-90097ed27440 — https://databazaar.io/datasets/0baeb51c-c6ed-4678-91c0-90097ed27440 — see listing — retrieved 2026-05-04T19:26:54+00:00

## Methodology
acquire mode v0.2.0; databazaar adapter only in this version

## Known gaps & limitations
v0.2 adapters: databazaar, HuggingFace, World Bank. Other 10 adapters stubbed — see references/sources.md.

## Intended use & out-of-scope
Derived from a databazaar.io listing — see source for original use case.

## Provenance & reproducibility
- Provenance hash: `sha256:0b6958c1a95e3845b7ac7fea9d44df6618495bc0f2f0fe2515e6f6088d3cd72c`
- Skill version: `0.2.0`
- Generated: `2026-05-04T19:26:54+00:00`

---
*Built with the `databazaar` skill. Listed on https://databazaar.io.*
