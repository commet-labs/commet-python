# Offers

API version: `2026-07-31`

## get

`commet.offers.get(...)`

`GET /offers/{id}` · operation `get-offer`

Retrieve reusable offer terms by public ID.

### Parameters

- `id` (`str`, required)

### Returns

`Offer`

## update

`commet.offers.update(...)`

`PATCH /offers/{id}` · operation `update-offer`

Replace reusable offer terms. Existing applications keep their immutable accepted terms.

### Parameters

- `id` (`str`, required)
- `name` (`str`, required)
- `phases` (`list[UpdateOfferParamsPhasesItem]`, required)
- `metadata` (`dict[str, Any]`, optional)
- `starts_at` (`str | null`, optional)
- `ends_at` (`str | null`, optional)
- `active` (`bool`, optional)

### Request options

- `idempotency_key` (`str`, optional) — Unique key used to safely retry this write for 24 hours without applying it twice.

### Returns

`Offer`

## delete

`commet.offers.delete(...)`

`DELETE /offers/{id}` · operation `delete-offer`

Soft-delete an Offer. Existing applications and their accepted terms remain available for billing and audit.

### Parameters

- `id` (`str`, required)

### Returns

`DeletedOffer`

## list

`commet.offers.list(...)`

`GET /offers` · operation `list-offers`

List reusable offer terms. Offers are independent from plans, prices, eligibility, and distribution channels.

### Parameters

- `cursor` (`str`, optional)
- `limit` (`int`, optional)
- `active` (`bool`, optional)

### Returns

`OffersListResult`

## create

`commet.offers.create(...)`

`POST /offers` · operation `create-offer`

Create reusable offer terms without assigning a plan, price, eligibility rule, or distribution channel.

### Parameters

- `name` (`str`, required)
- `phases` (`list[CreateOfferParamsPhasesItem]`, required)
- `metadata` (`dict[str, Any]`, optional)
- `starts_at` (`str | null`, optional)
- `ends_at` (`str | null`, optional)
- `active` (`bool`, optional)

### Request options

- `idempotency_key` (`str`, optional) — Unique key used to safely retry this write for 24 hours without applying it twice.

### Returns

`Offer`
