# Component workflows

Generated from `WebsiteBuilderInstructionCatalog` component skills. Do not edit by hand.

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

# Failures

- For schema errors, fetch the authoritative schema and correct the request.
- For source validation errors, change only the failing source or schema and validate again.
- For database/internal errors, retain the diagnostic ID and stop blind retries.
- Publish only after successful validation and preview review.
