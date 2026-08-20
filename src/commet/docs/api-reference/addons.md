# Addons

API version: `2026-07-31`

## list_active

`commet.addons.list_active(...)`

`GET /active-addons` · operation `list-active-addons`

List all active add-ons for a customer's subscription.

### Parameters

- `customer_id` (`str`, required)

### Returns

`AddonsListActiveResult`

## get

`commet.addons.get(...)`

`GET /addons/{id}` · operation `get-addon`

Retrieve an add-on by its public ID or slug.

### Parameters

- `id` (`str`, required)

### Returns

`Addon`

## update

`commet.addons.update(...)`

`PATCH /addons/{id}` · operation `update-addon`

Update an add-on's name, description, or pricing.

### Parameters

- `id` (`str`, required)
- `name` (`str`, optional)
- `description` (`str`, optional)
- `base_price` (`int`, optional)
- `included_units` (`int`, optional)
- `overage_rate` (`int`, optional)

### Request options

- `idempotency_key` (`str`, optional) — Unique key used to safely retry this write for 24 hours without applying it twice.

### Returns

`Addon`

## delete

`commet.addons.delete(...)`

`DELETE /addons/{id}` · operation `delete-addon`

Soft-delete an add-on. Fails if the add-on has active subscriptions.

### Parameters

- `id` (`str`, required)

### Returns

`DeletedObject`

## list

`commet.addons.list(...)`

`GET /addons` · operation `list-addons`

List all add-ons with cursor-based pagination.

### Parameters

- `cursor` (`str`, optional)
- `limit` (`int`, optional)

### Returns

`AddonsListResult`

## create

`commet.addons.create(...)`

`POST /addons` · operation `create-addon`

Create a new add-on linked to a feature. Each feature can only be assigned to one add-on.

### Parameters

- `name` (`str`, required)
- `description` (`str`, optional)
- `base_price` (`int`, required)
- `feature_id` (`str`, required)
- `consumption_model` (`Literal["boolean", "metered", "credits", "balance"]`, required)
- `included_units` (`int`, optional)
- `overage_rate` (`int`, optional)
- `credit_cost` (`int`, optional)

### Request options

- `idempotency_key` (`str`, optional) — Unique key used to safely retry this write for 24 hours without applying it twice.

### Returns

`Addon`
