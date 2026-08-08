# Labor Market & Workforce Statistics — 217 Countries (1960–2024)

## Overview
High-quality panel dataset covering labor market indicators for 217 countries and territories from 1960 to 2024. Includes 14,105 observations across 29 variables: unemployment rates (total, youth, male, female), labor force participation rates by gender, employment distribution across agriculture, industry, and services sectors, vulnerable and self-employment shares, GDP per employed person (2017 PPP), wage/salaried worker proportions, and working-age population demographics.

Data is sourced from the World Bank World Development Indicators, which aggregates ILO modeled estimates, national labor force surveys, and official statistical agencies. Core labor indicators have strongest coverage from 1991–2024 (ILO modeled estimates era), while demographic indicators (GDP per capita, working-age population) extend back to 1960.

Ideal for: labor economics research, cross-country employment comparisons, gender gap analysis in workforce participation, structural transformation studies (agriculture→services transitions), development economics, and policy impact evaluation.

- Rows: 14,105
- Columns: 29
- Format: csv (parquet available)
- Generated: 2026-05-04T19:27:36+00:00

## Schema
| Column | Type | Description | Null % | Examples |
|---|---|---|---|---|
| country_code_iso3 | string |  | 0.0% |  |
| country_code_iso2 | string |  | 0.0% |  |
| country_name | string |  | 0.0% |  |
| region | string |  | 0.0% |  |
| income_level | string |  | 0.0% |  |
| year | string |  | 0.0% |  |
| unemployment_rate_pct | string |  | 0.0% |  |
| labor_force_participation_rate_pct | string |  | 0.0% |  |
| youth_unemployment_rate_pct | string |  | 0.0% |  |
| total_labor_force | string |  | 0.0% |  |
| employment_agriculture_pct | string |  | 0.0% |  |
| employment_industry_pct | string |  | 0.0% |  |
| employment_services_pct | string |  | 0.0% |  |
| female_unemployment_rate_pct | string |  | 0.0% |  |
| male_unemployment_rate_pct | string |  | 0.0% |  |
| female_labor_participation_pct | string |  | 0.0% |  |
| male_labor_participation_pct | string |  | 0.0% |  |
| vulnerable_employment_pct | string |  | 0.0% |  |
| gdp_per_employed_person_2017ppp | string |  | 0.0% |  |
| self_employed_pct | string |  | 0.0% |  |
| youth_female_unemployment_pct | string |  | 0.0% |  |
| youth_male_unemployment_pct | string |  | 0.0% |  |
| labor_force_participation_15plus_pct | string |  | 0.0% |  |
| wage_and_salaried_workers_pct | string |  | 0.0% |  |
| contributing_family_workers_pct | string |  | 0.0% |  |
| employers_pct_of_employment | string |  | 0.0% |  |
| female_labor_force_pct | string |  | 0.0% |  |
| gdp_per_capita_constant_2015usd | string |  | 0.0% |  |
| working_age_population_pct | string |  | 0.0% |  |


## Sources
- databazaar.io listing a40821fa-425d-4708-8a5d-bfa6838c2d61 — https://databazaar.io/datasets/a40821fa-425d-4708-8a5d-bfa6838c2d61 — see listing — retrieved 2026-05-04T19:27:34+00:00

## Methodology
acquire mode v0.2.0; databazaar adapter only in this version

## Known gaps & limitations
v0.2 adapters: databazaar, HuggingFace, World Bank. Other 10 adapters stubbed — see references/sources.md.

## Intended use & out-of-scope
Derived from a databazaar.io listing — see source for original use case.

## Provenance & reproducibility
- Provenance hash: `sha256:ff907a914d2cba2858103e80f6d66ca7e80ea53409810ef3c5e0579f09192390`
- Skill version: `0.2.0`
- Generated: `2026-05-04T19:27:36+00:00`

---
*Built with the `databazaar` skill. Listed on https://databazaar.io.*
