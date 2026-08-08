# Energy & Emissions Panel — 195 Countries (2000–2024)

## Overview
Multi-source panel dataset covering 195 countries over 25 years (2000–2024) with 18 energy and emissions indicators per country-year observation. Includes primary energy production and consumption by source (oil, natural gas, coal, nuclear, hydroelectric, solar, wind, biofuels & waste), total renewable capacity, electricity generation mix, CO₂ emissions from fuel combustion, energy intensity of GDP, per-capita consumption, and electrification rates. Data normalized and cross-referenced from International Energy Agency (IEA) World Energy Balances, World Bank World Development Indicators, BP Statistical Review of World Energy / Energy Institute, and IRENA Renewable Energy Statistics. Contains 12,675 country-year observations suitable for energy transition analysis, climate policy modeling, forecasting, and cross-country comparative studies.

- Rows: 11,495
- Columns: 22
- Format: csv (parquet available)
- Generated: 2026-05-04T19:27:20+00:00

## Schema
| Column | Type | Description | Null % | Examples |
|---|---|---|---|---|
| iso3 | string |  | 0.0% |  |
| country | string |  | 0.0% |  |
| continent | string |  | 0.0% |  |
| subregion | string |  | 0.0% |  |
| year | string |  | 0.0% |  |
| primary_energy_production_mtoe | string |  | 0.0% |  |
| primary_energy_consumption_mtoe | string |  | 0.0% |  |
| oil_production_mtoe | string |  | 0.0% |  |
| gas_production_mtoe | string |  | 0.0% |  |
| coal_production_mtoe | string |  | 0.0% |  |
| nuclear_generation_twh | string |  | 0.0% |  |
| hydro_generation_twh | string |  | 0.0% |  |
| solar_capacity_gw | string |  | 0.0% |  |
| wind_capacity_gw | string |  | 0.0% |  |
| renewable_share_pct | string |  | 0.0% |  |
| electricity_generation_twh | string |  | 0.0% |  |
| co2_emissions_mt | string |  | 0.0% |  |
| co2_per_capita_tonnes | string |  | 0.0% |  |
| energy_intensity_mj_per_usd | string |  | 0.0% |  |
| electrification_rate_pct | string |  | 0.0% |  |
| population_millions | string |  | 0.0% |  |
| gdp_per_capita_usd | string |  | 0.0% |  |


## Sources
- databazaar.io listing daa7b136-fdb1-4b47-9b6e-ae23b00990f2 — https://databazaar.io/datasets/daa7b136-fdb1-4b47-9b6e-ae23b00990f2 — see listing — retrieved 2026-05-04T19:27:19+00:00

## Methodology
acquire mode v0.2.0; databazaar adapter only in this version

## Known gaps & limitations
v0.2 adapters: databazaar, HuggingFace, World Bank. Other 10 adapters stubbed — see references/sources.md.

## Intended use & out-of-scope
Derived from a databazaar.io listing — see source for original use case.

## Provenance & reproducibility
- Provenance hash: `sha256:9a640d5a1b5b8acd03fe6e08aebd1688549ebdae4177b667f4f5d058d1d5e56b`
- Skill version: `0.2.0`
- Generated: `2026-05-04T19:27:20+00:00`

---
*Built with the `databazaar` skill. Listed on https://databazaar.io.*
