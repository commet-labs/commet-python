# Features

API version: `2026-07-31`

## get

`commet.features.get(...)`

`GET /features/{code}` · operation `get-feature`

Get a single feature definition by code from the organization's feature catalog.

### Parameters

- `code` (`str`, required)

### Returns

`Feature`

## update

`commet.features.update(...)`

`PATCH /features/{code}` · operation `update-feature`

Update a feature's name, description, or unit name. At least one field must be provided.

### Parameters

- `code` (`str`, required)
- `name` (`str`, optional)
- `description` (`str | null`, optional)
- `unit_name` (`str | null`, optional)

### Request options

- `idempotency_key` (`str`, optional) — Unique key used to safely retry this write for 24 hours without applying it twice.

### Returns

`Feature`

## delete

`commet.features.delete(...)`

`DELETE /features/{code}` · operation `delete-feature`

Delete a feature. Fails if the feature is attached to active plans or has an active add-on.

### Parameters

- `code` (`str`, required)

### Returns

`DeletedObject`

## list

`commet.features.list(...)`

`GET /features` · operation `list-features`

List every feature defined in the organization. This is the organization's feature catalog (definitions), not a customer's feature access.

### Returns

`FeaturesListResult`

## create

`commet.features.create(...)`

`POST /features` · operation `create-feature`

Create a new feature. Code must be lowercase alphanumeric with underscores.

### Parameters

- `name` (`str`, required)
- `code` (`str`, required)
- `type` (`Literal["boolean", "usage", "seats", "quota"]`, required)
- `description` (`str`, optional)
- `unit_name` (`str`, optional)

### Request options

- `idempotency_key` (`str`, optional) — Unique key used to safely retry this write for 24 hours without applying it twice.

### Returns

`Feature`
