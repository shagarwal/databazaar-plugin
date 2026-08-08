# Pricing Model

Pricing for proprietary listings is genuinely hard — databazaar's catalog
is mostly free at present, so comp signal is thin. This file documents v0
heuristic + the upgrade path.

## v0: heuristic (confidence: low)

```
base = 1.00 USD
size_factor   = log10(max(rows, 100)) / 2          # 1k rows → 1.5x, 100k → 2.5x
cols_factor   = 1 + (column_count / 50)            # 50 cols → 2x
fresh_factor  = 1.0 if updated < 30d else 0.7      # stale data discounted
unique_factor = 1.0 + uniqueness_score             # 0–1, see below
category_mult = TABLE[category]                    # see below

suggested_price = base * size_factor * cols_factor * fresh_factor
                  * unique_factor * category_mult
```

Round to `[0.99, 1.99, 2.99, 4.99, 9.99, 19.99, 49.99, 99.99]`.

### Uniqueness score (0–1)

Cosine similarity of (tags + schema columns) against existing databazaar
listings. `1 - max_similarity` = uniqueness. If max_similarity > 0.9
(near-duplicate of existing free listing), suggest **free** instead.

### Category multipliers (initial guess; tune from sales data)

| Category | Multiplier | Rationale |
|---|---|---|
| financial | 2.5 | High WTP for trading/investment data |
| healthcare | 2.0 | Specialized buyers, compliance burden |
| pricing | 1.5 | Direct revenue use case |
| real-estate | 1.5 | Investor demand |
| ai-ml | 1.3 | Training data niche |
| scientific | 0.8 | Often free elsewhere |
| social | 0.8 | Often free from World Bank/UN |
| geographic | 0.7 | Public-domain saturation |
| text | 1.0 | |
| sensor | 1.2 | |
| images | 1.0 | |
| (default) | 1.0 | |

### Output

Always emit a confidence score with the suggestion:

```json
{
  "suggested_price_usd": 4.99,
  "confidence": "low",
  "reasoning": "Heuristic only — limited paid comps in catalog. 12k rows, 18 cols, scientific category.",
  "alternatives": [
    {"price": 0, "label": "free (drives traffic)"},
    {"price": 2.99, "label": "low-friction"},
    {"price": 4.99, "label": "heuristic"},
    {"price": 9.99, "label": "premium"}
  ]
}
```

## v1: comp-based (planned)

Once databazaar has ≥50 priced listings:

1. Embed each listing (title + description + tags + schema columns).
2. Find k=5 nearest neighbors of the new dataset.
3. Suggest median price of neighbors.
4. Confidence = `high` if neighbor distances < threshold, else `medium`.

## v2: market-feedback (future)

After listings have view/buy data:

- Boost suggestions for tags/categories with high view→buy conversion.
- Discount oversaturated tags.

## Never do

- Don't suggest prices >$100 without explicit user override (catalog norm
  is sub-$10; high prices kill conversion).
- Don't suggest paid for datasets that are bit-identical to a free listing
  on databazaar or HuggingFace.
- Don't bake pricing logic that requires user PII or financial data to run.
