# Seismic Events Database — 94,767 Earthquakes (2020–2025)

## Overview
Wide-coverage catalog of 94,767 seismic events (magnitude 4.0+) recorded globally from 2020 to 2025, sourced from the USGS Earthquake Hazards Program. Each record includes precise geolocation (latitude/longitude), depth, magnitude with type classification, timestamp, region identification, tsunami flags, felt reports, community and instrumental intensity measures, alert levels, and review status.

Key features:
- **94,767 unique events** spanning 6 years (2020–2025)
- **Global coverage**: 180+ countries and regions, with major representation from Indonesia, Japan, Philippines, Chile, and the Pacific Ring of Fire
- **Enriched classifications**: depth class (shallow/intermediate/deep), magnitude class (light/moderate/strong/major/great)
- **Multi-source validation**: Events cross-referenced across USGS contributing networks
- **28 columns** including technical parameters (RMS error, azimuthal gap, station count) for advanced seismological analysis

Ideal for: seismic risk modeling, geospatial analysis, climate/disaster research, machine learning (earthquake prediction), insurance risk assessment, and educational use.

Data sourced from the USGS Earthquake Hazards Program (earthquake.usgs.gov), a globally authoritative public seismological data source.

- Rows: 94,767
- Columns: 28
- Format: csv (parquet available)
- Generated: 2026-05-04T19:26:29+00:00

## Schema
| Column | Type | Description | Null % | Examples |
|---|---|---|---|---|
| event_id | string |  | 0.0% |  |
| time_utc | string |  | 0.0% |  |
| year | string |  | 0.0% |  |
| month | string |  | 0.0% |  |
| latitude | string |  | 0.0% |  |
| longitude | string |  | 0.0% |  |
| depth_km | string |  | 0.0% |  |
| depth_class | string |  | 0.0% |  |
| magnitude | string |  | 0.0% |  |
| magnitude_type | string |  | 0.0% |  |
| magnitude_class | string |  | 0.0% |  |
| place_description | string |  | 0.0% |  |
| region | string |  | 0.0% |  |
| locality | string |  | 0.0% |  |
| event_type | string |  | 0.0% |  |
| tsunami_flag | string |  | 0.0% |  |
| significance | string |  | 0.0% |  |
| felt_reports | string |  | 0.0% |  |
| community_intensity | string |  | 0.0% |  |
| modified_mercalli_intensity | string |  | 0.0% |  |
| alert_level | string |  | 0.0% |  |
| review_status | string |  | 0.0% |  |
| station_count | string |  | 0.0% |  |
| rms_error | string |  | 0.0% |  |
| azimuthal_gap | string |  | 0.0% |  |
| min_distance_deg | string |  | 0.0% |  |
| data_sources | string |  | 0.0% |  |
| usgs_url | string |  | 0.0% |  |


## Sources
- databazaar.io listing beb243fd-5039-4d81-bedf-2a1af8040c45 — https://databazaar.io/datasets/beb243fd-5039-4d81-bedf-2a1af8040c45 — see listing — retrieved 2026-05-04T19:26:15+00:00

## Methodology
acquire mode v0.2.0; databazaar adapter only in this version

## Known gaps & limitations
v0.2 adapters: databazaar, HuggingFace, World Bank. Other 10 adapters stubbed — see references/sources.md.

## Intended use & out-of-scope
Derived from a databazaar.io listing — see source for original use case.

## Provenance & reproducibility
- Provenance hash: `sha256:b3e7fc9fa9db084334078990da9e1a3e01996c527696ee886feeeea7a50c7a34`
- Skill version: `0.2.0`
- Generated: `2026-05-04T19:26:29+00:00`

---
*Built with the `databazaar` skill. Listed on https://databazaar.io.*
