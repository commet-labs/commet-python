# Usage

API version: `2026-07-31`

## check

`commet.usage.check(...)`

`POST /usage/check` · operation `check-usage-availability`

Check if a customer can consume a feature before actual consumption. Returns availability and cost estimates based on the plan's consumption model.

### Parameters

- `customer_id` (`str`, required)
- `feature_code` (`str`, required)
- `quantity` (`int`, optional)

### Request options

- `idempotency_key` (`str`, optional) — Unique key used to safely retry this write for 24 hours without applying it twice.

### Returns

`UsageCheck`

## track

`commet.usage.track(...)`

`POST /usage/events` · operation `track-usage`

Track a usage event for a metered feature. Deducts from balance/credits if applicable.

### Parameters

- `feature_code` (`str`, required)
- `customer_id` (`str`, required)
- `event_id` (`str`, optional)
- `timestamp` (`str`, optional)
- `properties` (`list[TrackUsageParamsPropertiesItem]`, optional)
- `model` (`str`, optional)
- `input_tokens` (`int`, optional)
- `output_tokens` (`int`, optional)
- `value` (`float`, optional)
- `cache_read_tokens` (`int`, optional)
- `cache_write_tokens` (`int`, optional)

### Request options

- `idempotency_key` (`str`, optional) — Unique key used to safely retry this write for 24 hours without applying it twice.

### Returns

`UsageEvent`

## set

`commet.usage.set(...)`

`PUT /usage` · operation `set-usage`

Set a metered feature's usage to an exact value for the current period. Use the Idempotency-Key header to make retries safe.

### Parameters

- `customer_id` (`str`, required)
- `feature_code` (`str`, required)
- `value` (`int`, required)
- `reason` (`str`, optional)

### Request options

- `idempotency_key` (`str`, optional) — Unique key used to safely retry this write for 24 hours without applying it twice.

### Returns

`UsageAdjustment`
