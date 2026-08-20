# Credit Packs

API version: `2026-07-31`

## update

`commet.credit_packs.update(...)`

`PATCH /credit-packs/{id}` · operation `update-credit-pack`

Update a credit pack's name, description, credits, price, or active status.

### Parameters

- `id` (`str`, required)
- `name` (`str`, optional)
- `description` (`str`, optional)
- `credits` (`int`, optional)
- `price` (`int`, optional)
- `is_active` (`bool`, optional)

### Request options

- `idempotency_key` (`str`, optional) — Unique key used to safely retry this write for 24 hours without applying it twice.

### Returns

`CreditPack`

## delete

`commet.credit_packs.delete(...)`

`DELETE /credit-packs/{id}` · operation `delete-credit-pack`

Soft-delete a credit pack.

### Parameters

- `id` (`str`, required)

### Returns

`DeletedObject`

## list

`commet.credit_packs.list(...)`

`GET /credit-packs` · operation `list-credit-packs`

List all active credit packs.

### Returns

`CreditPacksListResult`

## create

`commet.credit_packs.create(...)`

`POST /credit-packs` · operation `create-credit-pack`

Create a new credit pack.

### Parameters

- `name` (`str`, required)
- `description` (`str`, optional)
- `credits` (`int`, required)
- `price` (`int`, required)
- `is_active` (`bool`, optional)

### Request options

- `idempotency_key` (`str`, optional) — Unique key used to safely retry this write for 24 hours without applying it twice.

### Returns

`CreditPack`
