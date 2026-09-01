---
name: sdp-website-builder
description: Build, compose, inspect, or safely edit SDP CMS websites through the SDP/Arawa Website Builder MCP. Use for component schemas and data, Latte/SCSS source, page or template composition, component version switching, validation, publishing, and custom domain or sm.ke connectivity. Do not use for unrelated generic frontend repositories.
---

# SDP Website Builder

The user must already have an SDP account at https://sdp-platform.com. If OAuth fails, send them there to sign up or sign in first. Do not invent API keys.

This file is generated from `WebsiteBuilderInstructionCatalog`. Edit the catalog, then run `php artisan mcp:export-instructions`.

Start with one `get_website_builder_instructions` call or read `sdp://instructions`. Pass only the task skills needed; combine related skills in the same call.

- `website.create` (`/mcp/website-builder`): Create a website and establish its reusable visual foundation.
- `website.settings` (`/mcp/website-builder`): Read or partially update website identity and media settings.
- `website.domain` (`/mcp/website-builder`): Connect a custom domain or free sm.ke subdomain and verify DNS.
- `component.create` (`/mcp/website-builder`): Create one reusable Latte component with the correct schema, source, and styling.
- `component.update` (`/mcp/website-builder`): Safely update component Latte, SCSS, data, or a page-local placement.
- `component.fields` (`/mcp/website-builder`): Add, override, soft-remove, or restore fields on one component instance.
- `component.version` (`/mcp/website-builder`): Switch the reusable version behind an existing page placement without deleting it.
- `page.compose` (`/mcp/website-builder`): Compose a page from reusable component placements while preserving template ownership.
- `template.build` (`/mcp/website-builder`): Create or update the minimal template family and shared shell.
- `global_code.update` (`/mcp/website-builder`): Safely update global CSS, header scripts, footer scripts, or robots.txt.
- `media.upload` (`/mcp/website-builder`): Import public media or upload a local image/video without placing binary data in MCP calls.
- `runtime.posts` (`/mcp/website-builder`): Render post lists, categories, or one post with supported Latte runtime data.
- `runtime.catalog` (`/mcp/website-builder`): Render ecommerce, listing, course, taxonomy, archive, or custom-order runtime content.
- `content.publish` (`/mcp/website-builder`): Review lifecycle state and publish website, page, or post changes safely.
- `seo.read` (`/mcp/website-builder`): Read stored Google Search Console analysis without triggering refreshes.
- `planner.manage` (`/mcp/website-builder`): Create and manage content plans, assignments, categories, groups, and reminders.
- `image_template.build` (`/mcp/website-builder`): Design a reusable SDP image template, then render featured/OG images from it.
- `company.switch` (`/mcp/website-builder`): Select the company membership used by subsequent MCP and dashboard requests.

Then call `get_website_build_context` only when the selected workflow needs website-specific data, passing the smallest relevant `include` list.

Hard invariants live in the MCP server instructions. Task detail lives in the catalog, `sdp://instructions/{skill}`, and [references/workflows.md](references/workflows.md). Component source, fields, and version switching are also summarized in [references/components.md](references/components.md).
