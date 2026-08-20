# Promo Codes

API version: `2026-07-31`

## get

`commet.promo_codes.get(...)`

`GET /promo-codes/{id}` · operation `get-promo-code`

Retrieve a promo code by its public ID.

### Parameters

- `id` (`str`, required)

### Returns

`PromoCode`

## update

`commet.promo_codes.update(...)`

`PATCH /promo-codes/{id}` · operation `update-promo-code`

Update a promo code's billing interval, redemption limits, expiration, active status, or plan restrictions.

### Parameters

- `id` (`str`, required)
- `billing_interval` (`Literal["weekly", "monthly", "quarterly", "yearly", "one_time"] | null`, optional)
- `max_redemptions` (`int | null`, optional)
- `expires_at` (`str | null`, optional)
- `active` (`bool`, optional)
- `plan_ids` (`list[str]`, optional)

### Request options

- `idempotency_key` (`str`, optional) — Unique key used to safely retry this write for 24 hours without applying it twice.

### Returns

`PromoCode`

## list

`commet.promo_codes.list(...)`

`GET /promo-codes` · operation `list-promo-codes`

List promo codes with cursor-based pagination.

### Parameters

- `cursor` (`str`, optional)
- `limit` (`int`, optional)

### Returns

`PromoCodesListResult`

## create

`commet.promo_codes.create(...)`

`POST /promo-codes` · operation `create-promo-code`

Create a distribution code for an existing Offer. The referenced Offer owns the benefit and duration; the promo code owns redemption restrictions.

### Parameters

- `code` (`str`, required)
- `offer_id` (`str`, required)
- `billing_interval` (`Literal["weekly", "monthly", "quarterly", "yearly", "one_time"] | null`, optional)
- `max_redemptions` (`int`, optional)
- `expires_at` (`str`, optional)
- `plan_ids` (`list[str]`, optional)

### Request options

- `idempotency_key` (`str`, optional) — Unique key used to safely retry this write for 24 hours without applying it twice.

### Returns

`PromoCode`
