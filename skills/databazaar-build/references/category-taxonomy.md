# DataBazaar Category Taxonomy

Pulled from the live catalog at `GET https://api.databazaar.io/datasets`
(snapshot 2026-05-04). The skill auto-suggests one of these for new listings.

## Categories observed in catalog

| Category | Example listings | Typical row count |
|---|---|---|
| `financial` | Sovereign debt, employment stats, dev indicators, BTC prices, crypto regulation | 10k-90k |
| `pricing` | Aircraft listings, food prices, CPI, inflation | 60-90k |
| `scientific` | Earthquakes, exoplanets, energy, indices (cyber, AI reg, education, EV) | 40-100k |
| `social` | Tourism, labor, gender, education, WASH, demographics | 10k-15k |
| `geographic` | Country profiles, world cities, flight routes, US counties, neighborhoods | 30-66k |
| `healthcare` | Healthcare infra, disease burden, expenditure | 10k-12k |
| `energy` | Energy & emissions panels | 11k |
| `images` | Museum artworks, historical photos | 10k-15k |
| `sensor` | Weather stations, air quality, daily climate | 18k-125k |
| `text` | Public domain books, English vocab, dad jokes | 100-75k |
| `food-beverage` | Crop production, staple food prices | 24k-575k |
| `real-estate` | Property indices | 16k-35k |
| `transportation` | Logistics & infrastructure | 12k |
| `retail` | FDA recalls, digital commerce readiness | 11k-45k |
| `education` | Education & literacy panels | 10k |
| `sports` | International football results | 49k |
| `ai-ml` | HuggingFace model directory | 12k |
| `other` | HN jobs, dog-friendly venues | varies |

## Auto-suggestion logic

1. Tag-based: if tags overlap with a category's prototypical tag set ≥3 → suggest that category.
2. Schema-based: if column names match patterns (e.g., `country` + `year` + `value` → country panel → likely `social`/`financial`/`scientific` based on indicator name).
3. Title NER: extract domain entities, map to category.
4. Fallback: `other` (and flag for human review).

## Common tag clusters (top 30 by frequency)

`world-bank`, `global`, `country-level`, `panel-data`, `time-series`, `economics`,
`development`, `gdp`, `health`, `climate`, `population`, `demographics`, `WHO`,
`united-states`, `2024`, `2025`, `historical`, `usgs`, `noaa`, `csv`, `public-domain`,
`reference`, `aviation`, `agriculture`, `energy`, `sustainability`, `cities`,
`real-estate`, `world-bank`, `pricing`.

The skill should bias toward existing tags rather than inventing new ones —
discovery is better when tags overlap.

## When to propose a new category

If <5 existing listings would fit and the dataset is structurally different
from existing categories: propose a new category in `listing_suggestion.json`
with `proposed: true` and require user confirmation.
