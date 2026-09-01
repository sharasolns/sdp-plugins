# Repository Guidance

Maintain this repository as one SDP plugin with native Codex, Claude Code, and Cursor packaging plus the vendor-neutral Open Plugins manifest.

## Sources of truth

1. Hosted SDP MCP runtimes for tool names, OAuth, and instruction resources.
2. `sdp-cms-backend` `WebsiteBuilderInstructionCatalog` for website-builder skill prose. Copy exported files; do not rewrite them here.
3. `sdp://products/instructions`, `sdp://listings/instructions`, and `sdp://custom-forms/instructions` for catalog workflows.

When sources disagree, verify the hosted interface and document the discrepancy.

## Scope and structure

- Keep bundled skills focused on website builder, products, listings, and custom forms.
- Keep each `SKILL.md` concise. Put generated website-builder detail in `references/`.
- Use only `name` and `description` in shared `SKILL.md` frontmatter.
- Keep `agents/openai.yaml` synchronized with its skill. Declare MCP dependencies for every skill that calls MCP tools.
- Keep all plugin manifest versions synchronized and update `CHANGELOG.md` with each release.

## Safety

- Never put credentials, customer data, or live catalog dumps in this repository.
- Do not invent catalog ids or type slugs.
- Automated validation must not publish websites or mutate production catalogs.

## Working in Claude Code

Claude Code reads `CLAUDE.md`, not `AGENTS.md`. To auto-load this guidance there, run `ln -s AGENTS.md CLAUDE.md` locally; the symlink is gitignored.

## Validation

```bash
python3 scripts/validate_repo.py
```
