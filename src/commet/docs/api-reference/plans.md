# Plans

API version: `2026-07-31`

## update_feature

`commet.plans.update_feature(...)`

`PATCH /plans/{id}/features/{featureId}` · operation `update-plan-feature`

Update limits, overage, or enabled status of a feature on a plan.

### Parameters

- `id` (`str`, required)
- `feature_id` (`str`, required)
- `enabled` (`bool`, optional)
- `included_amount` (`int`, optional)
- `unlimited` (`bool`, optional)
- `overage` (`UpdatePlanFeatureParamsOverage`, optional)
- `credits_per_unit` (`int | null`, optional)

### Request options

- `idempotency_key` (`str`, optional) — Unique key used to safely retry this write for 24 hours without applying it twice.

### Returns

`PlanFeature`

## remove_feature

`commet.plans.remove_feature(...)`

`DELETE /plans/{id}/features/{featureId}` · operation `remove-plan-feature`

Detach a feature from a plan.

### Parameters

- `id` (`str`, required)
- `feature_id` (`str`, required)

### Returns

`RemovedPlanFeature`

## add_feature

`commet.plans.add_feature(...)`

`POST /plans/{id}/features` · operation `add-plan-feature`

Attach a feature to a plan with limits, overage, and credits configuration.

### Parameters

- `id` (`str`, required)
- `feature_id` (`str`, required)
- `enabled` (`bool`, optional)
- `included_amount` (`int`, optional)
- `unlimited` (`bool`, optional)
- `overage` (`AddPlanFeatureParamsOverage`, optional)
- `credits_per_unit` (`int | null`, optional)
- `pricing_mode` (`Literal["fixed", "ai_model"]`, optional)
- `margin` (`int | null`, optional)

### Request options

- `idempotency_key` (`str`, optional) — Unique key used to safely retry this write for 24 hours without applying it twice.

### Returns

`PlanFeature`

## set_default_price

`commet.plans.set_default_price(...)`

`PUT /plans/{id}/prices/{priceId}/default` · operation `set-default-plan-price`

Set a specific price as the default and return the updated plan price.

### Parameters

- `id` (`str`, required)
- `price_id` (`str`, required)

### Request options

- `idempotency_key` (`str`, optional) — Unique key used to safely retry this write for 24 hours without applying it twice.

### Returns

`PlanPrice`

## set_regional_prices

`commet.plans.set_regional_prices(...)`

`PUT /plans/{id}/prices/{priceId}/regional` · operation `upsert-regional-prices`

Create or update regional currency price overrides for a plan price.

### Parameters

- `id` (`str`, required)
- `price_id` (`str`, required)
- `overrides` (`list[UpsertRegionalPricesParamsOverridesItem]`, required)

### Request options

- `idempotency_key` (`str`, optional) — Unique key used to safely retry this write for 24 hours without applying it twice.

### Returns

`PlanRegionalPricing`

## delete_regional_prices

`commet.plans.delete_regional_prices(...)`

`DELETE /plans/{id}/prices/{priceId}/regional` · operation `delete-regional-prices`

Remove all regional currency overrides for a plan price. The request is rejected while billable subscriptions depend on an override.

### Parameters

- `id` (`str`, required)
- `price_id` (`str`, required)

### Returns

`DeletedPlanRegionalPricing`

## update_price

`commet.plans.update_price(...)`

`PATCH /plans/{id}/prices/{priceId}` · operation `update-plan-price`

Update a base price or market price variant. Removing a base market override is rejected while a variant depends on it. Offer terms are managed through Offers.

### Parameters

- `id` (`str`, required)
- `price_id` (`str`, required)
- `price` (`int`, optional)
- `is_default` (`bool`, optional)
- `trial_days` (`int`, optional)
- `included_balance` (`int | null`, optional)
- `included_credits` (`int | null`, optional)
- `metadata` (`dict[str, Any]`, optional) — Metadata keys to merge into the existing price metadata.
- `market_prices` (`list[UpdatePlanPriceParamsMarketPricesItem]`, optional)

### Request options

- `idempotency_key` (`str`, optional) — Unique key used to safely retry this write for 24 hours without applying it twice.

### Returns

`PlanPrice`

## delete_price

`commet.plans.delete_price(...)`

`DELETE /plans/{id}/prices/{priceId}` · operation `delete-plan-price`

Archive a price for new subscriptions. Existing subscriptions that selected it continue using its current catalog value.

### Parameters

- `id` (`str`, required)
- `price_id` (`str`, required)

### Returns

`DeletedObject`

## add_price

`commet.plans.add_price(...)`

`POST /plans/{id}/prices` · operation `add-plan-price`

Add a base price or a selectable market price variant. Variants inherit their base price outside the markets they override. Configure introductory and promotional benefits through Offers.

### Parameters

- `id` (`str`, required)
- `billing_interval` (`Literal["weekly", "monthly", "quarterly", "yearly", "one_time"]`, required)
- `metadata` (`dict[str, Any]`, optional)
- `price` (`int`, optional)
- `trial_days` (`int`, optional)
- `is_default` (`bool`, optional)
- `included_balance` (`int | null`, optional)
- `included_credits` (`int | null`, optional)
- `market_prices` (`list[AddPlanPriceParamsMarketPricesItem]`, optional)
- `inherits_from_price_id` (`str`, optional)

### Request options

- `idempotency_key` (`str`, optional) — Unique key used to safely retry this write for 24 hours without applying it twice.

### Returns

`PlanPrice`

## set_regional_pricing

`commet.plans.set_regional_pricing(...)`

`PUT /plans/{id}/regional` · operation `set-plan-regional-pricing`

Configure regional prices and feature overage values for one currency. Currency-specific offer terms are managed through Offers.

### Parameters

- `id` (`str`, required)
- `currency` (`Literal["usd", "ars", "brl", "clp", "cop", "pen", "uyu", "pyg", "bob", "mxn", "cad", "eur", "jpy", "cny", "krw", "hkd", "sgd", "twd", "inr", "thb"]`, required)
- `exchange_rate` (`float`, required)
- `prices` (`list[SetPlanRegionalPricingParamsPricesItem]`, optional)
- `features` (`list[SetPlanRegionalPricingParamsFeaturesItem]`, optional)

### Request options

- `idempotency_key` (`str`, optional) — Unique key used to safely retry this write for 24 hours without applying it twice.

### Returns

`PlanRegionalPricingResult`

## get

`commet.plans.get(...)`

`GET /plans/{id}` · operation `get-plan`

Get a plan with public price IDs and their automatic introductory offer IDs.

### Parameters

- `id` (`str`, required)

### Returns

`Plan`

## update

`commet.plans.update(...)`

`PATCH /plans/{id}` · operation `update-plan`

Update a plan's name, description, visibility, or metadata.

### Parameters

- `id` (`str`, required)
- `name` (`str`, optional)
- `description` (`str | null`, optional)
- `metadata` (`dict[str, Any]`, optional)
- `is_public` (`bool`, optional)

### Request options

- `idempotency_key` (`str`, optional) — Unique key used to safely retry this write for 24 hours without applying it twice.

### Returns

`Plan`

## delete

`commet.plans.delete(...)`

`DELETE /plans/{id}` · operation `delete-plan`

Soft-delete a plan.

### Parameters

- `id` (`str`, required)

### Returns

`DeletedObject`

## set_visibility

`commet.plans.set_visibility(...)`

`PUT /plans/{id}/visibility` · operation `set-plan-visibility`

Set a plan's public visibility and return the updated plan.

### Parameters

- `id` (`str`, required)
- `is_public` (`bool`, required)

### Request options

- `idempotency_key` (`str`, optional) — Unique key used to safely retry this write for 24 hours without applying it twice.

### Returns

`Plan`

## list

`commet.plans.list(...)`

`GET /plans` · operation `list-plans`

List plans with public price IDs and their automatic introductory offer IDs.

### Parameters

- `include_private` (`bool`, optional)

### Returns

`PlansListResult`

## create

`commet.plans.create(...)`

`POST /plans` · operation `create-plan`

Create a new plan with optional consumption model, visibility, and plan group assignment.

### Parameters

- `name` (`str`, required)
- `code` (`str`, required)
- `description` (`str`, optional)
- `consumption_model` (`Literal["metered", "credits", "balance"]`, optional)
- `is_public` (`bool`, optional)
- `is_free` (`bool`, optional)
- `block_on_exhaustion` (`bool`, optional)
- `plan_group_id` (`str`, optional)
- `metadata` (`dict[str, Any]`, optional)

### Request options

- `idempotency_key` (`str`, optional) — Unique key used to safely retry this write for 24 hours without applying it twice.

### Returns

`Plan`
