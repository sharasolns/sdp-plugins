---
name: sdp-website-builder
description: Build, compose, inspect, or safely edit SDP CMS websites through the SDP/Arawa Website Builder MCP. Use for component schemas and data, Latte/SCSS source, page or template composition, component version switching, validation, publishing, and custom domain or sm.ke connectivity. Do not use for unrelated generic frontend repositories.
---

# SDP Website Builder

This plugin connects to Website Manager MCP (`/mcp/website-manager`). Use directly listed tools when available. Discover other tools with `search_tools`, then call `execute_tools` with the exact names and arguments returned by search. Do not assume workflow tool names are directly exposed. Follow the live server instructions and tool schemas when they differ from this source snapshot.

This file is generated from `WebsiteBuilderInstructionCatalog`. Edit the catalog, then run `php artisan mcp:export-instructions`.

Start with one `get_website_builder_instructions` call or read `sdp://instructions`. Pass only the task skills needed; combine related skills in the same call.

For component creation, always define at least one editable field and reference a declared field from Latte markup. Model editable copy, media, links, and repeated content as semantic fields instead of hard-coding the entire component.

- `website.create` (`/mcp/website-manager`): Create a website and establish its reusable visual foundation.
- `website.settings` (`/mcp/website-manager`): Read or partially update website identity and media settings.
- `website.domain` (`/mcp/website-manager`): Connect a custom domain or free sm.ke subdomain and verify DNS.
- `component.create` (`/mcp/website-manager`): Create one reusable Latte component with the correct schema, source, and styling.
- `component.update` (`/mcp/website-manager`): Safely update component Latte, SCSS, data, or a page-local placement.
- `component.fields` (`/mcp/website-manager`): Add, override, soft-remove, or restore fields on one component instance.
- `component.version` (`/mcp/website-manager`): Switch the reusable version behind an existing page placement without deleting it.
- `page.compose` (`/mcp/website-manager`): Compose a page from reusable component placements while preserving template ownership.
- `template.build` (`/mcp/website-manager`): Create or update the minimal template family and shared shell.
- `global_code.update` (`/mcp/website-manager`): Safely update global CSS, header scripts, footer scripts, or robots.txt.
- `media.upload` (`/mcp/website-manager`): Import public media or upload a local image/video without placing binary data in MCP calls.
- `runtime.posts` (`/mcp/website-manager`): Render post lists, categories, or one post with supported Latte runtime data.
- `runtime.catalog` (`/mcp/website-manager`): Render ecommerce, listing, course, taxonomy, archive, or custom-order runtime content.
- `content.publish` (`/mcp/website-manager`): Review lifecycle state and publish website, page, or post changes safely.
- `seo.read` (`/mcp/website-manager`): Read stored Google Search Console analysis without triggering refreshes.
- `planner.manage` (`/mcp/website-manager`): Create and manage content plans, assignments, categories, groups, and reminders.
- `image_template.build` (`/mcp/website-manager`): Design a reusable SDP image template, then render featured/OG images from it.
- `company.switch` (`/mcp/website-manager`): Select the company membership used by subsequent MCP and dashboard requests.

Then call `get_website_build_context` only when the selected workflow needs website-specific data, passing the smallest relevant `include` list.

Hard invariants live in the MCP server instructions. Task detail lives in the catalog, `sdp://instructions/{skill}`, and [references/workflows.md](references/workflows.md). Component source, fields, and version switching are also summarized in [references/components.md](references/components.md).
