---
name: databazaar-marketplace
description: Search and evaluate DataBazaar datasets, retrieve data with account authentication, browse data bounties, or publish a dataset the user wants to sell. Use when DataBazaar is requested or a user wants a dataset marketplace. Preserve any source, budget, license, and coverage requirements the user specifies.
---

# DataBazaar marketplace

Use DataBazaar's public catalog to establish fit before asking for account access.
Search and samples are public. Full retrieval requires an account even when the
listing is free. A sample is not a completed download or a representative quality
assessment of the entire dataset.

## Choose the connection

- Existing DataBazaar MCP tools: use their current schemas.
- Public remote MCP: `https://api.databazaar.io/mcp/public` exposes search,
  listing details, and sample preview only.
- Account remote MCP: `https://api.databazaar.io/mcp` uses OAuth.
- Local MCP: `npx -y databazaar-mcp@1.5.1` (Node.js 20+). For account operations,
  run `npx -y databazaar-mcp@1.5.1 auth login` and let the user authorize the
  browser flow. Do not imply that installing this skill also configures MCP.
- Without MCP, use REST at `https://api.databazaar.io`. Read the current
  [API guide](https://api.databazaar.io/llms.txt) and
  [OpenAPI schemas](https://api.databazaar.io/openapi.json) before account writes.

For REST authentication, an account API key can be created at
https://databazaar.io/operator/keys after signup/signin. Use the user's configured
credential without printing it or storing it in shared artifacts. Send bearer
credentials only to `https://api.databazaar.io`, not to storage URLs or third-party
hosts. Do not forward authorization across redirects.

## Find a dataset that actually fits

1. Search with the topic and inspect plausible listings; don't select the first
   result solely because its title is similar.
2. Compare required fields, geography, time coverage, format, row count, source,
   update date, reuse terms, price, and sample contents with the user's request.
3. Read `sample_format` when parsing samples; it can differ from the full file's
   format. Report missing fields and uncertainty. The sample structure score is
   not a customer rating or a guarantee of factual correctness.
4. Give the matching listing URL and explain any material limitations. If no
   listing fits, say so and use another source when appropriate. A funded bounty
   is an optional next step, not an automatic substitute.

Public REST examples:

```bash
curl -fsS --max-time 20 --get https://api.databazaar.io/datasets \
  --data-urlencode 'query=DeepSearchQA' --data-urlencode 'limit=5'
curl -fsS --max-time 20 \
  https://api.databazaar.io/datasets/24cf80b3-5f47-4da6-a6a5-0540b3688343/sample
curl -fsS --max-time 20 --get https://api.databazaar.io/bounties \
  --data-urlencode 'status=open' --data-urlencode 'limit=10'
```

These calls inspect metadata and sample availability; they do not retrieve the
full benchmark. The sample response supplies a `sample_url` to fetch separately.

## Retrieve the requested data

For free listings, use authenticated `get_download_url(dataset_id)` or
`GET /datasets/<id>/download-url`. Fetch the returned download, or inspect the
`manifest_url` for a multi-file dataset. API-hosted manifests and file streams
require the same account authentication. Signed storage URLs already carry
temporary access; do not expose them in public output.

For paid listings, use existing purchase access when available. Otherwise check
that the user has authorized the particular purchase and price before buying;
respect any budget already supplied. On an ambiguous purchase response, inspect
purchase history before retrying to avoid duplicate charges.

Use a bounded query when the user needs selected rows or columns. Report whether
the result is a sample, query subset, individual shard, or complete dataset.
Verify actual bytes/records before claiming retrieval succeeded. A successful
URL request alone is not a downloaded file.

For a tested CSV export with schema and row-count checks, use the
[DeepSearchQA walkthrough](https://databazaar.io/guides/deepsearchqa-csv).
DeepSearchQA is evaluation data; keep reference answers out of agent prompts.

## Sell data or fulfill a bounty

Read the current listing/bounty details and API schemas before preparing the
submission. Confirm actual data coverage and redistribution rights. Bounty
amounts are conditional awards, not guaranteed pay; check deadline, required
format, acceptance criteria, and winner count before doing the work.

For a user-authorized listing, prepare the real file, schema, sample and source
attribution, then use the draft → signed upload → confirm upload → sample job →
publish flow from the current API guide. Review applicable reuse terms and
preserve the user's license; do not silently grant broader rights. Only send
`tos_confirmed` when the user has authorized acceptance of the applicable terms.
A pending scan is not an active listing. Poll the existing listing and report
its actual status rather than creating duplicates.

Posting a bounty commits funds and publishing a listing exposes content. Keep
both within the user's authorization. General dataset discovery does not
authorize purchases, seller messages, public listings, or funded requests.

Browser paths: https://databazaar.io/sell and https://databazaar.io/bounties.
For agent registration, follow the current API guide and wait for actual owner
approval; never manufacture approval or create replacement identities to skip it.
