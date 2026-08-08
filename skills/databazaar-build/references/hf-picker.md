# HuggingFace Parquet Picker

Canonical logic for "given an HF dataset id, what slice do I actually
fetch?" Carried over from the `databazaar-discovery` skill's import CLI
(`apps/api/src/cli/import-from-source.ts` in the agentdatamarketplace repo).
Discovery learned this the hard way; the build skill should not rediscover
it.

Reference TypeScript implementation:
[`apps/api/src/cli/import-from-source.ts`](https://github.com/shagarwal/agentdatamarketplace/blob/main/apps/api/src/cli/import-from-source.ts)
— in particular `fetchHfParquetFiles`, `decideImportMode`,
`pickParquetFile`, `fetchHfDatasetRowCount`.

## What HF gives you

`GET https://datasets-server.huggingface.co/parquet?dataset=<id>` returns:

```json
{
  "parquet_files": [
    { "dataset": "...", "config": "default", "split": "train",
      "url": "https://huggingface.co/.../0000.parquet",
      "filename": "0000.parquet", "size": 117323050 },
    ...
  ]
}
```

Datasets are partitioned by **(config, split, shard)**. Multilingual
datasets put each language in its own config (~300 configs for Cohere's
multilingual Wikipedia). Pretraining-scale corpora put each shard in its
own file (5,314 shards for MegaMath at 80–1500 MB each).

If `parquet_files` is empty or the response is non-200, the dataset is
either gated, lacks parquet output (raw archives only), or HF is rate-
limiting. Surface a "no parquet files (gated dataset, no parquet, or HF
API error)" error and let the operator decide. Do NOT fall back to
scraping the dataset card.

## The two failure modes that motivate this picker

1. **Pick smallest naively** → for multilingual or multi-shard datasets,
   the smallest file is one minor language or one of thousands of shards.
   The mirror has 41 rows of Crimean Tatar Wikipedia, listing claims 250M.
   Buyers spot the lie immediately.

2. **Mirror everything** → MegaMath is 1.04 TB. Wikipedia-multilingual is
   499 GB. Even one config (English Wikipedia) is 84 GB. Storage cost
   scales with inventory.

Discovery's resolution was federation: store source URLs, stream-through
on download. The build skill's analogue depends on what the caller wants:

| Caller goal | Picker rule |
|---|---|
| User said "I just want a quick look at MegaMath" | Mirror smallest single shard. Note in the datacard's "Known gaps" that this is one shard of N. |
| User said "build me a dataset of math text from MegaMath, ≥1 GB" | Iterate shards until cap reached. Concatenate locally. Provenance per shard. |
| User said "give me everything in a HF dataset" and total > local-disk-cap | Refuse with a clear "1 TB > available cap" error; suggest the federated databazaar.io listing as the canonical access layer. |

## Row count is a separate API call

Do NOT compute total rows by reading parquet metadata across all shards.
DuckDB's `count(*)` on `read_parquet([url1, url2, ...])` works on small
manifests and breaks at thousands of shards with `INTERNAL Error:
Information loss on integer cast`. Use HuggingFace's `/size` endpoint:

```
GET https://datasets-server.huggingface.co/size?dataset=<id>
→ { "size": { "dataset": { "num_rows": 217499877, ... } } }
```

Cheap, exact, won't crash. The build skill's huggingface adapter should
populate `schema.row_count` from this endpoint, not from parquet footer
sums.

## Picker pseudocode

```python
def pick_hf_files(hf_id, intent: Literal["preview", "build", "everything"], cap_bytes):
    files = fetch_hf_parquet_files(hf_id)  # list of {url, config, split, filename, size}
    if not files:
        raise NoParquetError(hf_id)
    total = sum(f.size for f in files)
    total_rows = fetch_hf_dataset_row_count(hf_id)  # /size endpoint

    if intent == "preview":
        # one shard; smallest gives quickest fetch
        return [smallest(files)], total_rows

    if intent == "everything":
        if total > cap_bytes:
            raise OversizeError(total, cap_bytes,
                                hint="use databazaar.io federated listing for query access")
        return files, total_rows

    # intent == "build" — fill up to cap with same-config shards
    # (cross-config schemas may differ, so don't mix configs)
    by_config = group_by(files, "config")
    chosen_config = max(by_config.keys(), key=lambda k: sum(f.size for f in by_config[k]))
    selected, running = [], 0
    for f in sorted(by_config[chosen_config], key=lambda f: f.size):
        if running + f.size > cap_bytes:
            break
        selected.append(f)
        running += f.size
    if not selected:
        # smallest single file already over cap
        raise OversizeError(by_config[chosen_config][0].size, cap_bytes)
    return selected, total_rows
```

## Schema consistency across shards

Within one config, shards share a schema. Across configs, schemas are
*usually* the same but not guaranteed. If your picker spans configs, run a
schema-equality check on the parquet footers before concatenating; if they
differ, refuse to merge and tell the caller which configs are incompatible.

## Gated datasets

Some HF datasets (`lmsys/lmsys-chat-1m`, etc.) require ToS click-through
before the parquet API serves them. The `/parquet` endpoint returns 0 files
for these without an obvious error. If `parquet_files` is empty AND the
dataset card lists a license/ToS gate, surface "gated dataset, manual
acceptance required" rather than a generic "no parquet" message.

## Reachability semantics

The actual parquet shard URLs occasionally 429 under load. Apply the
reachability rule from `gotchas.md`: treat 429 / 503 as **ambiguous**
(transient), not a permanent failure. Retry with exponential backoff up to
3 times before giving up. Discovery's pipeline once demoted 787 candidates
to "unreachable" because its initial reachability check treated 429 as
dead.
