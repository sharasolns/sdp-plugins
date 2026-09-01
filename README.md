# SDP Plugin

Official SDP plugin for Codex, Claude Code, Cursor, Grok Bot, and other Agent Plugin clients. It connects coding agents to hosted SDP MCP servers for websites, products, listings, and custom-order types.

Shared Agent Skills stay portable. Each client uses its native manifest. MCP tools and OAuth live on SDP hosts, not in this repository.

## Included skills

- `sdp-website-builder` — compose Latte components, pages, templates, and publish
- `sdp-products` — product catalog CRUD and images
- `sdp-listings` — listing catalog CRUD and images
- `sdp-custom-forms` — custom order types, fields, and pricing items

Task detail for website builder lives in [skills/sdp-website-builder/references/workflows.md](skills/sdp-website-builder/references/workflows.md). Catalog skills defer to `sdp://products/instructions`, `sdp://listings/instructions`, and `sdp://custom-forms/instructions`.

## Installation

### Codex

```bash
codex plugin marketplace add /Users/iankibet/www/back-end/sdp-plugins
codex plugin add sdp@sdp
```

Start a new Codex session after installation. Authenticate each MCP server through OAuth when prompted.

### Claude Code

```text
/plugin marketplace add /Users/iankibet/www/back-end/sdp-plugins
/plugin install sdp@sdp
```

Start a new session and complete OAuth on first use. Plugin skills are namespaced, for example `/sdp:sdp-website-builder`.

### Grok Build

Submit/install via the [Grok Build Plugin Marketplace](https://github.com/xai-org/plugin-marketplace). After it is listed:

```bash
grok plugin install sdp --trust
```

### Cursor / Grok Bot

Clone or symlink this folder into Cursor's local plugin directory:

```bash
mkdir -p ~/.cursor/plugins/local
ln -s /Users/iankibet/www/back-end/sdp-plugins ~/.cursor/plugins/local/sdp
```

Reload Cursor or Grok Bot. Complete the SDP OAuth browser sign-in when each MCP server first connects.

### Claude.ai / ChatGPT Developer mode

Add these Streamable HTTP URLs as remote MCP connectors:

```text
https://sdp-api.sdp-platform.com/mcp/website-builder
https://themes-production.sdp-platform.com/mcp/products
https://themes-production.sdp-platform.com/mcp/listings
https://themes-production.sdp-platform.com/mcp/custom-forms
```

## Authentication

| Surface | Default | API key required |
| --- | --- | --- |
| Codex | Hosted MCP with OAuth | No |
| Claude Code | Hosted MCP with OAuth | No |
| Cursor / Grok Bot | Hosted MCP with OAuth | No |
| Claude.ai / ChatGPT | Hosted MCP with OAuth | No |

Do not put credentials in this repository.

## Safety

- Never invent product ids, listing slugs, custom order type slugs, or pricing item ids.
- Never send base64 media through MCP.
- Publish website, page, or post changes only after review.
- Catalog MCP does not operate carts, checkout, inquiries, or storefront HTML.

## Development

```bash
python3 scripts/validate_repo.py
```

Website-builder skill prose is generated in `sdp-cms-backend` with `php artisan mcp:export-instructions`. Copy the exported files into `skills/sdp-website-builder/` when the catalog changes.

## License

MIT
