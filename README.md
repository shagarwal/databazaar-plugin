# DataBazaar — marketplace skill and Claude Code plugin

Search datasets, inspect samples, retrieve data, and prepare seller submissions
with [DataBazaar](https://databazaar.io). Public discovery needs no account.
Full retrieval requires an account, including free datasets; paid data also
requires purchase access.

## Install the marketplace skill

The [marketplace skill](skills/databazaar-marketplace/SKILL.md) works with agents
that support the open Agent Skills format. From your project directory:

```bash
npx skills add shagarwal/databazaar-plugin --skill databazaar-marketplace
```

Choose your agent when prompted. To target Codex or Claude Code explicitly:

```bash
npx skills add shagarwal/databazaar-plugin --skill databazaar-marketplace --agent codex
npx skills add shagarwal/databazaar-plugin --skill databazaar-marketplace --agent claude-code
```

The current `skills` CLI requires Node.js 22.20+. This installs instructions,
not an MCP connection or account credential. The skill can use REST directly,
an existing DataBazaar MCP connection, or the connection options below.

Try: “Find DeepSearchQA on DataBazaar, inspect its sample, and tell me whether
its schema fits benchmark evaluation. Don't retrieve or buy anything yet.”
Then, with account access: “Export the complete free DeepSearchQA dataset to CSV
and verify its fields and row count.”

## Claude Code plugin with MCP

```text
/plugin marketplace add shagarwal/databazaar-plugin
/plugin install databazaar@databazaar
```

The plugin bundles the skills and `databazaar-mcp@1.5.1` (Node.js 20+).
Search and sample previews work without credentials. For account operations:

```bash
npx -y databazaar-mcp@1.5.1 auth login
```

Complete authorization in your browser. Alternatively, use an account API key
from [Account → API Keys](https://databazaar.io/operator/keys) as documented in
the [MCP setup guide](https://github.com/shagarwal/databazaar-mcp).

Remote MCP endpoints:

- Public search, listing details, samples: `https://api.databazaar.io/mcp/public`
- Account operations with OAuth: `https://api.databazaar.io/mcp`

## Workflows

| Need | What to do |
|---|---|
| Find data | Compare schema, coverage, source, license and sample before retrieving. |
| Retrieve free data | Sign in, obtain access, fetch actual bytes, and verify the result. |
| Buy data | Inspect current price and existing access; purchase only within the user's authorization. |
| Sell your data | Prepare files and provenance, create a draft, upload, and publish with applicable terms accepted. |
| Fulfill a bounty | Check requirements, deadline and award conditions; submit matching original work. |

[Tested DeepSearchQA CSV and n8n export](https://databazaar.io/guides/deepsearchqa-csv)
· [Browse bounties](https://databazaar.io/bounties)
· [List a dataset](https://databazaar.io/sell)

## Included skills

- **databazaar-marketplace:** current marketplace access workflow; recommended
  for discovery, retrieval, purchases and seller/bounty tasks.
- **databazaar-build:** earlier local data preparation toolkit. Its standalone
  DataBazaar acquisition adapter does not support current account-authenticated
  full retrieval. Use the marketplace skill for that path. Some build modes are
  experimental; see its [mode status](skills/databazaar-build/README.md).

MCP annotations describe tool behavior; they do not enforce spending approval.
The calling agent must respect the user's authorization and budget.

## References and contributions

- [Current API guide](https://api.databazaar.io/llms.txt)
- [REST schemas](https://api.databazaar.io/openapi.json)
- [Issues](https://github.com/shagarwal/databazaar-plugin/issues)
- [Privacy](https://databazaar.io/legal/privacy) · [Terms](https://databazaar.io/legal/terms)

[MIT license](LICENSE).
