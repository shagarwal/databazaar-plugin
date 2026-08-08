# International Tourism, Travel & Transport Statistics (1960–2023)

## Overview
Multi-source panel dataset covering international tourism, air transport, surface transport, trade in services, and international migration for 218 countries from 1960 to 2023. Contains 13,952 observations across 31 variables including tourism arrivals/departures, receipts/expenditures, air passenger volumes, railway traffic, container port throughput, and derived indicators like tourism intensity per capita and tourism balance.

**Sources:** World Bank Open Data API — 25 indicator series compiled from World Development Indicators (WDI), International Tourism statistics (UNWTO via World Bank), ICAO air transport data, and UN Population Division migration estimates.

**Key Features:**
- 218 countries and territories
- 64-year time span (1960–2023)
- 8 core tourism indicators (arrivals, departures, receipts, expenditures)
- 3 air transport indicators (passengers, departures, freight)
- 2 surface transport indicators (railways passengers, freight)
- 5 trade & services indicators
- 3 migration indicators
- 4 derived analytical indicators (tourism intensity, receipts % GDP, tourism balance, air passengers per capita)
- GDP, GDP per capita, and population for contextual analysis

**Format:** Wide panel — one row per country-year, all indicators as columns. Missing values left blank (not all indicators available for all country-years).

**Use Cases:** Tourism economics research, travel industry analysis, transport infrastructure comparisons, international mobility trends, COVID-19 impact studies on global tourism, development economics.

- Rows: 13,952
- Columns: 31
- Format: csv (parquet available)
- Generated: 2026-05-04T19:27:28+00:00

## Schema
| Column | Type | Description | Null % | Examples |
|---|---|---|---|---|
| country_code | string |  | 0.0% |  |
| country_name | string |  | 0.0% |  |
| year | string |  | 0.0% |  |
| international_tourism_arrivals | string |  | 0.0% |  |
| international_tourism_departures | string |  | 0.0% |  |
| tourism_receipts_usd | string |  | 0.0% |  |
| tourism_expenditures_usd | string |  | 0.0% |  |
| tourism_receipts_pct_exports | string |  | 0.0% |  |
| tourism_expenditures_pct_imports | string |  | 0.0% |  |
| tourism_receipts_travel_items_usd | string |  | 0.0% |  |
| tourism_expenditures_travel_items_usd | string |  | 0.0% |  |
| air_transport_passengers | string |  | 0.0% |  |
| air_transport_departures | string |  | 0.0% |  |
| air_transport_freight_million_ton_km | string |  | 0.0% |  |
| exports_goods_services_usd | string |  | 0.0% |  |
| imports_goods_services_usd | string |  | 0.0% |  |
| travel_services_pct_exports | string |  | 0.0% |  |
| travel_services_pct_imports | string |  | 0.0% |  |
| international_migrant_stock | string |  | 0.0% |  |
| international_migrant_stock_pct_pop | string |  | 0.0% |  |
| net_migration | string |  | 0.0% |  |
| railways_passengers_km | string |  | 0.0% |  |
| railways_freight_million_ton_km | string |  | 0.0% |  |
| container_port_traffic_teu | string |  | 0.0% |  |
| gdp_current_usd | string |  | 0.0% |  |
| gdp_per_capita_usd | string |  | 0.0% |  |
| population | string |  | 0.0% |  |
| tourism_intensity_per_1000 | string |  | 0.0% |  |
| tourism_receipts_pct_gdp | string |  | 0.0% |  |
| tourism_balance_usd | string |  | 0.0% |  |
| air_passengers_per_capita | string |  | 0.0% |  |


## Sources
- databazaar.io listing a006b11c-c814-4f7a-84fc-2f73f65d7664 — https://databazaar.io/datasets/a006b11c-c814-4f7a-84fc-2f73f65d7664 — see listing — retrieved 2026-05-04T19:27:26+00:00

## Methodology
acquire mode v0.2.0; databazaar adapter only in this version

## Known gaps & limitations
v0.2 adapters: databazaar, HuggingFace, World Bank. Other 10 adapters stubbed — see references/sources.md.

## Intended use & out-of-scope
Derived from a databazaar.io listing — see source for original use case.

## Provenance & reproducibility
- Provenance hash: `sha256:d524ab326632160b0154bc4e43cf494ff394767eadf573bfa162e663a855cd92`
- Skill version: `0.2.0`
- Generated: `2026-05-04T19:27:28+00:00`

---
*Built with the `databazaar` skill. Listed on https://databazaar.io.*
