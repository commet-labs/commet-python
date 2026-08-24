# Markets

API version: `2026-07-31`

## get

`commet.markets.get(...)`

`GET /markets/{id}` · operation `get-market`

Get one reusable market.

### Parameters

- `id` (`str`, required)

### Returns

`Market`

## update

`commet.markets.update(...)`

`PATCH /markets/{id}` · operation `update-market`

Replace the name, countries, and metadata of a market.

### Parameters

- `id` (`str`, required)
- `name` (`str`, required)
- `country_codes` (`list[str]`, required)
- `metadata` (`dict[str, Any]`, optional)

### Request options

- `idempotency_key` (`str`, optional) — Unique key used to safely retry this write for 24 hours without applying it twice.

### Returns

`Market`

## delete

`commet.markets.delete(...)`

`DELETE /markets/{id}` · operation `delete-market`

Delete an unused market. Markets referenced by prices or subscriptions cannot be deleted.

### Parameters

- `id` (`str`, required)

### Returns

`DeletedObject`

## list

`commet.markets.list(...)`

`GET /markets` · operation `list-markets`

List reusable country groups that resolve market-specific prices independently from currency.

### Returns

`MarketsListResult`

## create

`commet.markets.create(...)`

`POST /markets` · operation `create-market`

Create a reusable market without attaching it to a plan or price. Countries can belong to only one active market.

### Parameters

- `name` (`str`, required)
- `country_codes` (`list[str]`, required)
- `metadata` (`dict[str, Any]`, optional)

### Request options

- `idempotency_key` (`str`, optional) — Unique key used to safely retry this write for 24 hours without applying it twice.

### Returns

`Market`
