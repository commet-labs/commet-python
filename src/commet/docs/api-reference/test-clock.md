# Test Clock

API version: `2026-07-31`

## process_billing

`commet.test_clock.process_billing(...)`

`POST /test-clock/process-billing` · operation `process-test-clock-billing`

Deprecated. POST /test-clock now advances time and processes every due billing deadline in one durable run.

Deprecated.

### Request options

- `idempotency_key` (`str`, optional) — Unique key used to safely retry this write for 24 hours without applying it twice.

### Returns

`void`

## get

`commet.test_clock.get(...)`

`GET /test-clock` · operation `get-test-clock`

Returns the organization's current test clock state and latest durable run. Sandbox only.

### Returns

`TestClock`

## advance

`commet.test_clock.advance(...)`

`POST /test-clock` · operation `advance-test-clock`

Starts a durable run that moves the test clock forward and processes every billing deadline due before the target time. Poll GET /test-clock for progress and terminal results. Sandbox only.

### Parameters

- `advance_days` (`int`, optional)
- `frozen_time` (`str`, optional)

### Valid parameter combinations

- `advance_days`
- `frozen_time`

### Request options

- `idempotency_key` (`str`, optional) — Unique key used to safely retry this write for 24 hours without applying it twice.

### Returns

`TestClockRun`
