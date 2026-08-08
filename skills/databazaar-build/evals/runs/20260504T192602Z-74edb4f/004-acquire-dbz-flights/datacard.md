# International Flight Routes & Airport Connectivity Network

## Overview
Cleaned dataset of 66,771 commercial flight routes connecting 3,214 airports across 225 countries, enriched with airline data, geographic coordinates, route distances, and country-level economic indicators.

## Sources
- **OpenFlights**: Airport locations, airline information, and route data for all commercial airlines worldwide
- **World Bank**: Country-level population (2023), GDP per capita (2023), and air passenger volume (2022)

## Key Features
- Route-level detail: origin/destination airports, airline, distance (km), equipment type
- Distance classification: short-haul (<500km), medium-haul, long-haul, ultra-long-haul (>4000km)
- Domestic vs international and intercontinental route flags
- Country-level economic context: population, GDP per capita, air passenger volumes
- Continental and timezone coverage for all airports

## Coverage
- 66,771 routes | 546 airlines | 3,214 airports | 225 countries
- Distance distribution: 12K short-haul, 28K medium-haul, 20K long-haul, 7K ultra-long-haul
- Intercontinental routes: 9,479

## Use Cases
- Aviation network analysis and hub identification
- Route optimization and market gap analysis
- Economic corridor mapping between countries
- Geographic accessibility studies
- Airline competitive landscape analysis

- Rows: 66,771
- Columns: 30
- Format: csv (parquet available)
- Generated: 2026-05-04T19:26:50+00:00

## Schema
| Column | Type | Description | Null % | Examples |
|---|---|---|---|---|
| route_id | string |  | 0.0% |  |
| airline_code | string |  | 0.0% |  |
| airline_name | string |  | 0.0% |  |
| airline_country | string |  | 0.0% |  |
| airline_active | string |  | 0.0% |  |
| source_airport_code | string |  | 0.0% |  |
| source_airport_name | string |  | 0.0% |  |
| source_city | string |  | 0.0% |  |
| source_country | string |  | 0.0% |  |
| source_continent | string |  | 0.0% |  |
| source_latitude | string |  | 0.0% |  |
| source_longitude | string |  | 0.0% |  |
| dest_airport_code | string |  | 0.0% |  |
| dest_airport_name | string |  | 0.0% |  |
| dest_city | string |  | 0.0% |  |
| dest_country | string |  | 0.0% |  |
| dest_continent | string |  | 0.0% |  |
| dest_latitude | string |  | 0.0% |  |
| dest_longitude | string |  | 0.0% |  |
| distance_km | string |  | 0.0% |  |
| distance_class | string |  | 0.0% |  |
| is_codeshare | string |  | 0.0% |  |
| stops | string |  | 0.0% |  |
| equipment | string |  | 0.0% |  |
| is_domestic | string |  | 0.0% |  |
| is_intercontinental | string |  | 0.0% |  |
| source_country_population | string |  | 0.0% |  |
| source_country_gdp_per_capita | string |  | 0.0% |  |
| dest_country_population | string |  | 0.0% |  |
| dest_country_gdp_per_capita | string |  | 0.0% |  |


## Sources
- databazaar.io listing 71f62319-b8c7-42f1-be03-c7eb69308335 — https://databazaar.io/datasets/71f62319-b8c7-42f1-be03-c7eb69308335 — see listing — retrieved 2026-05-04T19:26:40+00:00

## Methodology
acquire mode v0.2.0; databazaar adapter only in this version

## Known gaps & limitations
v0.2 adapters: databazaar, HuggingFace, World Bank. Other 10 adapters stubbed — see references/sources.md.

## Intended use & out-of-scope
Derived from a databazaar.io listing — see source for original use case.

## Provenance & reproducibility
- Provenance hash: `sha256:a66c16d1749e04a642a6dc0c0a574ff445ecc0e61617cb9911198f81fdf09ddb`
- Skill version: `0.2.0`
- Generated: `2026-05-04T19:26:50+00:00`

---
*Built with the `databazaar` skill. Listed on https://databazaar.io.*
