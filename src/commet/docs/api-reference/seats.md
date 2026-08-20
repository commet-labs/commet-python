# Seats

API version: `2026-07-31`

## get_balance

`commet.seats.get_balance(...)`

`GET /seats/balance` · operation `get-seat-balance`

Get current balance for a specific seat type.

### Parameters

- `customer_id` (`str`, required)
- `feature_code` (`str`, required)

### Returns

`SeatBalance`

## get_all_balances

`commet.seats.get_all_balances(...)`

`GET /seats/balances` · operation `get-all-seat-balances`

Get the current balance for all seat types in a customer's subscription.

### Parameters

- `customer_id` (`str`, required)

### Returns

`SeatBalanceCollection`

## set_all

`commet.seats.set_all(...)`

`PUT /seats/bulk` · operation `bulk-set-seats`

Set all seat types at once.

### Parameters

- `customer_id` (`str`, required)
- `seats` (`dict[str, int]`, required)

### Request options

- `idempotency_key` (`str`, optional) — Unique key used to safely retry this write for 24 hours without applying it twice.

### Returns

`SeatsSetAllResult`

## remove

`commet.seats.remove(...)`

`POST /seats/remove` · operation `remove-seats`

Remove seats from a customer's subscription. Takes effect at the end of the billing period.

### Parameters

- `customer_id` (`str`, required)
- `feature_code` (`str`, required)
- `count` (`int`, required)

### Request options

- `idempotency_key` (`str`, optional) — Unique key used to safely retry this write for 24 hours without applying it twice.

### Returns

`SeatEvent`

## add

`commet.seats.add(...)`

`POST /seats` · operation `add-seats`

Add seats to a customer's subscription. Prorates charges for the current billing period.

### Parameters

- `customer_id` (`str`, required)
- `feature_code` (`str`, required)
- `count` (`int`, required)

### Request options

- `idempotency_key` (`str`, optional) — Unique key used to safely retry this write for 24 hours without applying it twice.

### Returns

`SeatEvent`

## set

`commet.seats.set(...)`

`PUT /seats` · operation `set-seats`

Set seats to an exact count.

### Parameters

- `customer_id` (`str`, required)
- `feature_code` (`str`, required)
- `count` (`int`, required)

### Request options

- `idempotency_key` (`str`, optional) — Unique key used to safely retry this write for 24 hours without applying it twice.

### Returns

`SeatEvent`
