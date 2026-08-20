# Feature Access

API version: `2026-07-31`

## get

`commet.feature_access.get(...)`

`GET /feature-access/{code}` · operation `get-feature-access`

Get one feature's access and current usage for a customer. To evaluate a prospective consumption, use POST /usage/check.

### Parameters

- `code` (`str`, required)
- `customer_id` (`str`, required)

### Returns

`FeatureAccess`

## list

`commet.feature_access.list(...)`

`GET /feature-access` · operation `list-feature-access`

List a customer's feature access and current usage.

### Parameters

- `customer_id` (`str`, required)

### Returns

`FeatureAccessListResult`
