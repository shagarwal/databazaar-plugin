# Residential Property Market Index — 77 Cities, 45 Countries (2015–2025)

## Overview
Longitudinal quarterly dataset tracking residential property markets across 77 major cities in 45 countries, spanning 2015-2025. Contains 16,940 records covering 5 property types (Apartment, House, Condo, Townhouse, Studio) with 22 variables including price per square meter (USD), median property prices, rental yields, price-to-income ratios, year-over-year and quarter-over-quarter price changes, affordability indices, transaction volume indices, average days on market, mortgage rates, and new construction activity indices. Data is normalized to USD and structured for cross-city and cross-regional comparison. Ideal for real estate market analysis, housing affordability research, investment strategy modeling, and macroeconomic studies.

- Rows: 16,940
- Columns: 22
- Format: csv (parquet available)
- Generated: 2026-05-04T19:27:03+00:00

## Schema
| Column | Type | Description | Null % | Examples |
|---|---|---|---|---|
| id | string |  | 0.0% |  |
| city | string |  | 0.0% |  |
| country | string |  | 0.0% |  |
| region | string |  | 0.0% |  |
| year | string |  | 0.0% |  |
| quarter | string |  | 0.0% |  |
| property_type | string |  | 0.0% |  |
| avg_size_sqm | string |  | 0.0% |  |
| price_per_sqm_usd | string |  | 0.0% |  |
| median_price_usd | string |  | 0.0% |  |
| rental_yield_pct | string |  | 0.0% |  |
| monthly_rent_per_sqm_usd | string |  | 0.0% |  |
| price_to_income_ratio | string |  | 0.0% |  |
| yoy_price_change_pct | string |  | 0.0% |  |
| qoq_price_change_pct | string |  | 0.0% |  |
| city_population_millions | string |  | 0.0% |  |
| gdp_per_capita_usd | string |  | 0.0% |  |
| affordability_index | string |  | 0.0% |  |
| transaction_volume_index | string |  | 0.0% |  |
| avg_days_on_market | string |  | 0.0% |  |
| avg_mortgage_rate_pct | string |  | 0.0% |  |
| new_construction_index | string |  | 0.0% |  |


## Sources
- databazaar.io listing 23a12a33-f1da-4050-9af4-6525f6a6ec59 — https://databazaar.io/datasets/23a12a33-f1da-4050-9af4-6525f6a6ec59 — see listing — retrieved 2026-05-04T19:27:02+00:00

## Methodology
acquire mode v0.2.0; databazaar adapter only in this version

## Known gaps & limitations
v0.2 adapters: databazaar, HuggingFace, World Bank. Other 10 adapters stubbed — see references/sources.md.

## Intended use & out-of-scope
Derived from a databazaar.io listing — see source for original use case.

## Provenance & reproducibility
- Provenance hash: `sha256:5726202ac9708335978c97be572ba495641318b6a7cf2b80af2209443a4ab549`
- Skill version: `0.2.0`
- Generated: `2026-05-04T19:27:03+00:00`

---
*Built with the `databazaar` skill. Listed on https://databazaar.io.*
