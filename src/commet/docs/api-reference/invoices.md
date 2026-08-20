# Invoices

API version: `2026-07-31`

## get_download_url

`commet.invoices.get_download_url(...)`

`POST /invoices/{id}/download-links` · operation `download-invoice`

Generate a signed URL to download the invoice as a PDF. The URL expires after 7 days.

### Parameters

- `id` (`str`, required)

### Request options

- `idempotency_key` (`str`, optional) — Unique key used to safely retry this write for 24 hours without applying it twice.

### Returns

`InvoiceDownload`

## get

`commet.invoices.get(...)`

`GET /invoices/{id}` · operation `get-invoice`

Retrieve a single invoice by its public ID, including line items.

### Parameters

- `id` (`str`, required)

### Returns

`Invoice`

## send

`commet.invoices.send(...)`

`POST /invoices/{id}/send` · operation `send-invoice`

Send the invoice to the customer via email.

### Parameters

- `id` (`str`, required)

### Request options

- `idempotency_key` (`str`, optional) — Unique key used to safely retry this write for 24 hours without applying it twice.

### Returns

`SentInvoice`

## update_status

`commet.invoices.update_status(...)`

`PATCH /invoices/{id}/status` · operation `update-invoice-status`

Mark an outstanding invoice as "paid" or "void" and return the updated invoice. Cannot change the status of already paid or voided invoices.

### Parameters

- `id` (`str`, required)
- `status` (`Literal["paid", "void"]`, required)

### Request options

- `idempotency_key` (`str`, optional) — Unique key used to safely retry this write for 24 hours without applying it twice.

### Returns

`Invoice`

## list

`commet.invoices.list(...)`

`GET /invoices` · operation `list-invoices`

List invoices with cursor-based pagination. Filter by customer, status, or subscription.

### Parameters

- `cursor` (`str`, optional)
- `limit` (`int`, optional)
- `customer_id` (`str`, optional)
- `status` (`Literal["draft", "outstanding", "paid", "void", "uncollectible"]`, optional)
- `subscription_id` (`str`, optional)

### Returns

`InvoicesListResult`

## create_adjustment

`commet.invoices.create_adjustment(...)`

`POST /invoices` · operation `create-adjustment-invoice`

Create a one-off adjustment invoice and return the created invoice. Use a negative amount for a credit.

### Parameters

- `customer_id` (`str`, required)
- `amount` (`int`, required)
- `description` (`str`, required)
- `metadata` (`dict[str, Any]`, optional)

### Request options

- `idempotency_key` (`str`, optional) — Unique key used to safely retry this write for 24 hours without applying it twice.

### Returns

`Invoice`
