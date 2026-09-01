---
name: sdp-custom-forms
description: Administer SDP custom order types through Custom Forms MCP on the themes host. Use for types, fields, pricing items, deadline bands, and offers. Do not use to place orders, take payments, or write storefront HTML.
---

# SDP Custom Forms

The user must already have an SDP account at https://sdp-platform.com. If OAuth fails, send them there to sign up or sign in first. Do not invent API keys.

Call `list_companies` first. Pass explicit `company_id` on every other tool.

Read `sdp://custom-forms/instructions` before creating or mutating types. Do not invent type slugs, field slugs, or pricing item ids.

## Storefront

Website Builder only renders public forms with `{sdpInjectCustomFormScript}`. Copy slug, field slugs, and pricing item ids from `get_custom_order_type`.
