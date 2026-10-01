---
name: sdp-setup
description: Set up and connect the SDP plugin. Use when the SDP plugin was just installed, when any SDP MCP server fails to authenticate, when a tool returns an authentication or authorization error, or when the user asks how to connect, sign in to, or configure SDP.
---

# SDP Setup

This plugin has no API keys and no environment variables. Every SDP MCP server authenticates through browser OAuth against the user's own SDP account. Setup is therefore two things: make sure the account exists, then complete OAuth once per server.

## 1. Confirm the user has an SDP account

OAuth cannot succeed without one. Ask the user whether they already have an account at https://sdp-platform.com.

If they do not, send them there to sign up before going further. Their password must be at least 12 characters and include an uppercase letter, a lowercase letter, a number, and a symbol.

Never invent, request, or accept a pasted API key. There is no key-based path.

## 2. Connect the MCP servers

The plugin bundles five hosted HTTP MCP servers:

| Server | Purpose |
| --- | --- |
| `sdp-website-builder` | Latte components, pages, templates, publishing, domains |
| `sdp-products` | Product catalog, variants, media |
| `sdp-listings` | Listing catalog, brands, collections, media |
| `sdp-courses` | Course authoring, curricula, quizzes, media |
| `sdp-custom-forms` | Custom order types, fields, pricing items |

Each is authorized separately, on first use. Tell the user to expect a browser window per server and to approve the SDP consent screen there.

Start a fresh session after installing the plugin. The servers are registered at session start, so a session that was already running will not see them.

To verify a connection, call `list_companies` on the relevant server. A successful response means that server is connected. Do not treat a successful `list_companies` on one server as evidence that the others are authorized.

## 3. Establish the company context

Catalog data tools require an explicit numeric `company_id`; discovery and dashboard tools may omit it according to their schemas. Website Builder uses company selection via `switch_company` and website targeting according to the selected workflow.

Call `list_companies` first and confirm which company the user means before any read or write. If they own exactly one company, use it and say which one you picked. If they own several, ask. Never guess a `company_id`, and never carry one over from an unrelated conversation.

## 4. Read the hosted instructions before writing anything

Each server publishes its own authoritative instruction resource. Read the one for the server you are about to use before creating or mutating records:

- `sdp://instructions` (or one `get_website_builder_instructions` call) for Website Builder
- `sdp://products/instructions`
- `sdp://listings/instructions`
- `sdp://courses/instructions`
- `sdp://custom-forms/instructions`

These describe current tool names, required fields, and lifecycle rules. They take precedence over anything cached in this plugin's skills.

## Troubleshooting

**The SDP tools are not available at all.** The plugin was installed into a session that was already open. Start a new session.

**OAuth fails or loops.** The user most likely has no SDP account yet, or is signed into a different one in that browser. Send them to https://sdp-platform.com to sign in, then retry the tool call.

**A tool returns an authorization error while other SDP tools work.** That specific server has not been authorized yet. Trigger any tool on it and complete the OAuth prompt.

**A tool rejects `company_id`.** The user does not have access to that company, or the id came from a stale context. Re-run `list_companies`.

**An id, slug, or type is not found.** Do not invent replacements. Re-read the relevant `sdp://.../instructions` resource and list the parent records to get real ids.
