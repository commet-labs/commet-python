# Quota

API version: `2026-07-31`

## get_all

`commet.quota.get_all(...)`

`GET /usage/quota/all` · operation `get-all-quota-allowances`

Get all quota allowances for a customer across every quota feature in their plan.

### Parameters

- `customer_id` (`str`, required)

### Returns

`QuotaGetAllResult`

## remove

`commet.quota.remove(...)`

`POST /usage/quota/remove` · operation `remove-quota`

Remove from a customer's quota allowance for a feature. Defaults to 1 if count is omitted. Returns 400 insufficient_balance if the balance would go negative.

### Parameters

- `feature_code` (`str`, required)
- `count` (`int`, optional)
- `customer_id` (`str`, optional)
- `external_id` (`str`, optional)

### Request options

- `idempotency_key` (`str`, optional) — Unique key used to safely retry this write for 24 hours without applying it twice.

### Returns

`UsageQuotaEvent`

## get

`commet.quota.get(...)`

`GET /usage/quota` · operation `get-quota-allowance`

Get the current quota allowance (used vs included) for a specific feature.

### Parameters

- `customer_id` (`str`, required)
- `feature_code` (`str`, required)

### Returns

`UsageQuota`

## add

`commet.quota.add(...)`

`POST /usage/quota` · operation `add-quota`

Add to a customer's quota allowance for a feature. Defaults to 1 if count is omitted.

### Parameters

- `feature_code` (`str`, required)
- `count` (`int`, optional)
- `customer_id` (`str`, optional)
- `external_id` (`str`, optional)

### Request options

- `idempotency_key` (`str`, optional) — Unique key used to safely retry this write for 24 hours without applying it twice.

### Returns

`UsageQuotaEvent`

## set

`commet.quota.set(...)`

`PUT /usage/quota` · operation `set-quota`

Set a customer's quota allowance for a feature to an exact value.

### Parameters

- `feature_code` (`str`, required)
- `count` (`int`, required)
- `customer_id` (`str`, optional)
- `external_id` (`str`, optional)

### Request options

- `idempotency_key` (`str`, optional) — Unique key used to safely retry this write for 24 hours without applying it twice.

### Returns

`UsageQuotaEvent`
