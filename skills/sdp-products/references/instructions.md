# SDP Products MCP

This server administers product catalogs. It does not operate carts, checkout, orders, reviews, customers, or storefront links.

Except for `list_companies`, every tool requires an explicit numeric `company_id`. Never infer a company from a previous call.

## Discover and read

```json
{"tool":"list_companies","arguments":{}}
{"tool":"list_products","arguments":{"company_id":42,"status":"active","search":"shirt","limit":25}}
{"tool":"get_product","arguments":{"company_id":42,"product_id":314}}
```

## Create with a public image

Importing without `product_id` stages the image. Supply its returned `upload_id` to `create_product`.

```json
{"tool":"import_product_image_url","arguments":{"company_id":42,"staging_key":"new-blue-shirt","url":"https://cdn.example.com/blue-shirt.jpg","is_default":true}}
{"tool":"create_product","arguments":{"company_id":42,"name":"Blue Shirt","sku":"SHIRT-BLUE","currency":"KES","price":2500,"image_upload_ids":["returned-upload-uuid"]}}
```

## Create with direct upload

```json
{"tool":"create_product_image_upload","arguments":{"company_id":42,"staging_key":"new-blue-shirt","name":"blue-shirt.jpg","mime_type":"image/jpeg","is_default":true}}
```

POST the binary file once to the returned `upload_url`, then call:

```json
{"tool":"complete_product_image_upload","arguments":{"company_id":42,"upload_id":"returned-upload-uuid"}}
```

Never send base64 through MCP.

## Update, variants, and taxonomies

```json
{"tool":"update_product","arguments":{"company_id":42,"product_id":314,"price":2750,"description":"Updated description"}}
{"tool":"create_product_variant","arguments":{"company_id":42,"product_id":314,"name":"Large","price":2850,"custom_field_values":[{"product_type_custom_field_id":8,"value":"L"}]}}
{"tool":"create_product_category","arguments":{"company_id":42,"name":"Clothing"}}
{"tool":"create_brand","arguments":{"company_id":42,"name":"SDP Apparel"}}
```

## Catalog images (brand logos, category and product type covers)

`import_catalog_image_url` and `create_catalog_image_upload` + `complete_catalog_image_upload` produce an unattached `file_id`; nothing is visible on any record until `attach_catalog_image` is called. This same flow covers brands, product categories, product types, and product collections — one set of tools, no per-entity image tools. Products themselves keep their own dedicated gallery tools (import_product_image_url / create_product_image_upload / complete_product_image_upload) since they support multiple ordered images with list/update/reorder/delete.

```json
{"tool":"import_catalog_image_url","arguments":{"company_id":42,"url":"https://cdn.example.com/apparel-icon.png"}}
{"tool":"attach_catalog_image","arguments":{"company_id":42,"target_type":"product_type","target_id":7,"file_id":"returned-file-id"}}
```

For a direct upload instead of a public URL:

```json
{"tool":"create_catalog_image_upload","arguments":{"company_id":42,"name":"apparel-icon.jpg","mime_type":"image/jpeg"}}
```

POST the binary file once to the returned `upload_url`, then call `complete_catalog_image_upload` with the `upload_id` to get a `file_id`, then `attach_catalog_image` as above. `target_type` accepts `brand`, `product_category`, `product_type`, `product_collection`, or `product_variant`.

## Archive and restore

```json
{"tool":"archive_product","arguments":{"company_id":42,"product_id":314}}
{"tool":"restore_product","arguments":{"company_id":42,"product_id":314}}
```

Products are never permanently deleted. Variant, unused taxonomy, and media deletion tools are permanent.

## Common errors

- `stale_membership_version`: refresh the OAuth access token and retry.
- `permission_denied`: the company-local ecommerce user lacks the matching permission or has not opened Ecommerce from the dashboard.
- `ECOMMERCE_NOT_AVAILABLE`: the company is authorized but has not initialized Ecommerce. MCP will not initialize it.
- `validation_error`: inspect the structured field errors and retry with corrected arguments.
