---
name: sdp-listings
description: Administer SDP listing catalogs through Listings MCP on the themes host. Use for listing types, custom fields, brands, collections, media, and creating or updating listings. Do not use for inquiries, customers, or storefront HTML.
---

# SDP Listings

The user must already have an SDP account at https://sdp-platform.com. If OAuth fails, send them there to sign up or sign in first. Do not invent API keys.

Call `list_companies` first. Pass explicit `company_id` on every other tool.

Read `sdp://listings/instructions` before creating or mutating catalog records. Do not invent listing, type, brand, or collection ids.

## Images

Import a public image URL or complete a Cloudflare direct upload. Never send base64. Stage images with `staging_key`, then pass returned `upload_id` values as `image_upload_ids` on `create_listing`.

## Storefront

Website Builder only renders `{sdpGetListings}` / `{sdpGetListing}` pages. Link items to `/listings/{$listing->slug}`. Inquiry CTAs use `/cp/new-inquiry/{$listing->id}`.

## Instruction reference

Read [references/instructions.md](references/instructions.md) for source-exported workflows and examples. Refresh the hosted instruction resource before mutations; it takes precedence over this bundled snapshot.

For listing type, brand, collection, or variant images, use `import_catalog_image_url` or the catalog direct-upload flow, then `attach_catalog_image` with the returned `file_id`. Upload completion alone does not attach the image.

`update_listing_variant` requires `price` and the full `custom_field_values` set on every call. Use type fields with `use_for_variants` enabled.
