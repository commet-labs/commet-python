# Transactions

API version: `2026-07-31`

## refund

`commet.transactions.refund(...)`

`POST /transactions/{id}/refund` · operation `refund-transaction`

Issue a full refund and return the provider-neutral refund resource with its actual status.

### Parameters

- `id` (`str`, required)

### Request options

- `idempotency_key` (`str`, optional) — Unique key used to safely retry this write for 24 hours without applying it twice.

### Returns

`Refund`

## retry

`commet.transactions.retry(...)`

`POST /transactions/{id}/retry` · operation `retry-transaction`

Retry a failed subscription renewal and return an honest retry result. The original failed transaction remains immutable.

### Parameters

- `id` (`str`, required)

### Request options

- `idempotency_key` (`str`, optional) — Unique key used to safely retry this write for 24 hours without applying it twice.

### Returns

`TransactionRetry`

## get

`commet.transactions.get(...)`

`GET /transactions/{id}` · operation `get-transaction`

Retrieve a single payment transaction by its public ID, including provider details.

### Parameters

- `id` (`str`, required)

### Returns

`Transaction`

## list

`commet.transactions.list(...)`

`GET /transactions` · operation `list-transactions`

List payment transactions with cursor-based pagination. Filter by status or customer email.

### Parameters

- `cursor` (`str`, optional)
- `limit` (`int`, optional)
- `status` (`TransactionStatus`, optional)
- `customer_email` (`str`, optional)

### Returns

`TransactionsListResult`
