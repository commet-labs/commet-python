# Schemas

Generated from Commet API version `2026-07-31`.

## Enums

### BillingInterval

- `"weekly"`
- `"monthly"`
- `"quarterly"`
- `"yearly"`
- `"one_time"`

### ConsumptionModel

- `"metered"`
- `"credits"`
- `"balance"`

### FeatureType

- `"boolean"`
- `"usage"`
- `"seats"`
- `"quota"`

### InvoiceType

- `"recurring"`
- `"overage"`
- `"plan_change"`
- `"adjustment"`
- `"credit_purchase"`
- `"balance_topup"`
- `"addon_activation"`
- `"one_time_payment"`
- `"reactivation"`

### PaymentProvider

- `"stripe"`
- `"commet"`
- `"dlocal"`

### SubscriptionStatus

- `"draft"`
- `"pending_payment"`
- `"trialing"`
- `"active"`
- `"past_due"`
- `"canceled"`

### Timezone

- `"UTC"`
- `"America/New_York"`
- `"America/Chicago"`
- `"America/Denver"`
- `"America/Los_Angeles"`
- `"America/Sao_Paulo"`
- `"America/Mexico_City"`
- `"America/Buenos_Aires"`
- `"America/Santiago"`
- `"America/Bogota"`
- `"America/Lima"`
- `"America/Asuncion"`
- `"Europe/London"`
- `"Europe/Paris"`
- `"Europe/Berlin"`
- `"Europe/Madrid"`
- `"Asia/Tokyo"`
- `"Asia/Shanghai"`
- `"Asia/Singapore"`
- `"Asia/Dubai"`
- `"Australia/Sydney"`

### TransactionStatus

- `"pending"`
- `"succeeded"`
- `"failed"`
- `"refunded"`
- `"disputed"`

## Models

### ActiveAddon

- `slug` (`str`, required)
- `name` (`str`, required)
- `base_price` (`int`, required)
- `feature_code` (`str`, required)
- `feature_name` (`str`, required)
- `feature_type` (`FeatureType`, required)
- `consumption_model` (`Literal["boolean", "metered", "credits", "balance"]`, required)
- `activated_at` (`str`, required)
- `object` (`Literal["subscription_addon"]`, required)
- `livemode` (`bool`, required)

### AddedPlanToGroup

- `success` (`bool`, required)
- `object` (`Literal["plan_group_membership"]`, required)
- `livemode` (`bool`, required)

### Addon

- `id` (`str`, required)
- `name` (`str`, required)
- `slug` (`str`, required)
- `description` (`str | null`, required)
- `base_price` (`int`, required)
- `feature_code` (`str`, required)
- `feature_name` (`str`, required)
- `created_at` (`str`, required)
- `updated_at` (`str`, required)
- `consumption_model` (`Literal["boolean", "metered", "credits", "balance"]`, required)
- `included_units` (`int | null`, required)
- `overage_rate` (`int | null`, required)
- `credit_cost` (`int | null`, required)
- `object` (`Literal["addon"]`, required)
- `livemode` (`bool`, required)

### AddonsListActiveResult

- `object` (`Literal["list"]`, required)
- `data` (`list[ActiveAddon]`, required)
- `has_more` (`bool`, required)
- `next_cursor` (`str`, optional)

### AddonsListResult

- `object` (`Literal["list"]`, required)
- `data` (`list[Addon]`, required)
- `has_more` (`bool`, required)
- `next_cursor` (`str`, optional)

### AddPlanFeatureParamsOverage

- `enabled` (`bool`, optional)
- `unit_price` (`int`, optional)

### AddPlanPriceParamsMarketPricesItem

- `market_group_id` (`str`, required) — Public ID of a reusable pricing market group.
- `currency` (`Literal["usd", "ars", "brl", "clp", "cop", "pen", "uyu", "pyg", "bob", "mxn", "cad", "eur", "gbp", "jpy", "cny", "krw", "hkd", "sgd", "twd", "inr", "thb"]`, required) — Presentment currency configured for this plan and market.
- `price` (`int`, required) — Market price in the currency's minor unit.

### ApiKey

- `id` (`str`, required)
- `name` (`str`, required)
- `prefix` (`str`, required)
- `expires_at` (`str | null`, required)
- `last_used_at` (`str | null`, required)
- `created_at` (`str`, required)
- `object` (`Literal["api_key"]`, required)
- `livemode` (`bool`, required)

### ApiKeysListResult

- `object` (`Literal["list"]`, required)
- `data` (`list[ApiKey]`, required)
- `has_more` (`bool`, required)
- `next_cursor` (`str`, optional)

### BalanceAdjustment

- `amount` (`int`, required)
- `new_balance` (`int`, required)
- `reason` (`str | null`, required)
- `object` (`Literal["balance_transaction"]`, required)
- `livemode` (`bool`, required)

### BalanceTopup

- `amount` (`int`, required)
- `object` (`Literal["balance_topup"]`, required)
- `livemode` (`bool`, required)

### BatchCreateCustomersParamsCustomersItem

- `email` (`str`, required)
- `id` (`str`, optional)
- `external_id` (`str`, optional)
- `full_name` (`str`, optional)
- `tax_document` (`str`, optional)
- `timezone` (`Timezone`, optional)
- `metadata` (`dict[str, Any]`, optional)
- `address` (`BatchCreateCustomersParamsCustomersItemAddress`, optional)

### BatchCreateCustomersParamsCustomersItemAddress

- `line1` (`str`, required)
- `line2` (`str`, optional)
- `city` (`str`, required)
- `state` (`str`, optional)
- `postal_code` (`str`, required)
- `country` (`str`, required)
- `region` (`str`, optional)

### ClaimLink

- `url` (`str`, required)
- `expires_at` (`str`, required)
- `object` (`Literal["claim_link"]`, required)
- `livemode` (`bool`, required)

### CreateCustomerParamsAddress

- `line1` (`str`, required)
- `line2` (`str`, optional)
- `city` (`str`, required)
- `state` (`str`, optional)
- `postal_code` (`str`, required)
- `country` (`str`, required)
- `region` (`str`, optional)

### CreatedApiKey

- `id` (`str`, required)
- `name` (`str`, required)
- `api_key` (`str`, required)
- `prefix` (`str`, required)
- `expires_at` (`str`, required)
- `created_at` (`str`, required)
- `object` (`Literal["api_key"]`, required)
- `livemode` (`bool`, required)

### CreatedSubscription

- `id` (`str`, required)
- `customer_id` (`str`, required)
- `plan` (`CreatedSubscriptionPlan`, required)
- `name` (`str`, required)
- `description` (`str | null`, required)
- `status` (`SubscriptionStatus`, required)
- `billing_interval` (`BillingInterval | null`, required)
- `trial_ends_at` (`str | null`, required)
- `current_period` (`CreatedSubscriptionCurrentPeriod | null`, required)
- `cancellation` (`CreatedSubscriptionCancellation | null`, required)
- `cancel_at_period_end` (`bool`, required)
- `scheduled_plan_change` (`CreatedSubscriptionScheduledPlanChange | null`, required)
- `start_date` (`str`, required)
- `end_date` (`str | null`, required)
- `billing_day_of_month` (`int | null`, required)
- `next_billing_date` (`str | null`, required)
- `checkout_url` (`str | null`, required)
- `created_at` (`str`, required)
- `updated_at` (`str`, required)
- `offer_applications` (`list[SubscriptionOfferApplication]`, required)
- `checkout_provider` (`PaymentProvider | null`, required) — Payment provider resolved for this checkout when the subscription response was created. This is an informational snapshot and may differ when the checkout is loaded if its country or the organization's routing changes.
- `price_id` (`str | null`, required)
- `object` (`Literal["subscription"]`, required)
- `livemode` (`bool`, required)

### CreatedSubscriptionCancellation

- `scheduled_at` (`str`, required)
- `reason` (`str | null`, required)
- `effective_at` (`str`, required)

### CreatedSubscriptionCurrentPeriod

- `start` (`str`, required)
- `end` (`str`, required)
- `days_remaining` (`float`, required)

### CreatedSubscriptionPlan

- `id` (`str`, required)
- `name` (`str`, required)

### CreatedSubscriptionScheduledPlanChange

- `change_type` (`Literal["plan_downgrade", "interval_change"]`, required)
- `new_plan_id` (`str | null`, required)
- `new_plan_name` (`str | null`, required)
- `new_billing_interval` (`str | null`, required)
- `scheduled_for` (`str`, required)

### CreatedWebhook

- `id` (`str`, required)
- `url` (`str`, required)
- `events` (`list[str]`, required)
- `description` (`str | null`, required)
- `is_active` (`bool`, required)
- `api_version` (`str | null`, required)
- `created_at` (`str`, required)
- `secret_key` (`str`, required)
- `object` (`Literal["webhook"]`, required)
- `livemode` (`bool`, required)

### CreateOfferParamsPhasesItem

Variants:

- `CreateOfferParamsPhasesItemVariant1`
- `CreateOfferParamsPhasesItemVariant2`
- `CreateOfferParamsPhasesItemVariant3`
- `CreateOfferParamsPhasesItemVariant4`

Discriminator: `type`

- `"free_trial"` → `CreateOfferParamsPhasesItemVariant1`
- `"percentage"` → `CreateOfferParamsPhasesItemVariant2`
- `"amount_off"` → `CreateOfferParamsPhasesItemVariant3`
- `"fixed_price"` → `CreateOfferParamsPhasesItemVariant4`

### CreateOfferParamsPhasesItemVariant1

- `type` (`Literal["free_trial"]`, required)
- `duration_days` (`int`, required)

### CreateOfferParamsPhasesItemVariant2

- `type` (`Literal["percentage"]`, required)
- `duration_cycles` (`int | null`, required)
- `duration_interval` (`Literal["weekly", "monthly", "quarterly", "yearly"] | null`, optional) — Unit the phase duration is counted in. Only a fixed-price phase may set it, because its amount is declared rather than derived from the plan. Defaults to the plan's own billing interval.
- `percentage` (`int`, required) — Discount in basis points. 5000 means 50%.

### CreateOfferParamsPhasesItemVariant3

- `type` (`Literal["amount_off"]`, required)
- `duration_cycles` (`int | null`, required)
- `duration_interval` (`Literal["weekly", "monthly", "quarterly", "yearly"] | null`, optional) — Unit the phase duration is counted in. Only a fixed-price phase may set it, because its amount is declared rather than derived from the plan. Defaults to the plan's own billing interval.
- `amounts` (`list[CreateOfferParamsPhasesItemVariant3AmountsItem]`, required)

### CreateOfferParamsPhasesItemVariant3AmountsItem

- `currency` (`str`, required)
- `amount` (`int`, required) — Amount in the currency's minor unit (for example, cents for USD).

### CreateOfferParamsPhasesItemVariant4

- `type` (`Literal["fixed_price"]`, required)
- `duration_cycles` (`int | null`, required)
- `duration_interval` (`Literal["weekly", "monthly", "quarterly", "yearly"] | null`, optional) — Unit the phase duration is counted in. Only a fixed-price phase may set it, because its amount is declared rather than derived from the plan. Defaults to the plan's own billing interval.
- `prices` (`list[CreateOfferParamsPhasesItemVariant4PricesItem]`, required)

### CreateOfferParamsPhasesItemVariant4PricesItem

- `currency` (`str`, required)
- `amount` (`int`, required) — Amount in the currency's minor unit (for example, cents for USD).

### CreditGrant

- `credits` (`int`, required)
- `object` (`Literal["credit_grant"]`, required)
- `livemode` (`bool`, required)

### CreditPack

- `id` (`str`, required)
- `name` (`str`, required)
- `description` (`str | null`, required)
- `credits` (`int`, required)
- `price` (`int`, required)
- `is_active` (`bool`, required)
- `created_at` (`str`, required)
- `updated_at` (`str`, required)
- `object` (`Literal["credit_pack"]`, required)
- `livemode` (`bool`, required)

### CreditPackListItem

- `id` (`str`, required)
- `name` (`str`, required)
- `description` (`str | null`, required)
- `credits` (`int`, required)
- `price` (`int`, required)
- `currency` (`str`, required)
- `object` (`Literal["credit_pack"]`, required)
- `livemode` (`bool`, required)

### CreditPacksListResult

- `object` (`Literal["list"]`, required)
- `data` (`list[CreditPackListItem]`, required)
- `has_more` (`bool`, required)
- `next_cursor` (`str`, optional)

### Customer

- `id` (`str`, required)
- `external_id` (`str | null`, required)
- `full_name` (`str | null`, required)
- `email` (`str`, required)
- `tax_document` (`str | null`, required)
- `document_type` (`str | null`, required)
- `timezone` (`str | null`, required)
- `metadata` (`dict[str, Any] | null`, required)
- `created_at` (`str`, required)
- `updated_at` (`str`, required)
- `object` (`Literal["customer"]`, required)
- `livemode` (`bool`, required)

### CustomerBatch

- `successful` (`list[CustomerBatchSuccessfulItem]`, required)
- `failed` (`list[CustomerBatchFailedItem]`, required)
- `object` (`Literal["customer_batch"]`, required)
- `livemode` (`bool`, required)

### CustomerBatchFailedItem

- `index` (`int`, required)
- `error` (`str`, required)
- `data` (`CustomerBatchFailedItemData`, required)

### CustomerBatchFailedItemData

- `id` (`str`, optional)
- `external_id` (`str`, optional)
- `email` (`str`, required)
- `full_name` (`str | null`, optional)
- `tax_document` (`str | null`, optional)
- `timezone` (`str`, optional)
- `metadata` (`dict[str, Any] | null`, optional)
- `address` (`CustomerBatchFailedItemDataAddress`, optional)

### CustomerBatchFailedItemDataAddress

- `line1` (`str`, required)
- `line2` (`str`, optional)
- `city` (`str`, required)
- `state` (`str`, optional)
- `postal_code` (`str`, required)
- `country` (`str`, required)
- `region` (`str`, optional)

### CustomerBatchSuccessfulItem

- `id` (`str`, required)
- `external_id` (`str | null`, required)
- `email` (`str`, required)

### CustomerCredit

- `id` (`str`, required)
- `amount` (`int`, required) — Original grant amount in the currency's smallest unit.
- `applied_amount` (`int`, required)
- `reversed_amount` (`int`, required)
- `revoked_amount` (`int`, required)
- `remaining_amount` (`int`, required)
- `currency` (`str`, required)
- `reason` (`str`, required)
- `source` (`Literal["dashboard", "api", "plan_change", "migration"]`, required)
- `expires_at` (`str | null`, required)
- `created_at` (`str`, required)
- `object` (`Literal["customer_credit"]`, required)
- `livemode` (`bool`, required)

### CustomerCreditRevocation

- `id` (`str`, required)
- `remaining_amount` (`int`, required)
- `revoked_amount` (`int`, required)
- `currency` (`str`, required)
- `object` (`Literal["customer_credit"]`, required)
- `livemode` (`bool`, required)

### CustomersListCreditsResult

- `object` (`Literal["list"]`, required)
- `data` (`list[CustomerCredit]`, required)
- `has_more` (`bool`, required)
- `next_cursor` (`str`, optional)

### CustomersListPlanGrantsResult

- `object` (`Literal["list"]`, required)
- `data` (`list[PlanGrant]`, required)
- `has_more` (`bool`, required)
- `next_cursor` (`str`, optional)

### CustomersListResult

- `object` (`Literal["list"]`, required)
- `data` (`list[Customer]`, required)
- `has_more` (`bool`, required)
- `next_cursor` (`str`, optional)

### DeletedObject

- `id` (`str`, required)
- `deleted` (`Literal[True]`, required)
- `object` (`str`, required)
- `livemode` (`bool`, required)

### DeletedOffer

- `deleted` (`Literal[True]`, required)
- `object` (`Literal["offer"]`, required)
- `livemode` (`bool`, required)

### DeletedPlanRegionalPricing

- `deleted` (`Literal[True]`, required)
- `object` (`Literal["plan_regional_pricing"]`, required)
- `livemode` (`bool`, required)

### DeletedSubscriptionAddon

- `id` (`str`, required)
- `status` (`Literal["inactive"]`, required)
- `deactivated_at` (`str | null`, required)
- `object` (`Literal["subscription_addon"]`, required)
- `livemode` (`bool`, required)

### Feature

- `id` (`str`, required)
- `name` (`str`, required)
- `code` (`str`, required)
- `type` (`FeatureType`, required)
- `description` (`str | null`, required)
- `unit_name` (`str | null`, required)
- `created_at` (`str`, required)
- `updated_at` (`str`, required)
- `object` (`Literal["feature"]`, required)
- `livemode` (`bool`, required)

### FeatureAccess

Variants:

- `FeatureAccessVariant1`
- `FeatureAccessVariant2`
- `FeatureAccessVariant3`
- `FeatureAccessVariant4`

Discriminator: `type`

- `"boolean"` → `FeatureAccessVariant1`
- `"usage"` → `FeatureAccessVariant2`
- `"seats"` → `FeatureAccessVariant3`
- `"quota"` → `FeatureAccessVariant4`

### FeatureAccessListResult

- `object` (`Literal["list"]`, required)
- `data` (`list[FeatureAccess]`, required)
- `has_more` (`bool`, required)
- `next_cursor` (`str`, optional)

### FeatureAccessVariant1

- `code` (`str`, required) — Unique feature code.
- `name` (`str`, required) — Display name of the feature.
- `unit_name` (`str | null`, required) — Display name for one product unit, or null when not applicable.
- `allowed` (`bool`, required) — Whether the customer can currently access or consume the feature.
- `type` (`Literal["boolean"]`, required)
- `enabled` (`bool`, required) — Whether the feature is enabled.
- `base_access` (`FeatureAccessVariant1BaseAccess | null`, optional)
- `object` (`Literal["feature_access"]`, required)
- `livemode` (`bool`, required)

### FeatureAccessVariant1BaseAccess

- `enabled` (`bool`, required)

### FeatureAccessVariant2

- `code` (`str`, required) — Unique feature code.
- `name` (`str`, required) — Display name of the feature.
- `unit_name` (`str | null`, required) — Display name for one product unit, or null when not applicable.
- `allowed` (`bool`, required) — Whether the customer can currently access or consume the feature.
- `type` (`Literal["usage"]`, required)
- `consumption` (`FeatureAccessVariant2Consumption`, required)
- `base_access` (`FeatureAccessVariant2BaseAccess | null`, optional)
- `object` (`Literal["feature_access"]`, required)
- `livemode` (`bool`, required)

### FeatureAccessVariant2BaseAccess

- `included_units` (`float`, required)
- `unlimited` (`bool`, required)

### FeatureAccessVariant2Consumption

Variants:

- `FeatureAccessVariant2ConsumptionVariant1`
- `FeatureAccessVariant2ConsumptionVariant2`
- `FeatureAccessVariant2ConsumptionVariant3`

Discriminator: `model`

- `"metered"` → `FeatureAccessVariant2ConsumptionVariant1`
- `"credits"` → `FeatureAccessVariant2ConsumptionVariant2`
- `"balance"` → `FeatureAccessVariant2ConsumptionVariant3`

### FeatureAccessVariant2ConsumptionVariant1

- `model` (`Literal["metered"]`, required) — Usage is measured against an included allowance and overage.
- `period` (`FeatureAccessVariant2ConsumptionVariant1Period`, required) — Time range used to calculate this feature's consumption.
- `units_used` (`float`, required) — Product units recorded during the period.
- `included_units` (`float`, required) — Product units included in the subscription for the period.
- `remaining_units` (`float`, optional) — Included units not yet consumed. Absent when usage is unlimited.
- `unlimited` (`bool`, required) — Whether the feature has no usage limit.
- `overage` (`FeatureAccessVariant2ConsumptionVariant1Overage`, required)

### FeatureAccessVariant2ConsumptionVariant1Overage

- `enabled` (`bool`, required) — Whether usage above the included amount is allowed and billed.
- `units` (`float`, required) — Units consumed above the included amount.
- `unit_price` (`FeatureAccessVariant2ConsumptionVariant1OverageUnitPrice`, optional) — Price for one additional product unit.

### FeatureAccessVariant2ConsumptionVariant1OverageUnitPrice

- `amount` (`int`, required) — Integer rate amount. Divide by scale to obtain the price.
- `currency` (`str`, required) — Lowercase ISO 4217 currency code.
- `scale` (`Literal[10000]`, required) — Divide amount by scale to obtain the major-unit price.

### FeatureAccessVariant2ConsumptionVariant1Period

- `start` (`str`, required) — Inclusive usage period start.
- `end` (`str`, required) — Exclusive usage period end.

### FeatureAccessVariant2ConsumptionVariant2

- `model` (`Literal["credits"]`, required) — Product usage consumes credits from a shared pool.
- `period` (`FeatureAccessVariant2ConsumptionVariant2Period`, required) — Time range used to calculate this feature's consumption.
- `units_used` (`float`, required) — Product units recorded during the period.
- `credits_per_unit` (`int`, required) — Credits deducted for each product unit.
- `credits_consumed` (`float`, required) — Actual credits deducted by this feature during the period.
- `available_units` (`int`, required) — Additional product units available from the current shared credit pool at this feature's conversion rate.

### FeatureAccessVariant2ConsumptionVariant2Period

- `start` (`str`, required) — Inclusive usage period start.
- `end` (`str`, required) — Exclusive usage period end.

### FeatureAccessVariant2ConsumptionVariant3

- `model` (`Literal["balance"]`, required) — Product usage deducts money from a shared balance.
- `period` (`FeatureAccessVariant2ConsumptionVariant3Period`, required) — Time range used to calculate this feature's consumption.
- `units_used` (`float`, required) — Product units recorded during the period.
- `spent` (`FeatureAccessVariant2ConsumptionVariant3Spent`, required) — Actual money deducted for this feature during the period.
- `available_units` (`int`, optional) — Estimated additional units available from the current shared balance at this feature's fixed price. Absent for dynamic pricing.
- `unit_price` (`FeatureAccessVariant2ConsumptionVariant3UnitPrice`, optional) — Price for one additional product unit.

### FeatureAccessVariant2ConsumptionVariant3Period

- `start` (`str`, required) — Inclusive usage period start.
- `end` (`str`, required) — Exclusive usage period end.

### FeatureAccessVariant2ConsumptionVariant3Spent

- `amount` (`int`, required) — Amount in the currency's smallest unit.
- `currency` (`str`, required) — Lowercase ISO 4217 currency code.

### FeatureAccessVariant2ConsumptionVariant3UnitPrice

- `amount` (`int`, required) — Integer rate amount. Divide by scale to obtain the price.
- `currency` (`str`, required) — Lowercase ISO 4217 currency code.
- `scale` (`Literal[10000]`, required) — Divide amount by scale to obtain the major-unit price.

### FeatureAccessVariant3

- `code` (`str`, required) — Unique feature code.
- `name` (`str`, required) — Display name of the feature.
- `unit_name` (`str | null`, required) — Display name for one product unit, or null when not applicable.
- `allowed` (`bool`, required) — Whether the customer can currently access or consume the feature.
- `type` (`Literal["seats"]`, required)
- `usage` (`FeatureAccessVariant3Usage`, required)
- `base_access` (`FeatureAccessVariant3BaseAccess | null`, optional)
- `object` (`Literal["feature_access"]`, required)
- `livemode` (`bool`, required)

### FeatureAccessVariant3BaseAccess

- `included_units` (`float`, required)
- `unlimited` (`bool`, required)

### FeatureAccessVariant3Usage

- `period` (`FeatureAccessVariant3UsagePeriod`, required) — Time range used to calculate this feature's consumption.
- `units_used` (`float`, required) — Current units assigned or in use.
- `included_units` (`float`, required) — Units included in the subscription for the period.
- `remaining_units` (`float`, optional) — Included units still available. Absent when usage is unlimited.
- `unlimited` (`bool`, required) — Whether the feature has no usage limit.
- `overage` (`FeatureAccessVariant3UsageOverage`, required)

### FeatureAccessVariant3UsageOverage

- `enabled` (`bool`, required) — Whether usage above the included amount is allowed and billed.
- `units` (`float`, required) — Units consumed above the included amount.
- `unit_price` (`FeatureAccessVariant3UsageOverageUnitPrice`, optional) — Price for one additional product unit.

### FeatureAccessVariant3UsageOverageUnitPrice

- `amount` (`int`, required) — Integer rate amount. Divide by scale to obtain the price.
- `currency` (`str`, required) — Lowercase ISO 4217 currency code.
- `scale` (`Literal[10000]`, required) — Divide amount by scale to obtain the major-unit price.

### FeatureAccessVariant3UsagePeriod

- `start` (`str`, required) — Inclusive usage period start.
- `end` (`str`, required) — Exclusive usage period end.

### FeatureAccessVariant4

- `code` (`str`, required) — Unique feature code.
- `name` (`str`, required) — Display name of the feature.
- `unit_name` (`str | null`, required) — Display name for one product unit, or null when not applicable.
- `allowed` (`bool`, required) — Whether the customer can currently access or consume the feature.
- `type` (`Literal["quota"]`, required)
- `usage` (`FeatureAccessVariant4Usage`, required)
- `base_access` (`FeatureAccessVariant4BaseAccess | null`, optional)
- `object` (`Literal["feature_access"]`, required)
- `livemode` (`bool`, required)

### FeatureAccessVariant4BaseAccess

- `included_units` (`float`, required)
- `unlimited` (`bool`, required)

### FeatureAccessVariant4Usage

- `period` (`FeatureAccessVariant4UsagePeriod`, required) — Time range used to calculate this feature's consumption.
- `units_used` (`float`, required) — Current units assigned or in use.
- `included_units` (`float`, required) — Units included in the subscription for the period.
- `remaining_units` (`float`, optional) — Included units still available. Absent when usage is unlimited.
- `unlimited` (`bool`, required) — Whether the feature has no usage limit.
- `overage` (`FeatureAccessVariant4UsageOverage`, required)
- `billed_units` (`float`, required) — Highest quota reached during the period and used for billing.

### FeatureAccessVariant4UsageOverage

- `enabled` (`bool`, required) — Whether usage above the included amount is allowed and billed.
- `units` (`float`, required) — Units consumed above the included amount.
- `unit_price` (`FeatureAccessVariant4UsageOverageUnitPrice`, optional) — Price for one additional product unit.

### FeatureAccessVariant4UsageOverageUnitPrice

- `amount` (`int`, required) — Integer rate amount. Divide by scale to obtain the price.
- `currency` (`str`, required) — Lowercase ISO 4217 currency code.
- `scale` (`Literal[10000]`, required) — Divide amount by scale to obtain the major-unit price.

### FeatureAccessVariant4UsagePeriod

- `start` (`str`, required) — Inclusive usage period start.
- `end` (`str`, required) — Exclusive usage period end.

### FeaturesListResult

- `object` (`Literal["list"]`, required)
- `data` (`list[Feature]`, required)
- `has_more` (`bool`, required)
- `next_cursor` (`str`, optional)

### Invoice

- `id` (`str`, required)
- `customer_id` (`str`, required)
- `subscription_id` (`str | null`, required)
- `invoice_number` (`str`, required)
- `status` (`Literal["draft", "outstanding", "paid", "void", "uncollectible"]`, required)
- `invoice_type` (`InvoiceType`, required)
- `currency` (`str`, required)
- `subtotal` (`int`, required)
- `discount_amount` (`int`, required)
- `tax_amount` (`int`, required)
- `total` (`int`, required)
- `period_start` (`str`, required)
- `period_end` (`str`, required)
- `issue_date` (`str`, required)
- `due_date` (`str`, required)
- `memo` (`str | null`, required)
- `metadata` (`dict[str, Any]`, required)
- `created_at` (`str`, required)
- `updated_at` (`str`, required)
- `credit_applied` (`int`, required)
- `plan_name` (`str | null`, required)
- `po_number` (`str | null`, required)
- `reference` (`str | null`, required)
- `line_items` (`list[InvoiceLineItemsItem]`, required)
- `object` (`Literal["invoice"]`, required)
- `livemode` (`bool`, required)

### InvoiceDownload

- `url` (`str`, required)
- `expires_at` (`str`, required)
- `object` (`Literal["invoice_download_link"]`, required)
- `livemode` (`bool`, required)

### InvoiceLineItemsItem

- `line_type` (`Literal["plan_base", "feature_overage", "feature_seats", "feature_quota", "discount", "promo_code_discount", "credit", "balance_overage", "addon_base", "one_time"]`, required)
- `feature_name` (`str | null`, required)
- `description` (`str`, required)
- `quantity` (`int`, required)
- `unit_amount` (`int`, required)
- `amount` (`int`, required)
- `included_amount` (`int | null`, required)
- `used_amount` (`int | null`, required)
- `overage_amount` (`int | null`, required)
- `discount_type` (`str | null`, required)
- `discount_value` (`int | null`, required)
- `discount_name` (`str | null`, required)
- `charge_type` (`Literal["standard", "advance", "true_up"]`, required)

### InvoiceListItem

- `id` (`str`, required)
- `customer_id` (`str`, required)
- `subscription_id` (`str | null`, required)
- `invoice_number` (`str`, required)
- `status` (`Literal["draft", "outstanding", "paid", "void", "uncollectible"]`, required)
- `invoice_type` (`InvoiceType`, required)
- `currency` (`str`, required)
- `subtotal` (`int`, required)
- `discount_amount` (`int`, required)
- `tax_amount` (`int`, required)
- `total` (`int`, required)
- `period_start` (`str`, required)
- `period_end` (`str`, required)
- `issue_date` (`str`, required)
- `due_date` (`str`, required)
- `memo` (`str | null`, required)
- `metadata` (`dict[str, Any]`, required)
- `created_at` (`str`, required)
- `updated_at` (`str`, required)
- `object` (`Literal["invoice"]`, required)
- `livemode` (`bool`, required)

### InvoicesListResult

- `object` (`Literal["list"]`, required)
- `data` (`list[InvoiceListItem]`, required)
- `has_more` (`bool`, required)
- `next_cursor` (`str`, optional)

### Market

- `id` (`str`, required)
- `name` (`str`, required)
- `country_codes` (`list[str]`, required)
- `metadata` (`dict[str, Any]`, required)
- `created_at` (`str`, required)
- `updated_at` (`str`, required)
- `object` (`Literal["market"]`, required)
- `livemode` (`bool`, required)

### MarketsListResult

- `object` (`Literal["list"]`, required)
- `data` (`list[Market]`, required)
- `has_more` (`bool`, required)
- `next_cursor` (`str`, optional)

### Offer

- `id` (`str`, required)
- `name` (`str`, required)
- `phases` (`list[OfferPhasesItem]`, required)
- `metadata` (`dict[str, Any]`, required)
- `starts_at` (`str | null`, required)
- `ends_at` (`str | null`, required)
- `active` (`bool`, required)
- `created_at` (`str`, required)
- `updated_at` (`str`, required)
- `object` (`Literal["offer"]`, required)
- `livemode` (`bool`, required)

### OfferPhasesItem

Variants:

- `OfferPhasesItemVariant1`
- `OfferPhasesItemVariant2`
- `OfferPhasesItemVariant3`
- `OfferPhasesItemVariant4`

Discriminator: `type`

- `"free_trial"` → `OfferPhasesItemVariant1`
- `"percentage"` → `OfferPhasesItemVariant2`
- `"amount_off"` → `OfferPhasesItemVariant3`
- `"fixed_price"` → `OfferPhasesItemVariant4`

### OfferPhasesItemVariant1

- `type` (`Literal["free_trial"]`, required)
- `duration_days` (`int`, required)

### OfferPhasesItemVariant2

- `type` (`Literal["percentage"]`, required)
- `duration_cycles` (`int | null`, required)
- `duration_interval` (`Literal["weekly", "monthly", "quarterly", "yearly"] | null`, required) — Unit the phase duration is counted in. Only a fixed-price phase may set it, because its amount is declared rather than derived from the plan. Defaults to the plan's own billing interval.
- `percentage` (`int`, required) — Discount in basis points. 5000 means 50%.

### OfferPhasesItemVariant3

- `type` (`Literal["amount_off"]`, required)
- `duration_cycles` (`int | null`, required)
- `duration_interval` (`Literal["weekly", "monthly", "quarterly", "yearly"] | null`, required) — Unit the phase duration is counted in. Only a fixed-price phase may set it, because its amount is declared rather than derived from the plan. Defaults to the plan's own billing interval.
- `amounts` (`list[OfferPhasesItemVariant3AmountsItem]`, required)

### OfferPhasesItemVariant3AmountsItem

- `currency` (`str`, required)
- `amount` (`int`, required) — Amount in the currency's minor unit (for example, cents for USD).

### OfferPhasesItemVariant4

- `type` (`Literal["fixed_price"]`, required)
- `duration_cycles` (`int | null`, required)
- `duration_interval` (`Literal["weekly", "monthly", "quarterly", "yearly"] | null`, required) — Unit the phase duration is counted in. Only a fixed-price phase may set it, because its amount is declared rather than derived from the plan. Defaults to the plan's own billing interval.
- `prices` (`list[OfferPhasesItemVariant4PricesItem]`, required)

### OfferPhasesItemVariant4PricesItem

- `currency` (`str`, required)
- `amount` (`int`, required) — Amount in the currency's minor unit (for example, cents for USD).

### OffersListResult

- `object` (`Literal["list"]`, required)
- `data` (`list[Offer]`, required)
- `has_more` (`bool`, required)
- `next_cursor` (`str`, optional)

### Payment

- `id` (`str`, required)
- `customer_id` (`str | null`, required)
- `kind` (`Literal["link", "charge"]`, required)
- `status` (`Literal["pending", "processing", "succeeded", "requires_action", "failed", "canceled"]`, required)
- `provider` (`Literal["stripe", "commet", "dlocal"]`, required)
- `amount_subtotal` (`int`, required)
- `tax_amount` (`int`, required)
- `amount_total` (`int`, required)
- `currency` (`str`, required)
- `description` (`str`, required)
- `metadata` (`dict[str, Any] | null`, required)
- `url` (`str | null`, required)
- `expires_at` (`str | null`, required)
- `created_at` (`str`, required)
- `updated_at` (`str`, required)
- `object` (`Literal["payment"]`, required)
- `livemode` (`bool`, required)

### PaymentMethodUpdateCheckout

- `checkout_url` (`str`, required)
- `object` (`Literal["checkout_session"]`, required)
- `livemode` (`bool`, required)

### PaymentsListResult

- `object` (`Literal["list"]`, required)
- `data` (`list[Payment]`, required)
- `has_more` (`bool`, required)
- `next_cursor` (`str`, optional)

### Payout

- `id` (`str`, required)
- `status` (`Literal["pending", "in_transit", "paid", "failed", "canceled"]`, required)
- `amount` (`int`, required)
- `fee` (`int`, required)
- `net_amount` (`int`, required)
- `currency` (`str`, required)
- `description` (`str | null`, required)
- `provider_transfer_id` (`str`, required)
- `created_at` (`str`, required)
- `object` (`Literal["payout"]`, required)
- `livemode` (`bool`, required)

### PayoutBankAccount

- `id` (`str`, required)
- `provider_external_account_id` (`str | null`, required)
- `holder_name` (`str`, required)
- `last4` (`str`, required)
- `bank_name` (`str | null`, required)
- `country` (`str`, required)
- `currency` (`str`, required)
- `account_type` (`Literal["checking", "savings"] | null`, required)
- `is_default` (`bool`, required)
- `status` (`Literal["active", "errored"]`, required)
- `created_at` (`str`, required)
- `object` (`Literal["payout_bank_account"]`, required)
- `livemode` (`bool`, required)

### Plan

- `id` (`str`, required)
- `name` (`str`, required)
- `code` (`str`, required)
- `description` (`str | null`, required)
- `consumption_model` (`ConsumptionModel | null`, required)
- `is_public` (`bool`, required)
- `is_default` (`bool`, required)
- `is_free` (`bool`, required)
- `block_on_exhaustion` (`bool | null`, required)
- `sort_order` (`int`, required)
- `plan_group_id` (`str | null`, required)
- `metadata` (`dict[str, Any] | null`, required)
- `created_at` (`str`, required)
- `updated_at` (`str`, required)
- `features` (`list[PlanFeaturesItem]`, required)
- `prices` (`list[PlanPricesItem]`, required)
- `exchange_rates` (`list[PlanExchangeRatesItem]`, required)
- `object` (`Literal["plan"]`, required)
- `livemode` (`bool`, required)

### PlanChange

Variants:

- `PlanChangeVariant1`
- `PlanChangeVariant2`
- `PlanChangeVariant3`

Discriminator: `outcome`

- `"requires_checkout"` → `PlanChangeVariant1`
- `"scheduled"` → `PlanChangeVariant2`
- `"completed"` → `PlanChangeVariant3`

### PlanChangeVariant1

- `outcome` (`Literal["requires_checkout"]`, required)
- `requires_checkout` (`Literal[True]`, required)
- `checkout_url` (`str`, required)
- `offer_application` (`PlanChangeVariant1OfferApplication`, optional)
- `object` (`Literal["plan_change"]`, required)
- `livemode` (`bool`, required)

### PlanChangeVariant1OfferApplication

- `id` (`str`, required)
- `offer_id` (`str`, required)
- `name` (`str`, required)
- `currency` (`str`, required)
- `subtotal` (`int`, required) — Subtotal in the currency's minor unit.
- `discount_amount` (`int`, required) — Discount in the currency's minor unit.
- `total` (`int`, required) — Total in the currency's minor unit.
- `phases` (`list[PlanChangeVariant1OfferApplicationPhasesItem]`, required)
- `applies_to` (`PlanChangeVariant1OfferApplicationAppliesTo`, required)

### PlanChangeVariant1OfferApplicationAppliesTo

Variants:

- `PlanChangeVariant1OfferApplicationAppliesToVariant1`
- `PlanChangeVariant1OfferApplicationAppliesToVariant2`
- `PlanChangeVariant1OfferApplicationAppliesToVariant3`

Discriminator: `type`

- `"plan_price"` → `PlanChangeVariant1OfferApplicationAppliesToVariant1`
- `"addon"` → `PlanChangeVariant1OfferApplicationAppliesToVariant2`
- `"credit_pack"` → `PlanChangeVariant1OfferApplicationAppliesToVariant3`

### PlanChangeVariant1OfferApplicationAppliesToVariant1

- `type` (`Literal["plan_price"]`, required)
- `id` (`str`, required)

### PlanChangeVariant1OfferApplicationAppliesToVariant2

- `type` (`Literal["addon"]`, required)
- `id` (`str`, required)

### PlanChangeVariant1OfferApplicationAppliesToVariant3

- `type` (`Literal["credit_pack"]`, required)
- `id` (`str`, required)

### PlanChangeVariant1OfferApplicationPhasesItem

Variants:

- `PlanChangeVariant1OfferApplicationPhasesItemVariant1`
- `PlanChangeVariant1OfferApplicationPhasesItemVariant2`
- `PlanChangeVariant1OfferApplicationPhasesItemVariant3`
- `PlanChangeVariant1OfferApplicationPhasesItemVariant4`

Discriminator: `type`

- `"free_trial"` → `PlanChangeVariant1OfferApplicationPhasesItemVariant1`
- `"percentage"` → `PlanChangeVariant1OfferApplicationPhasesItemVariant2`
- `"amount_off"` → `PlanChangeVariant1OfferApplicationPhasesItemVariant3`
- `"fixed_price"` → `PlanChangeVariant1OfferApplicationPhasesItemVariant4`

### PlanChangeVariant1OfferApplicationPhasesItemVariant1

- `type` (`Literal["free_trial"]`, required)
- `duration_days` (`int`, required)
- `starts_at` (`str | null`, required)
- `ends_at` (`str | null`, required)

### PlanChangeVariant1OfferApplicationPhasesItemVariant2

- `type` (`Literal["percentage"]`, required)
- `duration_cycles` (`int | null`, required)
- `duration_interval` (`Literal["weekly", "monthly", "quarterly", "yearly"] | null`, required)
- `starts_at` (`str | null`, required)
- `ends_at` (`str | null`, required)
- `percentage` (`int`, required) — Discount in basis points. 5000 means 50%.

### PlanChangeVariant1OfferApplicationPhasesItemVariant3

- `type` (`Literal["amount_off"]`, required)
- `duration_cycles` (`int | null`, required)
- `duration_interval` (`Literal["weekly", "monthly", "quarterly", "yearly"] | null`, required)
- `starts_at` (`str | null`, required)
- `ends_at` (`str | null`, required)
- `amount` (`int`, required) — Discount in the application currency's minor unit.

### PlanChangeVariant1OfferApplicationPhasesItemVariant4

- `type` (`Literal["fixed_price"]`, required)
- `duration_cycles` (`int | null`, required)
- `duration_interval` (`Literal["weekly", "monthly", "quarterly", "yearly"] | null`, required)
- `starts_at` (`str | null`, required)
- `ends_at` (`str | null`, required)
- `price` (`int`, required) — Fixed price in the application currency's minor unit.

### PlanChangeVariant2

- `outcome` (`Literal["scheduled"]`, required)
- `id` (`str`, required)
- `scheduled` (`Literal[True]`, required)
- `scheduled_for` (`str`, required)
- `change_type` (`Literal["subscription.plan_downgrade", "subscription.interval_change", "subscription.cancel"]`, required)
- `customer_id` (`str`, required)
- `new_plan_id` (`str`, optional)
- `new_plan_name` (`str`, optional)
- `new_billing_interval` (`str`, optional)
- `seat_limit_warning` (`PlanChangeVariant2SeatLimitWarning`, optional)
- `object` (`Literal["plan_change"]`, required)
- `livemode` (`bool`, required)

### PlanChangeVariant2SeatLimitWarning

- `feature_code` (`str`, required)
- `feature_name` (`str`, required)
- `current_seats` (`int`, required)
- `included` (`int`, required)
- `new_plan_name` (`str`, required)
- `effective_date` (`str`, required)

### PlanChangeVariant3

- `outcome` (`Literal["completed"]`, required)
- `id` (`str`, required)
- `scheduled` (`Literal[False]`, required)
- `customer_id` (`str`, required)
- `previous_plan` (`PlanChangeVariant3PreviousPlan`, required)
- `current_plan` (`PlanChangeVariant3CurrentPlan`, required)
- `billing_interval` (`str`, required)
- `billing` (`PlanChangeVariant3Billing`, required)
- `invoice_id` (`str`, optional)
- `offer_application` (`PlanChangeVariant3OfferApplication`, optional)
- `object` (`Literal["plan_change"]`, required)
- `livemode` (`bool`, required)

### PlanChangeVariant3Billing

- `credit` (`int`, required)
- `credits_applied` (`int`, required)
- `charge` (`int`, required)
- `tax_amount` (`int`, required)
- `net_amount` (`int`, required)
- `total_charged` (`int`, required)
- `remaining_credit_balance` (`int`, required)

### PlanChangeVariant3CurrentPlan

- `id` (`str`, required)
- `name` (`str`, required)
- `price` (`int`, required)

### PlanChangeVariant3OfferApplication

- `id` (`str`, required)
- `offer_id` (`str`, required)
- `name` (`str`, required)
- `currency` (`str`, required)
- `subtotal` (`int`, required) — Subtotal in the currency's minor unit.
- `discount_amount` (`int`, required) — Discount in the currency's minor unit.
- `total` (`int`, required) — Total in the currency's minor unit.
- `phases` (`list[PlanChangeVariant3OfferApplicationPhasesItem]`, required)
- `applies_to` (`PlanChangeVariant3OfferApplicationAppliesTo`, required)

### PlanChangeVariant3OfferApplicationAppliesTo

Variants:

- `PlanChangeVariant3OfferApplicationAppliesToVariant1`
- `PlanChangeVariant3OfferApplicationAppliesToVariant2`
- `PlanChangeVariant3OfferApplicationAppliesToVariant3`

Discriminator: `type`

- `"plan_price"` → `PlanChangeVariant3OfferApplicationAppliesToVariant1`
- `"addon"` → `PlanChangeVariant3OfferApplicationAppliesToVariant2`
- `"credit_pack"` → `PlanChangeVariant3OfferApplicationAppliesToVariant3`

### PlanChangeVariant3OfferApplicationAppliesToVariant1

- `type` (`Literal["plan_price"]`, required)
- `id` (`str`, required)

### PlanChangeVariant3OfferApplicationAppliesToVariant2

- `type` (`Literal["addon"]`, required)
- `id` (`str`, required)

### PlanChangeVariant3OfferApplicationAppliesToVariant3

- `type` (`Literal["credit_pack"]`, required)
- `id` (`str`, required)

### PlanChangeVariant3OfferApplicationPhasesItem

Variants:

- `PlanChangeVariant3OfferApplicationPhasesItemVariant1`
- `PlanChangeVariant3OfferApplicationPhasesItemVariant2`
- `PlanChangeVariant3OfferApplicationPhasesItemVariant3`
- `PlanChangeVariant3OfferApplicationPhasesItemVariant4`

Discriminator: `type`

- `"free_trial"` → `PlanChangeVariant3OfferApplicationPhasesItemVariant1`
- `"percentage"` → `PlanChangeVariant3OfferApplicationPhasesItemVariant2`
- `"amount_off"` → `PlanChangeVariant3OfferApplicationPhasesItemVariant3`
- `"fixed_price"` → `PlanChangeVariant3OfferApplicationPhasesItemVariant4`

### PlanChangeVariant3OfferApplicationPhasesItemVariant1

- `type` (`Literal["free_trial"]`, required)
- `duration_days` (`int`, required)
- `starts_at` (`str | null`, required)
- `ends_at` (`str | null`, required)

### PlanChangeVariant3OfferApplicationPhasesItemVariant2

- `type` (`Literal["percentage"]`, required)
- `duration_cycles` (`int | null`, required)
- `duration_interval` (`Literal["weekly", "monthly", "quarterly", "yearly"] | null`, required)
- `starts_at` (`str | null`, required)
- `ends_at` (`str | null`, required)
- `percentage` (`int`, required) — Discount in basis points. 5000 means 50%.

### PlanChangeVariant3OfferApplicationPhasesItemVariant3

- `type` (`Literal["amount_off"]`, required)
- `duration_cycles` (`int | null`, required)
- `duration_interval` (`Literal["weekly", "monthly", "quarterly", "yearly"] | null`, required)
- `starts_at` (`str | null`, required)
- `ends_at` (`str | null`, required)
- `amount` (`int`, required) — Discount in the application currency's minor unit.

### PlanChangeVariant3OfferApplicationPhasesItemVariant4

- `type` (`Literal["fixed_price"]`, required)
- `duration_cycles` (`int | null`, required)
- `duration_interval` (`Literal["weekly", "monthly", "quarterly", "yearly"] | null`, required)
- `starts_at` (`str | null`, required)
- `ends_at` (`str | null`, required)
- `price` (`int`, required) — Fixed price in the application currency's minor unit.

### PlanChangeVariant3PreviousPlan

- `id` (`str`, required)
- `name` (`str`, required)

### PlanExchangeRatesItem

- `currency` (`str`, required)
- `exchange_rate` (`float`, required)

### PlanFeature

- `plan_id` (`str`, required)
- `feature_id` (`str`, required)
- `enabled` (`bool`, required)
- `included_amount` (`int`, required)
- `unlimited` (`bool`, required)
- `overage` (`PlanFeatureOverage`, required)
- `credits_per_unit` (`int | null`, required)
- `pricing_mode` (`Literal["fixed", "ai_model"]`, required)
- `margin` (`int | null`, required)
- `object` (`Literal["plan_feature"]`, required)
- `livemode` (`bool`, required)

### PlanFeatureOverage

- `enabled` (`bool`, required)
- `unit_price` (`int`, required)

### PlanFeaturesItem

- `code` (`str`, required)
- `name` (`str`, required)
- `type` (`FeatureType`, required)
- `unit_name` (`str | null`, required)
- `enabled` (`bool`, required)
- `included_amount` (`int | null`, required)
- `unlimited` (`bool`, required)
- `overage` (`PlanFeaturesItemOverage | null`, required)
- `regional_prices` (`list[PlanFeaturesItemRegionalPricesItem]`, required)

### PlanFeaturesItemOverage

- `enabled` (`bool`, required)
- `model` (`Literal["per_unit"] | null`, required)
- `unit_price` (`int | null`, required)

### PlanFeaturesItemRegionalPricesItem

- `currency` (`str`, required)
- `overage_unit_price` (`int | null`, required)
- `auto_synced` (`bool`, required)

### PlanGrant

- `id` (`str`, required)
- `customer_id` (`str`, required)
- `subscription_id` (`str`, required)
- `base_plan_id` (`str`, required)
- `plan_id` (`str`, required)
- `plan_release_id` (`str`, required)
- `status` (`Literal["active", "expired", "revoked"]`, required)
- `duration` (`Literal["cycles", "until_date", "until_revoked"]`, required)
- `duration_cycles` (`int | null`, required)
- `starts_at` (`str`, required)
- `expires_at` (`str | null`, required)
- `reason` (`str`, required)
- `source` (`Literal["dashboard", "api"]`, required)
- `revoked_at` (`str | null`, required)
- `created_at` (`str`, required)
- `updated_at` (`str`, required)
- `events` (`list[PlanGrantEventsItem]`, required)
- `object` (`Literal["plan_grant"]`, required)
- `livemode` (`bool`, required)

### PlanGrantEventsItem

- `id` (`str`, required)
- `type` (`Literal["created", "updated", "expired", "revoked"]`, required)
- `reason` (`str`, required)
- `source` (`Literal["dashboard", "api", "system"]`, required)
- `previous_expires_at` (`str | null`, required)
- `expires_at` (`str | null`, required)
- `duration` (`Literal["cycles", "until_date", "until_revoked"] | null`, required)
- `duration_cycles` (`int | null`, required)
- `requested_expires_at` (`str | null`, required)
- `created_at` (`str`, required)

### PlanGroup

- `id` (`str`, required)
- `name` (`str`, required)
- `description` (`str | null`, required)
- `is_public` (`bool`, required)
- `created_at` (`str`, required)
- `updated_at` (`str`, required)
- `object` (`Literal["plan_group"]`, required)
- `livemode` (`bool`, required)

### PlanGroupDetail

- `id` (`str`, required)
- `name` (`str`, required)
- `description` (`str | null`, required)
- `is_public` (`bool`, required)
- `created_at` (`str`, required)
- `updated_at` (`str`, required)
- `plans` (`list[PlanGroupDetailPlansItem]`, required)
- `object` (`Literal["plan_group"]`, required)
- `livemode` (`bool`, required)

### PlanGroupDetailPlansItem

- `id` (`str`, required)
- `name` (`str`, required)
- `sort_order` (`int`, required)

### PlanGroupsListResult

- `object` (`Literal["list"]`, required)
- `data` (`list[PlanGroup]`, required)
- `has_more` (`bool`, required)
- `next_cursor` (`str`, optional)

### PlanPrice

- `id` (`str`, required) — Public plan price ID.
- `plan_id` (`str`, required)
- `billing_interval` (`BillingInterval`, required)
- `price` (`int`, required) — Price in the currency's minor unit (for example, cents for USD).
- `is_default` (`bool`, required)
- `trial_days` (`int`, required)
- `included_balance` (`int | null`, required)
- `included_credits` (`int | null`, required)
- `offer_id` (`str | null`, required) — Automatic introductory offer for this price.
- `inherits_from_price_id` (`str | null`, required) — Public base price ID for a market price variant, or null for a base price.
- `metadata` (`dict[str, Any]`, required) — Application metadata. Variant display names may use metadata.name.
- `market_prices` (`list[PlanPriceMarketPricesItem]`, required) — Country-market overrides. Variants inherit their base price for every market not listed.
- `created_at` (`str`, required)
- `updated_at` (`str`, required)
- `object` (`Literal["plan_price"]`, required)
- `livemode` (`bool`, required)

### PlanPriceMarketPricesItem

- `market_group_id` (`str`, required) — Public pricing market group ID.
- `currency` (`str`, required) — Presentment currency for this market.
- `price` (`int`, required) — Market price in the currency's minor unit.

### PlanPricesItem

- `id` (`str`, required) — Public plan price ID.
- `billing_interval` (`BillingInterval`, required)
- `price` (`int`, required) — Price in the currency's minor unit (for example, cents for USD).
- `is_default` (`bool`, required)
- `trial_days` (`int`, required)
- `included_balance` (`int | null`, required)
- `included_credits` (`int | null`, required)
- `offer_id` (`str | null`, required) — Automatic introductory offer for this price. Pass a Promotional Offer ID when creating a subscription to override it.
- `inherits_from_price_id` (`str | null`, required) — Public base price ID for a market price variant, or null for a base price.
- `metadata` (`dict[str, Any]`, required) — Application metadata. Variant display names may use metadata.name.
- `market_prices` (`list[PlanPricesItemMarketPricesItem]`, required) — Country-market overrides. An empty array means currency pricing and then the global USD price remain the fallback.
- `regional_prices` (`list[PlanPricesItemRegionalPricesItem]`, required)

### PlanPricesItemMarketPricesItem

- `market_group_id` (`str`, required) — Public pricing market group ID.
- `currency` (`str`, required) — Presentment currency for this market.
- `price` (`int`, required) — Market price in the currency's minor unit.

### PlanPricesItemRegionalPricesItem

- `currency` (`str`, required)
- `price` (`int`, required)
- `included_balance` (`int | null`, required)
- `auto_synced` (`bool`, required)

### PlanRegionalPricing

- `price_id` (`str`, required)
- `overrides` (`list[PlanRegionalPricingOverridesItem]`, required)
- `object` (`Literal["plan_regional_pricing"]`, required)
- `livemode` (`bool`, required)

### PlanRegionalPricingOverridesItem

- `currency` (`str`, required)
- `price` (`int`, required)
- `included_balance` (`int`, optional)

### PlanRegionalPricingResult

- `plan_id` (`str`, required)
- `currency` (`str`, required)
- `exchange_rate` (`float`, required)
- `prices_configured` (`int`, required)
- `features_configured` (`int`, required)
- `object` (`Literal["plan_regional_pricing"]`, required)
- `livemode` (`bool`, required)

### PlansListResult

- `object` (`Literal["list"]`, required)
- `data` (`list[Plan]`, required)
- `has_more` (`bool`, required)
- `next_cursor` (`str`, optional)

### PortalAccess

- `portal_url` (`str`, required)
- `object` (`Literal["portal_session"]`, required)
- `livemode` (`bool`, required)

### PreviewChange

- `currency` (`str`, required)
- `current_plan_credit` (`int`, required)
- `new_plan_charge` (`int`, required)
- `estimated_total` (`int`, required)
- `effective_date` (`str`, required)
- `days_remaining` (`int`, required)
- `total_days` (`int`, required)
- `is_upgrade` (`bool`, required)
- `offer_application` (`PreviewChangeOfferApplication`, optional)
- `object` (`Literal["plan_change_preview"]`, required)
- `livemode` (`bool`, required)

### PreviewChangeOfferApplication

- `id` (`str`, required)
- `offer_id` (`str`, required)
- `name` (`str`, required)
- `currency` (`str`, required)
- `subtotal` (`int`, required) — Subtotal in the currency's minor unit.
- `discount_amount` (`int`, required) — Discount in the currency's minor unit.
- `total` (`int`, required) — Total in the currency's minor unit.
- `phases` (`list[PreviewChangeOfferApplicationPhasesItem]`, required)
- `applies_to` (`PreviewChangeOfferApplicationAppliesTo`, required)

### PreviewChangeOfferApplicationAppliesTo

Variants:

- `PreviewChangeOfferApplicationAppliesToVariant1`
- `PreviewChangeOfferApplicationAppliesToVariant2`
- `PreviewChangeOfferApplicationAppliesToVariant3`

Discriminator: `type`

- `"plan_price"` → `PreviewChangeOfferApplicationAppliesToVariant1`
- `"addon"` → `PreviewChangeOfferApplicationAppliesToVariant2`
- `"credit_pack"` → `PreviewChangeOfferApplicationAppliesToVariant3`

### PreviewChangeOfferApplicationAppliesToVariant1

- `type` (`Literal["plan_price"]`, required)
- `id` (`str`, required)

### PreviewChangeOfferApplicationAppliesToVariant2

- `type` (`Literal["addon"]`, required)
- `id` (`str`, required)

### PreviewChangeOfferApplicationAppliesToVariant3

- `type` (`Literal["credit_pack"]`, required)
- `id` (`str`, required)

### PreviewChangeOfferApplicationPhasesItem

Variants:

- `PreviewChangeOfferApplicationPhasesItemVariant1`
- `PreviewChangeOfferApplicationPhasesItemVariant2`
- `PreviewChangeOfferApplicationPhasesItemVariant3`
- `PreviewChangeOfferApplicationPhasesItemVariant4`

Discriminator: `type`

- `"free_trial"` → `PreviewChangeOfferApplicationPhasesItemVariant1`
- `"percentage"` → `PreviewChangeOfferApplicationPhasesItemVariant2`
- `"amount_off"` → `PreviewChangeOfferApplicationPhasesItemVariant3`
- `"fixed_price"` → `PreviewChangeOfferApplicationPhasesItemVariant4`

### PreviewChangeOfferApplicationPhasesItemVariant1

- `type` (`Literal["free_trial"]`, required)
- `duration_days` (`int`, required)
- `starts_at` (`str | null`, required)
- `ends_at` (`str | null`, required)

### PreviewChangeOfferApplicationPhasesItemVariant2

- `type` (`Literal["percentage"]`, required)
- `duration_cycles` (`int | null`, required)
- `duration_interval` (`Literal["weekly", "monthly", "quarterly", "yearly"] | null`, required)
- `starts_at` (`str | null`, required)
- `ends_at` (`str | null`, required)
- `percentage` (`int`, required) — Discount in basis points. 5000 means 50%.

### PreviewChangeOfferApplicationPhasesItemVariant3

- `type` (`Literal["amount_off"]`, required)
- `duration_cycles` (`int | null`, required)
- `duration_interval` (`Literal["weekly", "monthly", "quarterly", "yearly"] | null`, required)
- `starts_at` (`str | null`, required)
- `ends_at` (`str | null`, required)
- `amount` (`int`, required) — Discount in the application currency's minor unit.

### PreviewChangeOfferApplicationPhasesItemVariant4

- `type` (`Literal["fixed_price"]`, required)
- `duration_cycles` (`int | null`, required)
- `duration_interval` (`Literal["weekly", "monthly", "quarterly", "yearly"] | null`, required)
- `starts_at` (`str | null`, required)
- `ends_at` (`str | null`, required)
- `price` (`int`, required) — Fixed price in the application currency's minor unit.

### PromoCode

- `id` (`str`, required)
- `code` (`str`, required)
- `offer_id` (`str`, required)
- `billing_interval` (`BillingInterval | null`, required)
- `max_redemptions` (`int | null`, required)
- `expires_at` (`str | null`, required)
- `is_active` (`bool`, required)
- `redemption_count` (`int`, required)
- `created_at` (`str`, required)
- `updated_at` (`str`, required)
- `object` (`Literal["promo_code"]`, required)
- `livemode` (`bool`, required)

### PromoCodesListResult

- `object` (`Literal["list"]`, required)
- `data` (`list[PromoCode]`, required)
- `has_more` (`bool`, required)
- `next_cursor` (`str`, optional)

### QuotaGetAllResult

- `object` (`Literal["list"]`, required)
- `data` (`list[UsageQuota]`, required)
- `has_more` (`bool`, required)
- `next_cursor` (`str`, optional)

### ReactivatedSubscription

- `subscription_id` (`str`, required)
- `invoice_id` (`str`, required)
- `status` (`Literal["processing", "succeeded"]`, required)
- `offer_application` (`ReactivatedSubscriptionOfferApplication`, optional)
- `object` (`Literal["subscription_reactivation"]`, required)
- `livemode` (`bool`, required)

### ReactivatedSubscriptionOfferApplication

- `id` (`str`, required)
- `offer_id` (`str`, required)
- `name` (`str`, required)
- `currency` (`str`, required)
- `subtotal` (`int`, required) — Subtotal in the currency's minor unit.
- `discount_amount` (`int`, required) — Discount in the currency's minor unit.
- `total` (`int`, required) — Total in the currency's minor unit.
- `phases` (`list[ReactivatedSubscriptionOfferApplicationPhasesItem]`, required)
- `applies_to` (`ReactivatedSubscriptionOfferApplicationAppliesTo`, required)

### ReactivatedSubscriptionOfferApplicationAppliesTo

Variants:

- `ReactivatedSubscriptionOfferApplicationAppliesToVariant1`
- `ReactivatedSubscriptionOfferApplicationAppliesToVariant2`
- `ReactivatedSubscriptionOfferApplicationAppliesToVariant3`

Discriminator: `type`

- `"plan_price"` → `ReactivatedSubscriptionOfferApplicationAppliesToVariant1`
- `"addon"` → `ReactivatedSubscriptionOfferApplicationAppliesToVariant2`
- `"credit_pack"` → `ReactivatedSubscriptionOfferApplicationAppliesToVariant3`

### ReactivatedSubscriptionOfferApplicationAppliesToVariant1

- `type` (`Literal["plan_price"]`, required)
- `id` (`str`, required)

### ReactivatedSubscriptionOfferApplicationAppliesToVariant2

- `type` (`Literal["addon"]`, required)
- `id` (`str`, required)

### ReactivatedSubscriptionOfferApplicationAppliesToVariant3

- `type` (`Literal["credit_pack"]`, required)
- `id` (`str`, required)

### ReactivatedSubscriptionOfferApplicationPhasesItem

Variants:

- `ReactivatedSubscriptionOfferApplicationPhasesItemVariant1`
- `ReactivatedSubscriptionOfferApplicationPhasesItemVariant2`
- `ReactivatedSubscriptionOfferApplicationPhasesItemVariant3`
- `ReactivatedSubscriptionOfferApplicationPhasesItemVariant4`

Discriminator: `type`

- `"free_trial"` → `ReactivatedSubscriptionOfferApplicationPhasesItemVariant1`
- `"percentage"` → `ReactivatedSubscriptionOfferApplicationPhasesItemVariant2`
- `"amount_off"` → `ReactivatedSubscriptionOfferApplicationPhasesItemVariant3`
- `"fixed_price"` → `ReactivatedSubscriptionOfferApplicationPhasesItemVariant4`

### ReactivatedSubscriptionOfferApplicationPhasesItemVariant1

- `type` (`Literal["free_trial"]`, required)
- `duration_days` (`int`, required)
- `starts_at` (`str | null`, required)
- `ends_at` (`str | null`, required)

### ReactivatedSubscriptionOfferApplicationPhasesItemVariant2

- `type` (`Literal["percentage"]`, required)
- `duration_cycles` (`int | null`, required)
- `duration_interval` (`Literal["weekly", "monthly", "quarterly", "yearly"] | null`, required)
- `starts_at` (`str | null`, required)
- `ends_at` (`str | null`, required)
- `percentage` (`int`, required) — Discount in basis points. 5000 means 50%.

### ReactivatedSubscriptionOfferApplicationPhasesItemVariant3

- `type` (`Literal["amount_off"]`, required)
- `duration_cycles` (`int | null`, required)
- `duration_interval` (`Literal["weekly", "monthly", "quarterly", "yearly"] | null`, required)
- `starts_at` (`str | null`, required)
- `ends_at` (`str | null`, required)
- `amount` (`int`, required) — Discount in the application currency's minor unit.

### ReactivatedSubscriptionOfferApplicationPhasesItemVariant4

- `type` (`Literal["fixed_price"]`, required)
- `duration_cycles` (`int | null`, required)
- `duration_interval` (`Literal["weekly", "monthly", "quarterly", "yearly"] | null`, required)
- `starts_at` (`str | null`, required)
- `ends_at` (`str | null`, required)
- `price` (`int`, required) — Fixed price in the application currency's minor unit.

### RecoveryLink

- `url` (`str`, required)
- `token` (`str`, required)
- `object` (`Literal["recovery_link"]`, required)
- `livemode` (`bool`, required)

### Refund

- `id` (`str`, required)
- `transaction_id` (`str`, required)
- `amount` (`int`, required)
- `currency` (`str`, required)
- `charge_id` (`str | null`, required)
- `status` (`Literal["pending", "requires_action", "succeeded", "failed", "canceled"]`, required)
- `reason` (`Literal["duplicate", "fraudulent", "requested_by_customer"] | null`, required)
- `object` (`Literal["refund"]`, required)
- `livemode` (`bool`, required)

### RemovedPlanFeature

- `id` (`str`, required)
- `removed` (`Literal[True]`, required)
- `object` (`Literal["plan_feature"]`, required)
- `livemode` (`bool`, required)

### RemovedPlanFromGroup

- `id` (`str`, required)
- `removed` (`bool`, required)
- `object` (`Literal["plan_group_membership"]`, required)
- `livemode` (`bool`, required)

### ReorderedPlans

- `reordered` (`bool`, required)
- `object` (`Literal["plan_group_order"]`, required)
- `livemode` (`bool`, required)

### SeatBalance

- `current` (`int`, required)
- `as_of` (`str`, required)
- `object` (`Literal["seat_balance"]`, required)
- `livemode` (`bool`, required)

### SeatBalanceCollection

- `balances` (`dict[str, SeatBalanceCollectionBalancesValue]`, required)
- `object` (`Literal["seat_balance_collection"]`, required)
- `livemode` (`bool`, required)

### SeatBalanceCollectionBalancesValue

- `current` (`int`, required)
- `as_of` (`str`, required)

### SeatEvent

- `id` (`str`, required)
- `customer_id` (`str`, required)
- `feature_code` (`str`, required)
- `previous_balance` (`int`, required)
- `new_balance` (`int`, required)
- `ts` (`str`, required)
- `created_at` (`str`, required)
- `object` (`Literal["seat_event"]`, required)
- `livemode` (`bool`, required)

### SeatsSetAllResult

- `object` (`Literal["list"]`, required)
- `data` (`list[SeatEvent]`, required)
- `has_more` (`bool`, required)
- `next_cursor` (`str`, optional)

### SentInvoice

- `sent` (`bool`, required)
- `sent_at` (`str`, required)
- `object` (`Literal["invoice_delivery"]`, required)
- `livemode` (`bool`, required)

### SetPlanRegionalPricingParamsFeaturesItem

- `feature_id` (`str`, required)
- `overage_unit_price` (`int`, required)

### SetPlanRegionalPricingParamsPricesItem

- `price_id` (`str`, required)
- `price` (`int`, required)
- `included_balance` (`int`, optional)

### Subscription

- `id` (`str`, required)
- `customer_id` (`str`, required)
- `plan` (`SubscriptionPlan`, required)
- `name` (`str`, required)
- `description` (`str | null`, required)
- `status` (`SubscriptionStatus`, required)
- `billing_interval` (`BillingInterval | null`, required)
- `trial_ends_at` (`str | null`, required)
- `current_period` (`SubscriptionCurrentPeriod | null`, required)
- `cancellation` (`SubscriptionCancellation | null`, required)
- `cancel_at_period_end` (`bool`, required)
- `scheduled_plan_change` (`SubscriptionScheduledPlanChange | null`, required)
- `start_date` (`str`, required)
- `end_date` (`str | null`, required)
- `billing_day_of_month` (`int | null`, required)
- `next_billing_date` (`str | null`, required)
- `checkout_url` (`str | null`, required)
- `created_at` (`str`, required)
- `updated_at` (`str`, required)
- `offer_applications` (`list[SubscriptionOfferApplication]`, required)
- `plan_grant` (`SubscriptionPlanGrant`, optional)
- `consumption_model` (`ConsumptionModel | null`, required)
- `features` (`list[SubscriptionFeaturesItem]`, required)
- `credits` (`SubscriptionCredits | null`, required)
- `balance` (`SubscriptionBalance | null`, required)
- `price_id` (`str | null`, required)
- `object` (`Literal["subscription"]`, required)
- `livemode` (`bool`, required)

### SubscriptionAddon

- `addon_id` (`str`, required)
- `status` (`Literal["active"]`, required)
- `prorated_charge` (`int`, required)
- `object` (`Literal["subscription_addon"]`, required)
- `livemode` (`bool`, required)

### SubscriptionBalance

- `remaining` (`float`, required)
- `included` (`float`, required)
- `currency` (`str`, required)

### SubscriptionCancellation

- `scheduled_at` (`str`, required)
- `reason` (`str | null`, required)
- `effective_at` (`str`, required)

### SubscriptionCredits

- `remaining` (`float`, required)
- `included` (`float`, required)
- `purchased` (`float`, required)

### SubscriptionCurrentPeriod

- `start` (`str`, required)
- `end` (`str`, required)
- `days_remaining` (`float`, required)

### SubscriptionFeaturesItem

Variants:

- `SubscriptionFeaturesItemVariant1`
- `SubscriptionFeaturesItemVariant2`
- `SubscriptionFeaturesItemVariant3`
- `SubscriptionFeaturesItemVariant4`

Discriminator: `type`

- `"boolean"` → `SubscriptionFeaturesItemVariant1`
- `"usage"` → `SubscriptionFeaturesItemVariant2`
- `"seats"` → `SubscriptionFeaturesItemVariant3`
- `"quota"` → `SubscriptionFeaturesItemVariant4`

### SubscriptionFeaturesItemVariant1

- `code` (`str`, required)
- `name` (`str`, required)
- `type` (`Literal["boolean"]`, required)
- `enabled` (`bool`, required)
- `base_access` (`SubscriptionFeaturesItemVariant1BaseAccess | null`, optional)

### SubscriptionFeaturesItemVariant1BaseAccess

- `enabled` (`bool`, required)

### SubscriptionFeaturesItemVariant2

- `code` (`str`, required)
- `name` (`str`, required)
- `type` (`Literal["usage"]`, required)
- `usage` (`SubscriptionFeaturesItemVariant2Usage`, optional)
- `base_access` (`SubscriptionFeaturesItemVariant2BaseAccess | null`, optional)

### SubscriptionFeaturesItemVariant2BaseAccess

- `included` (`float`, required)
- `unlimited` (`bool`, required)

### SubscriptionFeaturesItemVariant2Usage

- `current` (`float`, required)
- `included` (`float`, required)
- `overage_quantity` (`float`, required)
- `overage_unit_price` (`float`, optional)
- `unlimited` (`bool`, optional)

### SubscriptionFeaturesItemVariant3

- `code` (`str`, required)
- `name` (`str`, required)
- `type` (`Literal["seats"]`, required)
- `usage` (`SubscriptionFeaturesItemVariant3Usage`, required)
- `base_access` (`SubscriptionFeaturesItemVariant3BaseAccess | null`, optional)

### SubscriptionFeaturesItemVariant3BaseAccess

- `included` (`float`, required)
- `unlimited` (`bool`, required)

### SubscriptionFeaturesItemVariant3Usage

- `current` (`float`, required)
- `included` (`float`, required)
- `overage_quantity` (`float`, required)
- `overage_unit_price` (`float`, optional)
- `unlimited` (`bool`, optional)

### SubscriptionFeaturesItemVariant4

- `code` (`str`, required)
- `name` (`str`, required)
- `type` (`Literal["quota"]`, required)
- `usage` (`SubscriptionFeaturesItemVariant4Usage`, optional)
- `base_access` (`SubscriptionFeaturesItemVariant4BaseAccess | null`, optional)

### SubscriptionFeaturesItemVariant4BaseAccess

- `included` (`float`, required)
- `unlimited` (`bool`, required)

### SubscriptionFeaturesItemVariant4Usage

- `current` (`float`, required)
- `included` (`float`, required)
- `overage_quantity` (`float`, required)
- `overage_unit_price` (`float`, optional)
- `unlimited` (`bool`, optional)

### SubscriptionOfferApplication

- `id` (`str`, required)
- `name` (`str`, required)
- `applies_to` (`SubscriptionOfferApplicationAppliesTo`, required)
- `offer_id` (`str | null`, required)
- `source` (`Literal["direct", "introductory", "promo_code", "card_promotion", "custom"]`, required)
- `status` (`Literal["quoted", "applied", "failed", "expired"]`, required)
- `currency` (`str | null`, required)
- `subtotal` (`int | null`, required)
- `discount_amount` (`int | null`, required)
- `total` (`int | null`, required)
- `phases` (`list[SubscriptionOfferApplicationPhase]`, required)
- `quoted_at` (`str`, required)
- `expires_at` (`str | null`, required)
- `applied_at` (`str | null`, required)

### SubscriptionOfferApplicationAppliesTo

Variants:

- `SubscriptionOfferApplicationAppliesToVariant1`
- `SubscriptionOfferApplicationAppliesToVariant2`
- `SubscriptionOfferApplicationAppliesToVariant3`

Discriminator: `type`

- `"plan_price"` → `SubscriptionOfferApplicationAppliesToVariant1`
- `"addon"` → `SubscriptionOfferApplicationAppliesToVariant2`
- `"credit_pack"` → `SubscriptionOfferApplicationAppliesToVariant3`

### SubscriptionOfferApplicationAppliesToVariant1

- `type` (`Literal["plan_price"]`, required)
- `id` (`str`, required)

### SubscriptionOfferApplicationAppliesToVariant2

- `type` (`Literal["addon"]`, required)
- `id` (`str`, required)

### SubscriptionOfferApplicationAppliesToVariant3

- `type` (`Literal["credit_pack"]`, required)
- `id` (`str`, required)

### SubscriptionOfferApplicationPhase

Variants:

- `SubscriptionOfferApplicationPhaseVariant1`
- `SubscriptionOfferApplicationPhaseVariant2`
- `SubscriptionOfferApplicationPhaseVariant3`
- `SubscriptionOfferApplicationPhaseVariant4`

Discriminator: `type`

- `"free_trial"` → `SubscriptionOfferApplicationPhaseVariant1`
- `"percentage"` → `SubscriptionOfferApplicationPhaseVariant2`
- `"amount_off"` → `SubscriptionOfferApplicationPhaseVariant3`
- `"fixed_price"` → `SubscriptionOfferApplicationPhaseVariant4`

### SubscriptionOfferApplicationPhaseVariant1

- `type` (`Literal["free_trial"]`, required)
- `duration_days` (`int`, required)
- `duration_interval` (`Literal["weekly", "monthly", "quarterly", "yearly"] | null`, required)
- `starts_at` (`str | null`, required)
- `ends_at` (`str | null`, required)

### SubscriptionOfferApplicationPhaseVariant2

- `type` (`Literal["percentage"]`, required)
- `duration_cycles` (`int | null`, required)
- `duration_interval` (`Literal["weekly", "monthly", "quarterly", "yearly"] | null`, required)
- `percentage` (`int`, required)
- `starts_at` (`str | null`, required)
- `ends_at` (`str | null`, required)

### SubscriptionOfferApplicationPhaseVariant3

- `type` (`Literal["amount_off"]`, required)
- `duration_cycles` (`int | null`, required)
- `duration_interval` (`Literal["weekly", "monthly", "quarterly", "yearly"] | null`, required)
- `amount` (`int`, required)
- `starts_at` (`str | null`, required)
- `ends_at` (`str | null`, required)

### SubscriptionOfferApplicationPhaseVariant4

- `type` (`Literal["fixed_price"]`, required)
- `duration_cycles` (`int | null`, required)
- `duration_interval` (`Literal["weekly", "monthly", "quarterly", "yearly"] | null`, required)
- `price` (`int`, required)
- `starts_at` (`str | null`, required)
- `ends_at` (`str | null`, required)

### SubscriptionPlan

- `id` (`str`, required)
- `name` (`str`, required)
- `base_price` (`float`, required)

### SubscriptionPlanGrant

- `id` (`str`, required) — The active Plan Grant ID.
- `plan` (`SubscriptionPlanGrantPlan`, required) — The higher plan whose access is temporarily applied.
- `expires_at` (`str | null`, required) — When the temporary access ends, or null when it lasts until revoked.

### SubscriptionPlanGrantPlan

- `id` (`str`, required)
- `name` (`str`, required)

### SubscriptionScheduledPlanChange

- `change_type` (`Literal["plan_downgrade", "interval_change"]`, required)
- `new_plan_id` (`str | null`, required)
- `new_plan_name` (`str | null`, required)
- `new_billing_interval` (`str | null`, required)
- `scheduled_for` (`str`, required)

### SubscriptionsListResult

- `object` (`Literal["list"]`, required)
- `data` (`list[SubscriptionSummary]`, required)
- `has_more` (`bool`, required)
- `next_cursor` (`str`, optional)

### SubscriptionSummary

- `id` (`str`, required)
- `customer_id` (`str`, required)
- `plan` (`SubscriptionSummaryPlan`, required)
- `name` (`str`, required)
- `description` (`str | null`, required)
- `status` (`SubscriptionStatus`, required)
- `billing_interval` (`BillingInterval | null`, required)
- `trial_ends_at` (`str | null`, required)
- `current_period` (`SubscriptionSummaryCurrentPeriod | null`, required)
- `cancellation` (`SubscriptionSummaryCancellation | null`, required)
- `cancel_at_period_end` (`bool`, required)
- `scheduled_plan_change` (`SubscriptionSummaryScheduledPlanChange | null`, required)
- `start_date` (`str`, required)
- `end_date` (`str | null`, required)
- `billing_day_of_month` (`int | null`, required)
- `next_billing_date` (`str | null`, required)
- `checkout_url` (`str | null`, required)
- `created_at` (`str`, required)
- `updated_at` (`str`, required)
- `offer_applications` (`list[SubscriptionOfferApplication]`, required)
- `price_id` (`str | null`, required)
- `object` (`Literal["subscription"]`, required)
- `livemode` (`bool`, required)

### SubscriptionSummaryCancellation

- `scheduled_at` (`str`, required)
- `reason` (`str | null`, required)
- `effective_at` (`str`, required)

### SubscriptionSummaryCurrentPeriod

- `start` (`str`, required)
- `end` (`str`, required)
- `days_remaining` (`float`, required)

### SubscriptionSummaryPlan

- `id` (`str`, required)
- `name` (`str`, required)

### SubscriptionSummaryScheduledPlanChange

- `change_type` (`Literal["plan_downgrade", "interval_change"]`, required)
- `new_plan_id` (`str | null`, required)
- `new_plan_name` (`str | null`, required)
- `new_billing_interval` (`str | null`, required)
- `scheduled_for` (`str`, required)

### TestClock

- `simulated_time` (`str | null`, required)
- `is_active` (`bool`, required)
- `now` (`str`, required)
- `latest_run` (`TestClockLatestRun | null`, required)
- `object` (`Literal["test_clock"]`, required)
- `livemode` (`bool`, required)

### TestClockLatestRun

- `id` (`str`, required)
- `status` (`Literal["pending", "running", "completed", "failed"]`, required)
- `started_at_time` (`str`, required)
- `target_time` (`str`, required)
- `estimated_deadline_count` (`int`, required)
- `completed_deadline_count` (`int`, required)
- `failed_deadline_count` (`int`, required)
- `error` (`str | null`, required)
- `items` (`list[TestClockLatestRunItemsItem]`, required)

### TestClockLatestRunItemsItem

- `kind` (`Literal["billing_cycle", "dunning_retry"]`, required)
- `status` (`Literal["pending", "processing", "completed", "failed"]`, required)
- `due_at` (`str`, required)
- `subscription_id` (`str`, required)
- `customer_name` (`str | null`, required)
- `invoice_number` (`str | null`, required)
- `invoice_id` (`str | null`, required)
- `outcome` (`str | null`, required)
- `detail` (`str | null`, required)
- `error` (`str | null`, required)

### TestClockRun

- `id` (`str`, required)
- `status` (`Literal["pending", "running", "completed", "failed"]`, required)
- `started_at_time` (`str`, required)
- `target_time` (`str`, required)
- `estimated_deadline_count` (`int`, required)
- `completed_deadline_count` (`int`, required)
- `failed_deadline_count` (`int`, required)
- `error` (`str | null`, required)
- `items` (`list[TestClockRunItemsItem]`, required)
- `object` (`Literal["test_clock_run"]`, required)
- `livemode` (`bool`, required)

### TestClockRunItemsItem

- `kind` (`Literal["billing_cycle", "dunning_retry"]`, required)
- `status` (`Literal["pending", "processing", "completed", "failed"]`, required)
- `due_at` (`str`, required)
- `subscription_id` (`str`, required)
- `customer_name` (`str | null`, required)
- `invoice_number` (`str | null`, required)
- `invoice_id` (`str | null`, required)
- `outcome` (`str | null`, required)
- `detail` (`str | null`, required)
- `error` (`str | null`, required)

### TrackUsageParamsPropertiesItem

- `property` (`str`, required)
- `value` (`str`, required)

### Transaction

- `id` (`str`, required)
- `invoice_id` (`str | null`, required)
- `gross_amount` (`int | null`, required) — Gross amount in USD cents. Null when the provider has not reported an honest USD figure; see presentmentAmount.
- `subtotal` (`int | null`, required) — Subtotal in USD cents (gross minus tax). Null when grossAmount is null.
- `tax_amount` (`int | null`, required)
- `presentment_amount` (`int | null`, required) — Amount in the charge currency's smallest unit, as presented to the customer. Set for non-USD charges; null when the charge was made in USD.
- `currency` (`str`, required)
- `provider` (`PaymentProvider`, required) — The payment provider the charge was routed to: stripe, commet, or dlocal.
- `status` (`TransactionStatus`, required)
- `customer_email` (`str | null`, required)
- `customer_name` (`str | null`, required)
- `paid_at` (`str | null`, required)
- `created_at` (`str`, required)
- `updated_at` (`str`, required)
- `available_at` (`str | null`, required)
- `object` (`Literal["transaction"]`, required)
- `livemode` (`bool`, required)

### TransactionListItem

- `id` (`str`, required)
- `invoice_id` (`str | null`, required)
- `gross_amount` (`int | null`, required) — Gross amount in USD cents. Null when the provider has not reported an honest USD figure; see presentmentAmount.
- `subtotal` (`int | null`, required) — Subtotal in USD cents (gross minus tax). Null when grossAmount is null.
- `tax_amount` (`int | null`, required)
- `presentment_amount` (`int | null`, required) — Amount in the charge currency's smallest unit, as presented to the customer. Set for non-USD charges; null when the charge was made in USD.
- `currency` (`str`, required)
- `provider` (`PaymentProvider`, required) — The payment provider the charge was routed to: stripe, commet, or dlocal.
- `status` (`TransactionStatus`, required)
- `customer_email` (`str | null`, required)
- `customer_name` (`str | null`, required)
- `paid_at` (`str | null`, required)
- `created_at` (`str`, required)
- `updated_at` (`str`, required)
- `object` (`Literal["transaction"]`, required)
- `livemode` (`bool`, required)

### TransactionRetry

- `original_transaction_id` (`str`, required)
- `invoice_id` (`str`, required)
- `status` (`Literal["processing", "succeeded"]`, required)
- `object` (`Literal["transaction_retry"]`, required)
- `livemode` (`bool`, required)

### TransactionsListResult

- `object` (`Literal["list"]`, required)
- `data` (`list[TransactionListItem]`, required)
- `has_more` (`bool`, required)
- `next_cursor` (`str`, optional)

### UpdateCustomerParamsAddress

- `line1` (`str`, required)
- `line2` (`str`, optional)
- `city` (`str`, required)
- `state` (`str`, optional)
- `postal_code` (`str`, required)
- `country` (`str`, required)
- `region` (`str`, optional)

### UpdateOfferParamsPhasesItem

Variants:

- `UpdateOfferParamsPhasesItemVariant1`
- `UpdateOfferParamsPhasesItemVariant2`
- `UpdateOfferParamsPhasesItemVariant3`
- `UpdateOfferParamsPhasesItemVariant4`

Discriminator: `type`

- `"free_trial"` → `UpdateOfferParamsPhasesItemVariant1`
- `"percentage"` → `UpdateOfferParamsPhasesItemVariant2`
- `"amount_off"` → `UpdateOfferParamsPhasesItemVariant3`
- `"fixed_price"` → `UpdateOfferParamsPhasesItemVariant4`

### UpdateOfferParamsPhasesItemVariant1

- `type` (`Literal["free_trial"]`, required)
- `duration_days` (`int`, required)

### UpdateOfferParamsPhasesItemVariant2

- `type` (`Literal["percentage"]`, required)
- `duration_cycles` (`int | null`, required)
- `duration_interval` (`Literal["weekly", "monthly", "quarterly", "yearly"] | null`, optional) — Unit the phase duration is counted in. Only a fixed-price phase may set it, because its amount is declared rather than derived from the plan. Defaults to the plan's own billing interval.
- `percentage` (`int`, required) — Discount in basis points. 5000 means 50%.

### UpdateOfferParamsPhasesItemVariant3

- `type` (`Literal["amount_off"]`, required)
- `duration_cycles` (`int | null`, required)
- `duration_interval` (`Literal["weekly", "monthly", "quarterly", "yearly"] | null`, optional) — Unit the phase duration is counted in. Only a fixed-price phase may set it, because its amount is declared rather than derived from the plan. Defaults to the plan's own billing interval.
- `amounts` (`list[UpdateOfferParamsPhasesItemVariant3AmountsItem]`, required)

### UpdateOfferParamsPhasesItemVariant3AmountsItem

- `currency` (`str`, required)
- `amount` (`int`, required) — Amount in the currency's minor unit (for example, cents for USD).

### UpdateOfferParamsPhasesItemVariant4

- `type` (`Literal["fixed_price"]`, required)
- `duration_cycles` (`int | null`, required)
- `duration_interval` (`Literal["weekly", "monthly", "quarterly", "yearly"] | null`, optional) — Unit the phase duration is counted in. Only a fixed-price phase may set it, because its amount is declared rather than derived from the plan. Defaults to the plan's own billing interval.
- `prices` (`list[UpdateOfferParamsPhasesItemVariant4PricesItem]`, required)

### UpdateOfferParamsPhasesItemVariant4PricesItem

- `currency` (`str`, required)
- `amount` (`int`, required) — Amount in the currency's minor unit (for example, cents for USD).

### UpdatePlanFeatureParamsOverage

- `enabled` (`bool`, optional)
- `unit_price` (`int`, optional)

### UpdatePlanPriceParamsMarketPricesItem

- `market_group_id` (`str`, required)
- `currency` (`Literal["usd", "ars", "brl", "clp", "cop", "pen", "uyu", "pyg", "bob", "mxn", "cad", "eur", "gbp", "jpy", "cny", "krw", "hkd", "sgd", "twd", "inr", "thb"]`, required)
- `price` (`int`, required)

### UpsertRegionalPricesParamsOverridesItem

- `currency` (`str`, required)
- `price` (`int`, required)
- `included_balance` (`int`, optional)

### UsageAdjustment

- `id` (`str`, required)
- `value` (`int`, required)
- `previous_value` (`int`, required)
- `adjustment` (`int`, required)
- `customer_id` (`str`, required)
- `reason` (`str | null`, required)
- `ts` (`str`, required)
- `created_at` (`str`, required)
- `feature_code` (`str`, required)
- `object` (`Literal["usage_adjustment"]`, required)
- `livemode` (`bool`, required)

### UsageCheck

Variants:

- `UsageCheckVariant1`
- `UsageCheckVariant2`
- `UsageCheckVariant3`

Discriminator: `consumption_model`

- `"metered"` → `UsageCheckVariant1`
- `"credits"` → `UsageCheckVariant2`
- `"balance"` → `UsageCheckVariant3`

### UsageCheckVariant1

- `allowed` (`bool`, required)
- `subscription_status` (`str`, required)
- `feature_code` (`str`, required)
- `quantity` (`int`, required)
- `reason` (`str`, optional)
- `message` (`str`, optional)
- `consumption_model` (`Literal["metered"]`, required)
- `current` (`float`, required)
- `remaining` (`float`, required)
- `unlimited` (`bool`, required)
- `included` (`float`, required)
- `overage_enabled` (`bool`, required)
- `overage_unit_price` (`float | null`, required)
- `object` (`Literal["usage_check"]`, required)
- `livemode` (`bool`, required)

### UsageCheckVariant2

- `allowed` (`bool`, required)
- `subscription_status` (`str`, required)
- `feature_code` (`str`, required)
- `quantity` (`int`, required)
- `reason` (`str`, optional)
- `message` (`str`, optional)
- `consumption_model` (`Literal["credits"]`, required)
- `credits_per_unit` (`int`, required)
- `estimated_credits` (`int`, required)
- `plan_credits` (`int`, required)
- `purchased_credits` (`int`, required)
- `total_credits` (`int`, required)
- `object` (`Literal["usage_check"]`, required)
- `livemode` (`bool`, required)

### UsageCheckVariant3

- `allowed` (`bool`, required)
- `subscription_status` (`str`, required)
- `feature_code` (`str`, required)
- `quantity` (`int`, required)
- `reason` (`str`, optional)
- `message` (`str`, optional)
- `consumption_model` (`Literal["balance"]`, required)
- `unit_price` (`float`, required)
- `estimated_amount` (`float`, required)
- `current_balance` (`float`, required)
- `block_on_exhaustion` (`bool`, required)
- `currency` (`str`, required)
- `object` (`Literal["usage_check"]`, required)
- `livemode` (`bool`, required)

### UsageEvent

- `id` (`str`, required)
- `feature_code` (`str`, required)
- `value` (`float`, required)
- `customer_id` (`str`, required)
- `event_id` (`str | null`, required)
- `ts` (`str`, required)
- `created_at` (`str`, required)
- `properties` (`list[UsageEventPropertiesItem]`, required)
- `consumption` (`UsageEventConsumption`, optional)
- `object` (`Literal["usage_event"]`, required)
- `livemode` (`bool`, required)

### UsageEventConsumption

- `model` (`Literal["credits", "balance"]`, required)
- `deducted` (`float`, required)
- `remaining` (`float`, required)
- `blocked` (`bool`, required)

### UsageEventPropertiesItem

- `property` (`str`, required)
- `value` (`str`, required)

### UsageQuota

- `feature_code` (`str`, required)
- `current` (`float`, required)
- `included` (`float`, required)
- `remaining` (`float | null`, required)
- `billed_quantity` (`float`, required)
- `unlimited` (`bool`, required)
- `overage_enabled` (`bool`, required)
- `as_of` (`str | null`, required)
- `object` (`Literal["usage_quota"]`, required)
- `livemode` (`bool`, required)

### UsageQuotaEvent

- `id` (`str`, required)
- `customer_id` (`str`, required)
- `feature_code` (`str`, required)
- `previous_balance` (`int`, required)
- `new_balance` (`int`, required)
- `ts` (`str`, required)
- `created_at` (`str`, required)
- `object` (`Literal["usage_quota_event"]`, required)
- `livemode` (`bool`, required)

### Webhook

- `id` (`str`, required)
- `url` (`str`, required)
- `events` (`list[str]`, required)
- `description` (`str | null`, required)
- `is_active` (`bool`, required)
- `api_version` (`str | null`, required)
- `created_at` (`str`, required)
- `object` (`Literal["webhook"]`, required)
- `livemode` (`bool`, required)

### WebhookAddonRef

- `id` (`str`, required)
- `name` (`str`, required)

### WebhookBalance

- `current_balance` (`float`, required)

### WebhookBankRef

- `bank_name` (`str | null`, required)
- `last4` (`str`, required)

### WebhookCardInfo

- `brand` (`str`, required)
- `last4` (`str`, required)
- `exp_month` (`float`, required)
- `exp_year` (`float`, required)

### WebhookCreditsBalance

- `plan_credits` (`float`, required)
- `purchased_credits` (`float`, required)
- `total_credits` (`float`, required)

### WebhookPlanGrantTimelineEvent

- `id` (`str`, required) — The public ID of this plan grant event.
- `type` (`Literal["created", "updated", "expired", "revoked"]`, required) — The durable lifecycle transition recorded by this event.
- `reason` (`str`, required) — The reason recorded for this transition.
- `source` (`Literal["dashboard", "api", "system"]`, required) — Where this transition originated.
- `previous_expires_at` (`str | null`, required) — The prior expiration deadline for an update, otherwise null.
- `expires_at` (`str | null`, required) — The expiration deadline after this transition, if any.
- `duration` (`Literal["cycles", "until_date", "until_revoked"] | null`, required) — The duration selected by a create or update event.
- `duration_cycles` (`int | null`, required) — The selected cycle count when duration is cycles.
- `requested_expires_at` (`str | null`, required) — The requested deadline when duration is until_date.
- `created_at` (`str`, required) — When this transition occurred.

### WebhookPlanRef

- `id` (`str`, required)
- `name` (`str`, required)

### WebhookSeatSummary

- `code` (`str`, required)
- `current` (`float | null`, required)
- `included` (`float | null`, required)
- `remaining` (`float | null`, required)
- `unlimited` (`bool | null`, required)

### WebhooksListResult

- `object` (`Literal["list"]`, required)
- `data` (`list[Webhook]`, required)
- `has_more` (`bool`, required)
- `next_cursor` (`str`, optional)

### WebhookTest

- `success` (`bool`, required)
- `delivery_id` (`str`, required)
- `delivered_at` (`str`, required)
- `object` (`Literal["webhook_delivery"]`, required)
- `livemode` (`bool`, required)
