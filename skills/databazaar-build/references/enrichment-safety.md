# Enrichment Safety

When `enrich` mode joins proprietary data against public sources, the join
itself can leak proprietary information. This file defines the guardrails.

## The leak vector

Naive enrichment:

```python
for row in proprietary_df:
    public_data = wikidata.lookup(row["company_name"])  # LEAK
    row.update(public_data)
```

The leak: `wikidata.lookup` (or any external API call) sends the proprietary
join key to a third party. Over thousands of rows, the third party can
reconstruct the proprietary entity list — which IS the proprietary asset.

## Required pattern

1. **Hash join keys client-side before any public lookup.**
2. **Batch + shuffle queries** so request order doesn't leak row order.
3. **Add decoy queries** when the proprietary list is small (< 1000 rows) —
   ratio configurable, default 2x decoys from a public reference list.
4. **Cache locally** — never re-query the same key.
5. **Audit log** every external call to `provenance.json` with the hash, not
   the cleartext key.

## Allowed enrichment sources

Public sources only. The skill must reject enrichment requests against:

- Any source requiring auth (defeats the purpose; auth-walled sources can log queries).
- Databazaar listings owned by other sellers (would leak the user's interest
  in their data to the platform).

## Approved enrichment fields

By category — these are safe to look up because they are commodity public facts:

- **Companies:** ticker, country of HQ, industry code (NAICS/SIC), founding year, employee count band.
- **Cities:** ISO code, country, lat/lon, population band, timezone.
- **Countries:** ISO codes, region, currency, official languages.
- **Products (UPC/EAN):** generic category, manufacturer.

## Forbidden enrichment fields

- Anything that would let the public source infer *why* the user is asking
  (e.g., a property valuation lookup against a proprietary customer list
  reveals the customer is a high-net-worth segment).
- Personally identifiable enrichment of any kind (no email lookup, no
  address-to-person joins).

## Audit log entry

```json
{
  "timestamp": "ISO",
  "source": "wikidata",
  "field_added": "founding_year",
  "key_hash": "sha256:...",
  "decoy_ratio": 2.0,
  "cached": false
}
```

## When in doubt

Refuse enrichment, do `acquire` separately, and tell the user to join locally.
That's the leak-free path.
