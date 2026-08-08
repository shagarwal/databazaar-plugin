# International Football Match Results (1872–2026)

## Overview
A benchmark dataset of 49,215 international football (soccer) match results spanning over 150 years, from the first official match (Scotland vs England, 1872) through March 2026. Covers 333 national teams across 193 tournaments in every FIFA confederation.

Each record includes: match date, year, decade, month, home and away teams, scores, total goals, goal difference, match result (home win/away win/draw), tournament name, tournament tier classification (Major Tournament, World Cup Qualifier, Continental Qualifier, Continental League, Friendly, Other Competition), venue city and country, neutral venue indicator, FIFA confederation for both teams (UEFA/CONMEBOL/CONCACAF/CAF/AFC/OFC), inter- vs intra-confederation match type, and penalty shootout indicator.

20 columns across 49,215 rows. Sourced from publicly available international football records, enriched with confederation mappings, tournament tier classifications, and computed analytics fields. Ideal for sports analytics, historical trend analysis, prediction modeling, and FIFA ranking research.

- Rows: 49,215
- Columns: 20
- Format: csv (parquet available)
- Generated: 2026-05-04T19:27:00+00:00

## Schema
| Column | Type | Description | Null % | Examples |
|---|---|---|---|---|
| date | string |  | 0.0% |  |
| year | string |  | 0.0% |  |
| decade | string |  | 0.0% |  |
| month | string |  | 0.0% |  |
| home_team | string |  | 0.0% |  |
| away_team | string |  | 0.0% |  |
| home_score | string |  | 0.0% |  |
| away_score | string |  | 0.0% |  |
| total_goals | string |  | 0.0% |  |
| goal_difference | string |  | 0.0% |  |
| result | string |  | 0.0% |  |
| tournament | string |  | 0.0% |  |
| tournament_tier | string |  | 0.0% |  |
| city | string |  | 0.0% |  |
| country | string |  | 0.0% |  |
| neutral_venue | string |  | 0.0% |  |
| home_confederation | string |  | 0.0% |  |
| away_confederation | string |  | 0.0% |  |
| match_type | string |  | 0.0% |  |
| penalty_shootout | string |  | 0.0% |  |


## Sources
- databazaar.io listing e9f0cefb-7269-4468-a779-f9cb047fc75c — https://databazaar.io/datasets/e9f0cefb-7269-4468-a779-f9cb047fc75c — see listing — retrieved 2026-05-04T19:26:58+00:00

## Methodology
acquire mode v0.2.0; databazaar adapter only in this version

## Known gaps & limitations
v0.2 adapters: databazaar, HuggingFace, World Bank. Other 10 adapters stubbed — see references/sources.md.

## Intended use & out-of-scope
Derived from a databazaar.io listing — see source for original use case.

## Provenance & reproducibility
- Provenance hash: `sha256:10508b6c95752a5b9eaddb4ea0786c1feb234f76844d8209bf436c0af2163284`
- Skill version: `0.2.0`
- Generated: `2026-05-04T19:27:00+00:00`

---
*Built with the `databazaar` skill. Listed on https://databazaar.io.*
