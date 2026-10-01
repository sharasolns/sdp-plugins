# Changelog

## 0.1.9 - 2026-10-01

- Regenerate Website Builder instructions from the current backend catalog.
- Bundle source-exported catalog references and document catalog image attachment, listing variants, and read-only course quiz results.
- Add a repeatable instruction sync command with drift checking.

## 0.1.8 - 2026-09-10

- Rename the plugin: id `sdp` -> `sdp-platform`, display name "SDP Platform". Install as `sdp-platform@sdp` (Claude/Codex), `sdp-platform` (Grok); skills namespace to `/sdp-platform:...`. Switch the contact email to `info@sdp-platform.com`.
- website-builder: new `clone_page` tool; `get_page` gains `include_data` for lighter payloads; `replace_page_composition` / `replace_template_composition` gain `dry_run`; `create_website_component` returns the resolved `component_type`. Instruction docs now cover archive-as-delete, content-plan auto-publish, and the `field_meta` shape. Regenerated `sdp-website-builder` reference docs.

## 0.1.7 - 2026-09-10

- website-builder: `replace_page_composition` and `replace_template_composition` now accept a flat `components` array (`{component_id, data?, field_meta?}`); `sections` is optional and only needed when a template owns more than one section. Regenerated `sdp-website-builder` workflow docs with the new guidance and examples.

## 0.1.6 - 2026-09-10

- Correct `privacyPolicyURL` and `termsOfServiceURL` in the Codex manifest; both pointed at 404 paths. The live pages are `/privacy-policy` and `/terms-and-conditions`.

## 0.1.5 - 2026-09-10

- Correct the `repository` URL in the Claude, Cursor, Codex, and Open Plugins manifests; it pointed at a non-existent `sdp-platforms/sdp-plugins`.
- Add a root `SETUP.md` covering account prerequisites, per-server OAuth, company context, and troubleshooting.

## 0.1.4 - 2026-09-09

- Require every MCP-created website component to define an editable field and reference a declared field from its Latte markup.
- Tell agents to model editable copy, media, links, and repeated content as semantic fields instead of hard-coding entire components.

## 0.1.3 - 2026-09-04

- Add the hosted Courses Administration MCP and `sdp-courses` skill.
- Document course authoring, media, curriculum, quiz, final-test, and Website Builder routing boundaries.
- Synchronize generated Website Builder workflow guidance with the backend instruction catalog.

## 0.1.2 - 2026-09-01

- Use the SDP Platform logo in plugin manifests and the README.

## 0.1.1 - 2026-09-01

- Tell users to create an SDP account at https://sdp-platform.com before OAuth.

## 0.1.0 - 2026-09-01

- Initial plugin package for Codex, Claude Code, Cursor, and Open Plugins.
- Hosted MCP servers: website-builder, products, listings, custom-forms.
- Skills: sdp-website-builder, sdp-products, sdp-listings, sdp-custom-forms.
