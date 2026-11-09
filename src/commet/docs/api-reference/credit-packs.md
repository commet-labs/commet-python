# Credit Packs

API version: `2026-08-27`

## update

`commet.credit_packs.update(...)`

`PATCH /credit-packs/{id}` · operation `update-credit-pack`

Update a credit pack's name, description, credits, price, active status, or the plans that sell it.

### Parameters

- `id` (`str`, required)
- `name` (`str`, optional)
- `description` (`str`, optional)
- `credits` (`int`, optional)
- `price` (`int`, optional)
- `is_active` (`bool`, optional)
- `plan_ids` (`list[str]`, optional) — Plans that sell the credit pack, replacing the current ones. Empty means every plan; omitted keeps them.

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
- `plan_ids` (`list[str]`, optional) — Plans that sell the credit pack. Omitted or empty, every plan sells it. Plans created later sell it too.

### Request options

- `idempotency_key` (`str`, optional) — Unique key used to safely retry this write for 24 hours without applying it twice.

### Returns

`CreditPack`
