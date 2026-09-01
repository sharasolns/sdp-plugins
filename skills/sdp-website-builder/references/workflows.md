# Website builder workflows

Generated from `WebsiteBuilderInstructionCatalog`. Do not edit by hand.

# website.create

Create a website and establish its reusable visual foundation.

- Server: `website-builder` (`/mcp/website-builder`)
- Resource: `sdp://instructions/website.create`

## Workflow

1. Create the website, then call get_website_build_context with include=[website,global_code,architecture,component_inventory,templates] for its initial build state.
2. If global_code.custom_css_bytes is zero, read custom_css and establish reusable design tokens, base typography, and shared semantic classes before creating many components.
3. Preserve website.theme.frontend_framework. Do not introduce a competing utility framework.
4. Build reusable components as cohesive sections, compose pages, validate, preview, and publish only after review.

## Tools

- `create_website`
- `get_website_build_context`
- `get_website_global_code`
- `update_website_global_code`

# website.settings

Read or partially update website identity and media settings.

- Server: `website-builder` (`/mcp/website-builder`)
- Resource: `sdp://instructions/website.settings`

## Workflow

1. Read settings before mutation and send only fields that should change.
2. For logo, favicon, or featured image, import a public image or complete a direct upload first, then store the returned public URL.

## Tools

- `get_website_settings`
- `update_website_settings`
- `upload_website_image`
- `create_website_image_upload`
- `complete_website_image_upload`

# website.domain

Connect a custom domain or free sm.ke subdomain and verify DNS.

- Server: `website-builder` (`/mcp/website-builder`)
- Resource: `sdp://instructions/website.domain`

## Workflow

1. Call get_website_domain first. Use recommended_action and next_steps; do not invent DNS records.
2. Prefer Cloudflare DNS. The owner must point nameservers at Cloudflare before add_custom. Then call connect_website_domain action=add_custom with the hostname.
3. Call start_cloudflare_connect and ask the owner to open authorization_url. After they finish, call verify. If automatic setup is unavailable, give the returned dns_records (CNAME to cname.sdp-builder.com) and then verify.
4. If the owner does not want DNS, use add_sm_ke with a label such as hauzisha to create hauzisha.sm.ke. That path does not need Cloudflare or lookup.
5. Verification can stay pending for a few minutes. Keep the temporary domain until custom_domain.status is active. Use remove only when the owner wants to detach the domain.

## Tools

- `get_website_domain`
- `connect_website_domain`

# component.create

Create one reusable Latte component with the correct schema, source, and styling.

- Server: `website-builder` (`/mcp/website-builder`)
- Resource: `sdp://instructions/component.create`

## Style ownership

- `website.custom_css`: Site-wide SCSS compiled unscoped into the page. Use it for :root/CSS variables, base typography, and classes shared by many components. Invalid SCSS is rejected on update; published CSS falls back to the raw source only if compile fails at render. Read with get_website_global_code include=[custom_css].
- `component.scss`: Optional SCSS for this component only. The runtime wraps it in [data-component] or [data-version], so write unprefixed selectors such as .card or h2 — do not target html, body, or :root, and do not wrap it again yourself. Omit the field when framework utilities are enough. scss:null clears it.
- `latte.style_scoped`: An inline <style scoped> block in Latte is extracted to <head> and rewritten to the same component/version scope. An unscoped <style> is treated as global and can leak. Prefer the scss field or <style scoped>; do not duplicate the same rules in both.

## Workflow

1. Call get_website_build_context with include=[website,global_code,field_type_contract,architecture,component_inventory], then inspect existing website_components and component_types before creating anything.
2. Fetch a candidate type with get_component_type before reusing its ID. Pass component_type_id to reuse it. Omit both type fields to create a one-off type from the component name and optional fields. Create a new shared type only when the logical schema is genuinely different.
3. One component represents one cohesive section. Repeated items within that section use one array-of-objects field.
4. Component types provide defaults; create_website_component.fields may add or override instance fields without mutating the type.
5. If global_code.custom_css_bytes is zero, establish tokens and shared classes first. Put only this section's rules in component scss (auto-scoped) or <style scoped>. Reference shared global classes from markup. Match website.theme.frontend_framework; do not mix Bootstrap and Tailwind.
6. Use semantic field types from field_type_contract. Latte object and repeater children use ->child access.
7. Image fields: write a public URL in data and alt in field_meta.{field}.alt, or write {url, alt}. Render <img src="{$image->url ?? $image}" alt="{$image->alt ?? ''}">. Nested images inside object/array children must be {url, alt} objects.
8. Link fields are objects: {$link->url}, {$link->text}, {$link->target}. HTML/rich text uses {$body|noescape}. Do not put class="" and n:class on the same element.
9. Create and validate components sequentially. Correct errors until valid=true before placement.

## Tools

- `get_website_build_context`
- `get_component_type`
- `create_component_type`
- `create_website_component`
- `validate_website_component`

# component.update

Safely update component Latte, SCSS, data, or a page-local placement.

- Server: `website-builder` (`/mcp/website-builder`)
- Resource: `sdp://instructions/component.update`

## Workflow

1. Read the authoritative component with get_website_component before editing it.
2. Check source_mode. When it is version, effective_custom_html/effective_scss are rendered and local custom_html/scss are dormant.
3. Use update_website_component for complete selected-field replacement. Sending only custom_html preserves effective SCSS; sending only scss preserves effective HTML; scss:null clears SCSS. Component SCSS is auto-scoped — do not use it for site-wide tokens. A local edit materializes the preserved effective counterpart before switching source_mode to local.
4. Use patch_website_component_source only when the exact fragment occurs once in the effective selected source. Broaden the search context when a short fragment is ambiguous.
5. Use set_component_data for reusable source values and update_page_component for page-local values. Do not change a reusable source when only one placement should differ.
6. Never retry a truncated or invalid large payload unchanged. Reduce it to one component operation.
7. Validate after every source or schema change until valid=true.

## Tools

- `get_website_component`
- `update_website_component`
- `patch_website_component_source`
- `set_component_data`
- `update_page_component`
- `validate_website_component`

# component.fields

Add, override, soft-remove, or restore fields on one component instance.

- Server: `website-builder` (`/mcp/website-builder`)
- Resource: `sdp://instructions/component.fields`

## Workflow

1. Read the component and its resolved fields first. Component types are defaults; instances may own different or additional fields.
2. Use add_or_update for schema definitions, remove for reversible soft-removal, and restore to reactivate removed fields.
3. Set field values only after the resolved schema contains those keys. Unknown-field errors require re-reading the schema rather than guessing.
4. Use image, bootstrap_icon, link, object, array, and scalar array types according to field_type_contract.
5. Image values are a public URL or {url, alt}. Nested image children inside objects/repeaters must be {url, alt} so alt is available as $item->image->alt.

## Tools

- `get_website_component`
- `get_component_type`
- `update_website_component_fields`
- `set_component_data`
- `validate_website_component`

# component.version

Switch the reusable version behind an existing page placement without deleting it.

- Server: `website-builder` (`/mcp/website-builder`)
- Resource: `sdp://instructions/component.version`

## Workflow

1. Use the page-owned placement ID and the target reusable source component ID.
2. change_page_component_version preserves placement identity, position, compatible data, instance fields, soft-removed fields, and dormant local source.
3. The default conflict strategy rejects incompatible matching field types. Use use_target only when replacing that field definition and value is intended.
4. Validate the placement and inspect the page preview before publishing.

## Tools

- `get_page`
- `get_website_component`
- `change_page_component_version`
- `validate_website_component`

# page.compose

Compose a page from reusable component placements while preserving template ownership.

- Server: `website-builder` (`/mcp/website-builder`)
- Resource: `sdp://instructions/page.compose`

## Workflow

1. Call get_website_build_context with include=[website,architecture,component_inventory,templates], then read get_page. Pages place content only in the selected template page_sections and inherit the shared shell.
2. Reuse compatible website components. A normal multi-section page uses multiple cohesive components, not one entire-page component.
3. Use replace_page_composition when replacing the complete ordered composition; use add, move, update, or delete tools for precise changes.
4. Placement data is local. Preserve exact ordering and preview before publishing.

## Tools

- `get_website_build_context`
- `get_page`
- `replace_page_composition`
- `add_page_component`
- `move_page_component`
- `update_page_component`
- `delete_page_component`

# template.build

Create or update the minimal template family and shared shell.

- Server: `website-builder` (`/mcp/website-builder`)
- Resource: `sdp://instructions/template.build`

## Workflow

1. Keep exactly one base template plus only the page, blank-page, post, and error children the website needs.
2. The base alone owns shared template-section placements such as header and footer.
3. Each child directly inherits the base and declares inherited template section names, but never duplicates parent-owned placements.
4. Children may own defaults only in page_sections. A post template also owns one body View Post component rendering the runtime $page object.
5. Call get_website_build_context with include=[website,architecture,component_inventory,templates], read architecture_warnings, preserve ordering, and set the view-post or 404 template explicitly when required.

## Tools

- `get_website_build_context`
- `create_website_template`
- `update_website_template`
- `replace_template_composition`
- `set_view_post_template`
- `set_404_template`

# global_code.update

Safely update global CSS, header scripts, footer scripts, or robots.txt.

- Server: `website-builder` (`/mcp/website-builder`)
- Resource: `sdp://instructions/global_code.update`

## Workflow

1. get_website_global_code returns byte counts by default. Pass include=[custom_css] (or header_scripts, footer_scripts, robots_txt) to read a body before mutation.
2. Use update_website_global_code for complete selected-field replacement; omitted fields remain unchanged; null clears a field. CSS/SCSS is compiler-validated and the whole update is rejected if it cannot compile.
3. Use patch_website_global_code only when one exact search fragment occurs once.
4. Global custom_css is unscoped site-wide SCSS. Define :root tokens (including --sdp-* overrides), base typography, and classes reused by multiple components. Do not put one-section layout rules here.
5. On Tailwind sites, dark: follows html.dark after header_scripts <meta name="sdp-theme" content="class">. Use light defaults plus dark: variants. Do not put dark-only colors in @theme; those flatten to :root and stay light.
6. Preserve website.theme.frontend_framework. Publish with publish_website after global CSS or script changes; clear_website_cache does not deploy them.

## Tools

- `get_website_global_code`
- `update_website_global_code`
- `patch_website_global_code`
- `publish_website`

# media.upload

Import public media or upload a local image/video without placing binary data in MCP calls.

- Server: `website-builder` (`/mcp/website-builder`)
- Resource: `sdp://instructions/media.upload`

## Workflow

1. Import a public image with upload_website_image.
2. For a local image, create an upload, POST the raw file once to upload_url, then complete the upload.
3. For a local video under 200 MB, create an upload, POST once, then repeat only completion while processing continues.
4. Never send base64 media in an MCP tool call. Store the returned public URL in image fields (plus field_meta.alt or {url, alt}) or apply it as featured media.

## Tools

- `upload_website_image`
- `create_website_image_upload`
- `complete_website_image_upload`
- `create_website_video_upload`
- `complete_website_video_upload`
- `set_content_featured_image`

# runtime.posts

Render post lists, categories, or one post with supported Latte runtime data.

- Server: `website-builder` (`/mcp/website-builder`)
- Resource: `sdp://instructions/runtime.posts`

## Workflow

1. Call get_website_build_context with include=[website,field_type_contract,runtime_content] for authoritative fields and examples.
2. On a normal page call {sdpGetPosts N}, iterate $posts, and paginate with {sdpPaginate 'posts'}. Declare every component-controlled filter in the component schema.
3. Use {sdpGetBlogCategories N} or its documented aliases for category lists.
4. On a post template the runtime $page object already exists; render trusted body HTML as documented and guard nullable relationships.

## Tools

- `get_website_build_context`
- `get_component_type`
- `create_website_component`

# runtime.catalog

Render ecommerce, listing, course, taxonomy, archive, or custom-order runtime content.

- Server: `website-builder` (`/mcp/website-builder`)
- Resource: `sdp://instructions/runtime.catalog`

## Workflow

1. Call get_website_build_context with include=[website,field_type_contract,runtime_content] and check website.feature_modules before building. Do not build a disabled module.
2. Use the documented list directive with its numeric per-page argument. Declare every filter that component data should control.
3. Create single-item pages with the documented dynamic route and one body component calling the matching single-item directive.
4. For ecommerce actions, use the documented <checkout-product-link> and <add-product-to-cart> elements with the numeric product id and required product attributes. On Tailwind sites call {sdpInjectProductsScript} once before using them; do not recreate checkout URLs or cart JavaScript.
5. Use distinct archive prefixes, the documented heading getter, and taxonomy list directives. Avoid conflicting dynamic route parameters.
6. Use {sdpInjectCustomFormScript} for custom-order forms. Obtain type slug, field slugs, and pricing item ids from Custom Forms MCP (/mcp/custom-forms on the themes host). Never invent them.
7. After submit, reveal the hidden success element selected by the first tag argument, set data-success-redirect="/thank-you", or set data-success-redirect="view-order" to open /cp/view-custom-order/{unique_id}. Redirect takes precedence. Optional {unique_id} is replaced on custom paths.

## Tools

- `get_website_build_context`
- `create_page`
- `create_website_component`
- `replace_page_composition`

# content.publish

Review lifecycle state and publish website, page, or post changes safely.

- Server: `website-builder` (`/mcp/website-builder`)
- Resource: `sdp://instructions/content.publish`

## Workflow

1. Use discovery tools before precise mutation and get_website_content_summary for counts instead of walking large catalogs.
2. Validate components and inspect previews before publishing.
3. Use publish_page or publish_post after content review, change_content_status for other lifecycle changes, and keep parking separate from status.
4. Use get_website_status to inspect unpublished changes and publish_website to deploy website-level changes. Clearing cache does not publish.

## Tools

- `get_website_content_summary`
- `get_website_status`
- `publish_page`
- `publish_post`
- `change_content_status`
- `publish_website`

# seo.read

Read stored Google Search Console analysis without triggering refreshes.

- Server: `website-builder` (`/mcp/website-builder`)
- Resource: `sdp://instructions/seo.read`

## Workflow

1. These tools live on /mcp/website-builder: get_website_seo_overview, list_website_seo_queries, get_website_seo_query, list_website_seo_pages, get_website_seo_page.
2. Start with get_website_seo_overview, discover rows with list_website_seo_queries or list_website_seo_pages, then drill into one exact query or page URL.
3. These read-only tools do not return AI Visibility data and do not refresh Search Console.

## Tools

- `get_website_seo_overview`
- `list_website_seo_queries`
- `get_website_seo_query`
- `list_website_seo_pages`
- `get_website_seo_page`

# planner.manage

Create and manage content plans, assignments, categories, groups, and reminders.

- Server: `website-builder` (`/mcp/website-builder`)
- Resource: `sdp://instructions/planner.manage`

## Workflow

1. These tools live on /mcp/website-builder: list_content_plans, get_content_plan, create_content_plan, update_content_plan, delete_content_plan, change_content_plan_status, convert_content_plan, list_content_plan_groups, create_content_plan_group, update_content_plan_group, delete_content_plan_group, list_planner_assignees, get_planner_reminder_settings, update_planner_reminder_settings.
2. Use list_categories and list_planner_assignees before assigning category_id or assignee_ids.
3. Use change_content_plan_status to move an idea to planned when it is approved for the calendar. Setting planned_date alone does not change its status.
4. A plan category is preserved when convert_content_plan creates a page or post.
5. Read reminder settings before updating due-day, overdue, or final-day behavior.

## Tools

- `list_categories`
- `list_planner_assignees`
- `create_content_plan`
- `update_content_plan`
- `change_content_plan_status`
- `convert_content_plan`
- `get_planner_reminder_settings`
- `update_planner_reminder_settings`

# image_template.build

Design a reusable SDP image template, then render featured/OG images from it.

- Server: `website-builder` (`/mcp/website-builder`)
- Resource: `sdp://instructions/image_template.build`

## Workflow

1. Do not call list_pages or list_posts to invent unique kickers. The template is one reusable card; Cloudflare renders it later with the real $page and $website for each content item.
2. Call list_image_templates first. Reuse a compatible template before creating another. Set include_source=true only when editing Latte.
3. save_image_template once. Put CSS in a <style> block inside custom_html. Bind copy to {$page->title}, {$page->meta_description}, {$website->name}, and {$website->logo}. Blade and JavaScript are rejected. Default size is 1200x630.
4. preview_image_template with content_type, content_id, and template_id. preview_url is /cms/image/{content_id}/{template_id}?website_id=. Open that URL; do not rewrite the IDs.
5. Then generate_image_from_template with that template_id and each page or post content_id. render_image_from_template returns a media URL without applying it.
6. Do not invent a custom HTML screenshot path or attach a one-off image when an image template should be used.
7. list_featured_image_templates, save_featured_image_template, preview_featured_image_template, and generate_featured_image_from_template are legacy aliases of the same workflow.

## Tools

- `list_image_templates`
- `save_image_template`
- `preview_image_template`
- `render_image_from_template`
- `generate_image_from_template`

# company.switch

Select the company membership used by subsequent MCP and dashboard requests.

- Server: `website-builder` (`/mcp/website-builder`)
- Resource: `sdp://instructions/company.switch`

## Workflow

1. Call list_companies first and select an accessible company ID.
2. A successful switch applies to subsequent requests; do not guess company IDs.

## Tools

- `list_companies`
- `switch_company`
