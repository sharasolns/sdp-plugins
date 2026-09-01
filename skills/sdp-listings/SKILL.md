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
