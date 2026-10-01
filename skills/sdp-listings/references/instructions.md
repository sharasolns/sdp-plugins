# SDP Listings MCP

This server administers listing catalogs. It does not operate inquiries, customers, or storefront HTML.

Except for `list_companies`, every tool requires an explicit numeric `company_id`. Never infer a company from a previous call.

Website Builder MCP renders listing pages with `{sdpGetListings}` / `{sdpGetListing}`. Do not invent listing slugs or ids.

## Discover and read

```json
{"tool":"list_companies","arguments":{}}
{"tool":"list_listings","arguments":{"company_id":42,"status":"active","search":"house","limit":25}}
{"tool":"get_listing","arguments":{"company_id":42,"listing_id":18}}
```

## Types, brands, collections, then listings

```json
{"tool":"create_listing_type","arguments":{"company_id":42,"name":"Property","requires_location":true}}
{"tool":"replace_listing_type_custom_fields","arguments":{"company_id":42,"listing_type_id":3,"fields":[{"label":"Bedrooms","type":"number"},{"label":"Furnishing","type":"select","options":["Furnished","Unfurnished"]}]}}
{"tool":"create_listing_brand","arguments":{"company_id":42,"name":"Harbor Homes"}}
{"tool":"import_listing_image_url","arguments":{"company_id":42,"staging_key":"new-apt","url":"https://cdn.example.com/apt.jpg","is_default":true}}
{"tool":"create_listing","arguments":{"company_id":42,"name":"2-bed apartment","currency":"KES","price":45000,"listing_type_id":3,"listing_brand_id":5,"location_name":"Westlands","image_upload_ids":["returned-upload-uuid"],"custom_field_values":{"bedrooms":2}}}
```

Gallery tools match products: import a public URL or create a Cloudflare direct-upload, then complete it. Never send base64. Attach staged `upload_id`s on `create_listing`, or pass `listing_id` to add images to an existing listing. Brand and location are required only when the listing type has `requires_brand` or `requires_location`.

## Catalog images (listing type covers, listing brand logos, listing collection covers)

`import_catalog_image_url` and `create_catalog_image_upload` + `complete_catalog_image_upload` produce an unattached `file_id`; nothing is visible on any record until `attach_catalog_image` is called. This same flow covers listing types, listing brands, and listing collections — one set of tools, no per-entity image tools.

```json
{"tool":"import_catalog_image_url","arguments":{"company_id":42,"url":"https://cdn.example.com/property-icon.png"}}
{"tool":"attach_catalog_image","arguments":{"company_id":42,"target_type":"listing_type","target_id":3,"file_id":"returned-file-id"}}
```

`target_type` accepts `listing_type`, `listing_brand`, `listing_collection`, or `listing_variant`.

## Variants

`custom_field_values` must reference `listing_custom_field_id`s that belong to the listing's type and have `use_for_variants` enabled.

```json
{"tool":"create_listing_variant","arguments":{"company_id":42,"listing_id":18,"name":"2 bedrooms","price":50000,"custom_field_values":[{"listing_custom_field_id":9,"value":"2"}]}}
```

Unlike `update_product_variant`, `update_listing_variant` is not a partial patch: `price` and the full `custom_field_values` set are required on every call, even to change only `name`.

## Archive and restore

```json
{"tool":"archive_listing","arguments":{"company_id":42,"listing_id":18}}
{"tool":"restore_listing","arguments":{"company_id":42,"listing_id":18}}
```

Listings are never permanently deleted. Unused types, brands, and collections can be deleted.

## Common errors

- `stale_membership_version`: refresh the OAuth access token and retry.
- `permission_denied`: the company-local listings user lacks the matching permission or has not opened Listings from the dashboard.
- `LISTINGS_NOT_AVAILABLE`: the company is authorized but has not initialized Listings. MCP will not initialize it.
- `validation_error`: inspect the structured field errors and retry with corrected arguments.
