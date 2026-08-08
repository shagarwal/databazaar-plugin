# NASA Exoplanet & Planetary Candidate Catalog — 20,933 Objects from NASA, Kepler & TESS (1992–2025)

## Overview
Harmonized catalog of 20,933 exoplanetary objects combining three authoritative NASA sources: the NASA Exoplanet Archive (6,153 confirmed exoplanets), the Kepler Cumulative KOI Table (6,867 unique Kepler Objects of Interest), and the TESS Objects of Interest catalog (7,913 TOIs). Each record includes 28 normalized fields covering planetary properties (orbital period, radius, mass, equilibrium temperature, eccentricity, insolation flux), host star characteristics (effective temperature, radius, mass, metallicity, surface gravity, spectral type, luminosity), discovery metadata (method, year, facility), sky coordinates (RA/Dec), distance, and system multiplicity. Objects span the full disposition spectrum from confirmed planets through candidates to false positives, enabling classification model training, demographic analysis, and habitability studies. Data sourced from the NASA Exoplanet Science Institute (IPAC/Caltech), Kepler mission pipeline, and TESS Follow-up Observing Program. Deduplicated across catalogs to avoid double-counting confirmed Kepler planets. Suitable for exoplanet population statistics, machine learning classification of planetary candidates, stellar characterization, and habitability zone analysis.

- Rows: 20,933
- Columns: 28
- Format: csv (parquet available)
- Generated: 2026-05-04T19:27:07+00:00

## Schema
| Column | Type | Description | Null % | Examples |
|---|---|---|---|---|
| object_name | string |  | 0.0% |  |
| host_star | string |  | 0.0% |  |
| source_catalog | string |  | 0.0% |  |
| status | string |  | 0.0% |  |
| discovery_method | string |  | 0.0% |  |
| discovery_year | string |  | 0.0% |  |
| discovery_facility | string |  | 0.0% |  |
| orbital_period_days | string |  | 0.0% |  |
| orbital_semi_major_axis_au | string |  | 0.0% |  |
| planet_radius_earth | string |  | 0.0% |  |
| planet_mass_earth | string |  | 0.0% |  |
| equilibrium_temp_k | string |  | 0.0% |  |
| orbital_eccentricity | string |  | 0.0% |  |
| insolation_flux_earth | string |  | 0.0% |  |
| stellar_effective_temp_k | string |  | 0.0% |  |
| stellar_radius_solar | string |  | 0.0% |  |
| stellar_mass_solar | string |  | 0.0% |  |
| stellar_metallicity_dex | string |  | 0.0% |  |
| stellar_surface_gravity_log | string |  | 0.0% |  |
| stellar_spectral_type | string |  | 0.0% |  |
| stellar_luminosity_log_solar | string |  | 0.0% |  |
| distance_pc | string |  | 0.0% |  |
| visual_magnitude | string |  | 0.0% |  |
| ra_deg | string |  | 0.0% |  |
| dec_deg | string |  | 0.0% |  |
| num_stars_in_system | string |  | 0.0% |  |
| num_planets_in_system | string |  | 0.0% |  |
| transit_duration_hours | string |  | 0.0% |  |


## Sources
- databazaar.io listing 3ae48a0c-0e00-4b42-8f9b-90757642a2a9 — https://databazaar.io/datasets/3ae48a0c-0e00-4b42-8f9b-90757642a2a9 — see listing — retrieved 2026-05-04T19:27:06+00:00

## Methodology
acquire mode v0.2.0; databazaar adapter only in this version

## Known gaps & limitations
v0.2 adapters: databazaar, HuggingFace, World Bank. Other 10 adapters stubbed — see references/sources.md.

## Intended use & out-of-scope
Derived from a databazaar.io listing — see source for original use case.

## Provenance & reproducibility
- Provenance hash: `sha256:3621ffc22bfdf579716dd761e0afb0041c465c5630b0980d8b4d902f8f8df7ef`
- Skill version: `0.2.0`
- Generated: `2026-05-04T19:27:07+00:00`

---
*Built with the `databazaar` skill. Listed on https://databazaar.io.*
