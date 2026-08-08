# Healthcare Infrastructure & Disease Burden — 226 Countries (1980–2024)

## Overview
Wide-coverage panel dataset covering 226 countries and territories from 1980 to 2024 with 28 health system indicators. Includes life expectancy, infant and maternal mortality, physician and nurse density, hospital bed capacity, health expenditure (% GDP and per capita), immunization coverage (DPT and measles), HIV prevalence, tuberculosis incidence, NCD mortality risk, UHC service coverage index, water and sanitation access, obesity and diabetes prevalence, tobacco use, and alcohol consumption. Data synthesized from WHO Global Health Observatory, World Bank Health Nutrition and Population Statistics, UNICEF State of the Worlds Children, UNAIDS, and UN Population Division sources. Suitable for longitudinal health system analysis, cross-country benchmarking, disease burden modeling, and public health policy research.

- Rows: 10,170
- Columns: 28
- Format: csv (parquet available)
- Generated: 2026-05-04T19:28:00+00:00

## Schema
| Column | Type | Description | Null % | Examples |
|---|---|---|---|---|
| iso_code | string |  | 0.0% |  |
| country | string |  | 0.0% |  |
| region | string |  | 0.0% |  |
| year | string |  | 0.0% |  |
| life_expectancy_years | string |  | 0.0% |  |
| infant_mortality_per_1000 | string |  | 0.0% |  |
| under5_mortality_per_1000 | string |  | 0.0% |  |
| maternal_mortality_per_100k | string |  | 0.0% |  |
| physicians_per_1000 | string |  | 0.0% |  |
| nurses_per_1000 | string |  | 0.0% |  |
| hospital_beds_per_1000 | string |  | 0.0% |  |
| health_expenditure_pct_gdp | string |  | 0.0% |  |
| health_expenditure_per_capita_usd | string |  | 0.0% |  |
| out_of_pocket_expenditure_pct | string |  | 0.0% |  |
| dpt_immunization_pct | string |  | 0.0% |  |
| measles_immunization_pct | string |  | 0.0% |  |
| hiv_prevalence_pct | string |  | 0.0% |  |
| tb_incidence_per_100k | string |  | 0.0% |  |
| ncd_mortality_pct_30_70 | string |  | 0.0% |  |
| uhc_service_coverage_index | string |  | 0.0% |  |
| birth_rate_per_1000 | string |  | 0.0% |  |
| death_rate_per_1000 | string |  | 0.0% |  |
| clean_water_access_pct | string |  | 0.0% |  |
| sanitation_access_pct | string |  | 0.0% |  |
| obesity_prevalence_pct | string |  | 0.0% |  |
| diabetes_prevalence_pct | string |  | 0.0% |  |
| tobacco_use_pct | string |  | 0.0% |  |
| alcohol_consumption_liters_pc | string |  | 0.0% |  |


## Sources
- databazaar.io listing 526457a6-a870-49ab-9115-c236fbfdf377 — https://databazaar.io/datasets/526457a6-a870-49ab-9115-c236fbfdf377 — see listing — retrieved 2026-05-04T19:27:58+00:00

## Methodology
acquire mode v0.2.0; databazaar adapter only in this version

## Known gaps & limitations
v0.2 adapters: databazaar, HuggingFace, World Bank. Other 10 adapters stubbed — see references/sources.md.

## Intended use & out-of-scope
Derived from a databazaar.io listing — see source for original use case.

## Provenance & reproducibility
- Provenance hash: `sha256:b69b738b49f924ce2b6e9e09e983d9a0cdf17ecd9ddc178ef444381e35174bb9`
- Skill version: `0.2.0`
- Generated: `2026-05-04T19:28:00+00:00`

---
*Built with the `databazaar` skill. Listed on https://databazaar.io.*
