# SDP Custom Forms MCP

This server administers custom order types used by public website forms. It does not place orders, take payments, or write storefront HTML.

Except for `list_companies`, every tool requires an explicit numeric `company_id`. Never infer a company from a previous call.

Website Builder MCP (`/mcp/website-manager` on the backend) renders the public form. Pass the type `slug` and pricing-item `id` values returned here into that form. Do not invent them.

## Discover and read

```json
{"tool":"list_companies","arguments":{}}
{"tool":"list_custom_order_types","arguments":{"company_id":42,"is_active":true}}
{"tool":"get_custom_order_type","arguments":{"company_id":42,"custom_order_type_id":7}}
```

## Create a type, then packages and fields

```json
{"tool":"create_custom_order_type","arguments":{"company_id":42,"name":"Logo design","currency_code":"KES","has_notes":true}}
{"tool":"replace_custom_order_type_pricing_items","arguments":{"company_id":42,"custom_order_type_id":7,"pricing_items":[{"name":"Starter","base_price":5000},{"name":"Pro","base_price":12000}]}}
{"tool":"replace_custom_order_type_fields","arguments":{"company_id":42,"custom_order_type_id":7,"fields":[{"label":"Brand name","type":"text","is_required":true},{"label":"Rush","type":"boolean","affects_price":true,"price_modifier_type":"add","price_modifier_value":1500},{"label":"Package","type":"select","options":["starter","pro"],"affects_price":true,"option_price_modifiers":{"starter":{"type":"add","value":0},"pro":{"type":"add","value":7000}}}]}}
```

Only `select`, `multi_select`, `number`, and `boolean` fields may set `affects_price`. Modifiers are `add`, `multiply`, or `percentage`.

## Deadline bands and auto-priced offers

Time-bound types can add rush bands, then offers that auto-calculate from the package, field modifiers, and deadline hours. Omit `amount` or pass `auto_amount: true`. An explicit `amount` is a manual override.

```json
{"tool":"update_custom_order_type","arguments":{"company_id":42,"custom_order_type_id":7,"is_time_bound":true,"default_deadline_days":7}}
{"tool":"replace_custom_order_type_deadline_pricing_bands","arguments":{"company_id":42,"custom_order_type_id":7,"bands":[{"label":"Rush 24h","min_hours":0,"max_hours":24,"price_modifier_type":"percentage","price_modifier_value":25}]}}
{"tool":"create_custom_order_offer","arguments":{"company_id":42,"custom_order_type_id":7,"custom_order_pricing_item_id":12,"name":"Starter rush","auto_amount":true,"deadline_duration_hours":24,"fields":{"rush":true}}}
```

## Update and delete

```json
{"tool":"update_custom_order_type","arguments":{"company_id":42,"custom_order_type_id":7,"is_active":true}}
{"tool":"delete_custom_order_type","arguments":{"company_id":42,"custom_order_type_id":7}}
```

Types with existing orders cannot be deleted. Pricing items that already have orders are kept when omitted from a replace call.

## Common errors

- `stale_membership_version`: refresh the OAuth access token and retry.
- `permission_denied`: the company-local custom-orders user lacks `custom_orders.custom_order_types` or has not opened Custom Orders from the dashboard.
- `CUSTOM_ORDERS_NOT_AVAILABLE`: the company is authorized but has not initialized Custom Orders. MCP will not initialize it.
- `validation_error`: inspect the structured field errors and retry with corrected arguments.
