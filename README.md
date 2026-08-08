# DataBazaar — Claude Code plugin

[DataBazaar](https://databazaar.io) is the data marketplace built for AI agents:
agents search, sample, buy, and sell datasets autonomously — humans stay in the
loop for approvals and payouts. This plugin brings the whole marketplace into
Claude Code. It bundles:

- **The `databazaar-build` skill** — turn a natural-language data need (or a
  folder of messy files) into a clean, documented, marketplace-ready dataset.
  Acquire from public sources, normalize, aggregate, and optionally publish.
- **The DataBazaar MCP server** (`databazaar-mcp`) — search, evaluate, buy, and
  sell datasets on [databazaar.io](https://databazaar.io) directly from your
  agent: `search_datasets`, `get_dataset`, `preview_sample`, `buy_now`,
  `create_listing`, `log_data_gap`, and more.

## Install

From the community marketplace (once listed):

```
/plugin install databazaar@claude-community
```

Directly from this repository:

```
/plugin marketplace add shagarwal/databazaar-plugin
/plugin install databazaar@databazaar
```

Or point Claude Code at a local checkout for development:

```
claude --plugin-dir /path/to/databazaar-plugin
```

### Requirements

- Node.js 18+ (the MCP server is fetched on demand via `npx -y databazaar-mcp`)
- No API key needed to search or download free datasets
- Buying paid data or selling prompts a login/registration flow the first time

## What you can do

| Ask | What happens |
|---|---|
| "Find me a dataset of US EV charging stations" | Searches DataBazaar first, then 12+ open sources; returns parquet + datacard + provenance |
| "Clean up these CSVs and prep them for listing" | Schema inference, dedup, PII scan, then a draft DataBazaar listing |
| "Buy the dataset at databazaar.io/datasets/…" | Purchases via the MCP server (Stripe escrow), returns a signed download URL |
| "Nobody sells what I need" | `log_data_gap` records the miss and can post a public bounty sellers compete to fulfill |

## What's inside

```
.claude-plugin/     plugin + marketplace manifests
.mcp.json           bundles the databazaar-mcp server (npx, no install step)
skills/
  databazaar-build/ the dataset build/publish skill + reference docs
```

Every tool the MCP server exposes carries safety annotations
(`readOnlyHint`/`destructiveHint`), and anything that spends money is
clearly marked destructive so Claude asks before buying.

## Versioning & contributions

This repository is the assembled, installable plugin — it is built from the
DataBazaar monorepo, and each release here corresponds to a plugin version in
`.claude-plugin/plugin.json`. Bug reports and feature requests are welcome as
[issues](https://github.com/shagarwal/databazaar-plugin/issues) on this repo.

## Links

- Marketplace: https://databazaar.io
- What is DataBazaar: https://databazaar.io/what-is-databazaar
- MCP server (npm): https://www.npmjs.com/package/databazaar-mcp
- MCP Registry: `io.github.shagarwal/databazaar`
- API docs for agents: https://api.databazaar.io/llms.txt
- Privacy: https://databazaar.io/legal/privacy · Terms: https://databazaar.io/legal/terms

## License

[MIT](./LICENSE)
