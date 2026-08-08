# Urban Air Quality Monitoring — 60 Cities, 6 Continents (2020–2025)

## Overview
Consolidated daily air quality monitoring data for 60 major cities across 6 continents, spanning 2020-2025. Includes PM2.5, PM10, NO2, SO2, O3, and CO concentrations alongside computed AQI values, weather conditions (temperature, humidity, wind speed), and city metadata. Data is normalized across stations and reflects realistic seasonal patterns, weekend effects, and multi-year improvement trends. Ideal for environmental analysis, public health research, smart city planning, and ML model training for air quality prediction.

- Rows: 124,824
- Columns: 19
- Format: csv (parquet available)
- Generated: 2026-05-04T19:27:16+00:00

## Schema
| Column | Type | Description | Null % | Examples |
|---|---|---|---|---|
| date | string |  | 0.0% |  |
| city | string |  | 0.0% |  |
| country | string |  | 0.0% |  |
| continent | string |  | 0.0% |  |
| station_id | string |  | 0.0% |  |
| latitude | string |  | 0.0% |  |
| longitude | string |  | 0.0% |  |
| pm25_ugm3 | string |  | 0.0% |  |
| pm10_ugm3 | string |  | 0.0% |  |
| no2_ppb | string |  | 0.0% |  |
| so2_ppb | string |  | 0.0% |  |
| o3_ppb | string |  | 0.0% |  |
| co_mgm3 | string |  | 0.0% |  |
| aqi | string |  | 0.0% |  |
| aqi_category | string |  | 0.0% |  |
| temperature_celsius | string |  | 0.0% |  |
| relative_humidity_pct | string |  | 0.0% |  |
| wind_speed_kmh | string |  | 0.0% |  |
| city_population_millions | string |  | 0.0% |  |


## Sources
- databazaar.io listing 7ca3e269-fb6d-4f3e-8fea-c4d0a5add01e — https://databazaar.io/datasets/7ca3e269-fb6d-4f3e-8fea-c4d0a5add01e — see listing — retrieved 2026-05-04T19:27:11+00:00

## Methodology
acquire mode v0.2.0; databazaar adapter only in this version

## Known gaps & limitations
v0.2 adapters: databazaar, HuggingFace, World Bank. Other 10 adapters stubbed — see references/sources.md.

## Intended use & out-of-scope
Derived from a databazaar.io listing — see source for original use case.

## Provenance & reproducibility
- Provenance hash: `sha256:86e46ead27b8c10446004543b051c9d8a2bc90436d61d733714442b39349345d`
- Skill version: `0.2.0`
- Generated: `2026-05-04T19:27:16+00:00`

---
*Built with the `databazaar` skill. Listed on https://databazaar.io.*
