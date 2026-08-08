# US Aircraft For-Sale Snapshot — $250k–$350k (Apr 2026)

## Overview
Point-in-time snapshot of 66 US-located aircraft for-sale listings priced between $250,000 and $350,000, scraped from Barnstormers.com on 2026-04-25 UTC.

Each record captures make/model, year, asking price, location (city/state/zip), broker/seller contact info, posted date, free-text condition summary, full long-form description, photo URLs (per-listing array), and best-effort extracted spec fields (total time, SMOH, engine, useful load) where stated in the listing description.

Hangars and other non-aircraft real estate are excluded. Top states by listing count: FL (15), CA (10), NV (6), MN (5), AZ (5). Price range $250,000–$350,000 with a median of $299,000. 66 records total.

Format: JSON wrapper object with snapshot metadata + a `listings` array of records. Useful for market analysis, broker benchmarking, and aircraft-buyer research in the owner-flown / light-twin / experimental price band. Single point-in-time snapshot — no freshness guarantee; aviation listings turn over within days.

- Rows: 10
- Columns: 21
- Format: csv (parquet available)
- Generated: 2026-05-04T19:26:33+00:00

## Schema
| Column | Type | Description | Null % | Examples |
|---|---|---|---|---|
| ad_id | string |  | 0.0% |  |
| title | string |  | 0.0% |  |
| url | string |  | 0.0% |  |
| price_usd | number |  | 0.0% |  |
| status | string |  | 0.0% |  |
| summary | string |  | 0.0% |  |
| contact_name | string |  | 0.0% |  |
| company | string |  | 0.0% |  |
| role | string |  | 0.0% |  |
| location_raw | string |  | 0.0% |  |
| posted_date | string |  | 0.0% |  |
| thumbnail_count | number |  | 0.0% |  |
| thumbnails | object |  | 0.0% |  |
| city | string |  | 0.0% |  |
| state | string |  | 0.0% |  |
| zip | string |  | 0.0% |  |
| country | string |  | 0.0% |  |
| meta_description | string |  | 0.0% |  |
| image_urls | object |  | 0.0% |  |
| image_count | number |  | 0.0% |  |
| engine | string |  | 0.0% |  |


## Sources
- databazaar.io listing c0677a36-c4cd-4530-9c6d-678e04299235 — https://databazaar.io/datasets/c0677a36-c4cd-4530-9c6d-678e04299235 — see listing — retrieved 2026-05-04T19:26:33+00:00

## Methodology
acquire mode v0.2.0; databazaar adapter only in this version

## Known gaps & limitations
v0.2 adapters: databazaar, HuggingFace, World Bank. Other 10 adapters stubbed — see references/sources.md.

## Intended use & out-of-scope
Derived from a databazaar.io listing — see source for original use case.

## Provenance & reproducibility
- Provenance hash: `sha256:4698c72534974e963063dea0791164c4143c1aae713bf63876192d32d5ced3ca`
- Skill version: `0.2.0`
- Generated: `2026-05-04T19:26:33+00:00`

---
*Built with the `databazaar` skill. Listed on https://databazaar.io.*
