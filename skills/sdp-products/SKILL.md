---
name: sdp-products
description: Administer SDP product catalogs through Products MCP on the themes host. Use for product types, brands, categories, collections, media, variants, and creating or updating products. Do not use for cart, checkout, orders, reviews, customers, or storefront HTML.
---

# SDP Products

Call `list_companies` first. Pass explicit `company_id` on every other tool.

Read `sdp://products/instructions` before creating or mutating catalog records. Do not invent product, type, brand, category, or collection ids.

## Images

Import a public image URL or complete a Cloudflare direct upload. Never send base64. Stage images with `staging_key`, then pass returned `upload_id` values as `image_upload_ids` on `create_product`.

## Storefront

Website Builder only renders `{sdpGetProducts}` / `{sdpGetProduct}` pages. Link items to `/products/{$product->slug}`.
