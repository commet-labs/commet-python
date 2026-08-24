# Subscriptions

API version: `2026-07-31`

## deactivate_addon

`commet.subscriptions.deactivate_addon(...)`

`DELETE /subscriptions/{id}/addons/{addonId}` · operation `deactivate-addon`

Deactivate an add-on from a subscription.

### Parameters

- `id` (`str`, required)
- `addon_id` (`str`, required)

### Returns

`DeletedSubscriptionAddon`

## activate_addon

`commet.subscriptions.activate_addon(...)`

`POST /subscriptions/{id}/addons` · operation `activate-addon`

Activate an add-on on a subscription. Charges a prorated amount for the current billing period.

### Parameters

- `id` (`str`, required)
- `addon_id` (`str`, required)

### Request options

- `idempotency_key` (`str`, optional) — Unique key used to safely retry this write for 24 hours without applying it twice.

### Returns

`SubscriptionAddon`

## adjust_balance

`commet.subscriptions.adjust_balance(...)`

`POST /subscriptions/{id}/balance/adjust` · operation `adjust-balance`

Adjust a subscription's balance or credits by a signed amount. Positive adds, negative subtracts.

### Parameters

- `id` (`str`, required)
- `amount` (`int`, required)
- `reason` (`str`, optional)
- `type` (`Literal["credits", "balance"]`, optional)

### Request options

- `idempotency_key` (`str`, optional) — Unique key used to safely retry this write for 24 hours without applying it twice.

### Returns

`BalanceAdjustment`

## topup_balance

`commet.subscriptions.topup_balance(...)`

`POST /subscriptions/{id}/balance/topup` · operation `topup-balance`

Top up a subscription's balance. Charges the customer's payment method for the specified amount.

### Parameters

- `id` (`str`, required)
- `amount` (`int`, required)

### Request options

- `idempotency_key` (`str`, optional) — Unique key used to safely retry this write for 24 hours without applying it twice.

### Returns

`BalanceTopup`

## cancel

`commet.subscriptions.cancel(...)`

`POST /subscriptions/{id}/cancel` · operation `cancel-subscription`

Cancel immediately or at period end and return the updated subscription.

### Parameters

- `id` (`str`, required)
- `reason` (`str`, optional)
- `immediate` (`bool`, optional)

### Request options

- `idempotency_key` (`str`, optional) — Unique key used to safely retry this write for 24 hours without applying it twice.

### Returns

`Subscription`

## change_plan

`commet.subscriptions.change_plan(...)`

`POST /subscriptions/{id}/change-plan` · operation `change-plan`

Upgrade or change billing interval immediately, optionally applying an Offer. Scheduled changes do not accept offers.

### Parameters

- `id` (`str`, required)
- `new_plan_id` (`str`, optional)
- `new_billing_interval` (`Literal["weekly", "monthly", "quarterly", "yearly"]`, optional)
- `success_url` (`str`, optional)
- `offer_id` (`str`, optional)

### Request options

- `idempotency_key` (`str`, optional) — Unique key used to safely retry this write for 24 hours without applying it twice.

### Returns

`PlanChange`

## purchase_credits

`commet.subscriptions.purchase_credits(...)`

`POST /subscriptions/{id}/credits` · operation `purchase-credits`

Purchase a credit pack for a subscription. Charges the customer and adds credits to their balance.

### Parameters

- `id` (`str`, required)
- `credit_pack_id` (`str`, required)

### Request options

- `idempotency_key` (`str`, optional) — Unique key used to safely retry this write for 24 hours without applying it twice.

### Returns

`CreditGrant`

## apply_offer

`commet.subscriptions.apply_offer(...)`

`PUT /subscriptions/{id}/offer` · operation `apply-subscription-offer`

Apply a direct Offer to a subscription. On a pending payment checkout it quotes or replaces the checkout discount and the existing checkout URL remains unchanged. On an active subscription it applies the Offer immediately with its discount phases starting at the next billing cycle; the call is rejected while another applied Offer still has active or upcoming discount phases. Offers with a free trial phase cannot be applied after checkout creation.

### Parameters

- `id` (`str`, required)
- `offer_id` (`str`, required)
- `expires_at` (`str`, optional)

### Request options

- `idempotency_key` (`str`, optional) — Unique key used to safely retry this write for 24 hours without applying it twice.

### Returns

`Subscription`

## remove_offer

`commet.subscriptions.remove_offer(...)`

`DELETE /subscriptions/{id}/offer` · operation `remove-subscription-offer`

Remove the quoted direct Offer from a subscription's pending payment checkout. The existing checkout URL remains unchanged and returns to its undiscounted price.

### Parameters

- `id` (`str`, required)

### Returns

`Subscription`

## update_payment_method

`commet.subscriptions.update_payment_method(...)`

`POST /subscriptions/{id}/payment-method/update` · operation `update-payment-method`

Creates a hosted checkout session for the customer to update the subscription's default payment method.

### Parameters

- `id` (`str`, required)
- `success_url` (`str`, optional)

### Request options

- `idempotency_key` (`str`, optional) — Unique key used to safely retry this write for 24 hours without applying it twice.

### Returns

`PaymentMethodUpdateCheckout`

## preview_change

`commet.subscriptions.preview_change(...)`

`POST /subscriptions/{id}/preview-change` · operation `preview-change-plan`

Preview proration details for an immediate plan change without applying it. Free-to-paid changes are never scheduled and the change-plan endpoint always returns hosted checkout for them. For paid plans, interval direction takes precedence: a longer interval is immediate and a shorter interval is scheduled. When the interval is unchanged, a higher-sort-order plan is immediate and a lower-sort-order plan is scheduled. A paid-to-free change is always scheduled. Returns credit, charge, and net amount. The target plan must belong to the same plan group as the current plan, otherwise a 400 with code `plans_not_in_same_group` is returned. A change between two free plans has nothing to prorate and returns a zero-amount estimate. Scheduled changes return a 400 with code `plan_change_scheduled`; apply those via the change-plan endpoint. Pass offerId to quote the destination plan with an Offer.

### Parameters

- `id` (`str`, required)
- `plan_id` (`str`, required)
- `billing_interval` (`Literal["weekly", "monthly", "quarterly", "yearly", "one_time"]`, optional)
- `offer_id` (`str`, optional)

### Request options

- `idempotency_key` (`str`, optional) — Unique key used to safely retry this write for 24 hours without applying it twice.

### Returns

`PreviewChange`

## reactivate

`commet.subscriptions.reactivate(...)`

`POST /subscriptions/{id}/reactivate` · operation `reactivate-subscription`

Reactivates a subscription. A past_due subscription retries its outstanding renewal charge (recovering to active on success). A canceled subscription generates a fresh invoice, charges the saved card, and resets the billing period. On a successful charge the subscription becomes active; a declined charge returns an error with a recoveryUrl in the error details that can be sent to the customer to update their card. A canceled subscription may apply an Offer by offerId; past-due recovery cannot.

### Parameters

- `id` (`str`, required)
- `offer_id` (`str`, optional)

### Request options

- `idempotency_key` (`str`, optional) — Unique key used to safely retry this write for 24 hours without applying it twice.

### Returns

`ReactivatedSubscription`

## create_recovery_link

`commet.subscriptions.create_recovery_link(...)`

`POST /subscriptions/{id}/recovery-links` · operation `create-subscription-recovery-link`

Generates a hosted, signed recovery link that lets the customer pay the outstanding renewal charge for a past_due subscription. Unlike reactivate, which charges server-to-server, this returns a link the merchant can deliver through their own email, SMS, or dashboard. The link carries a self-contained signed token and stays valid until the charge is paid or the subscription is no longer past due.

### Parameters

- `id` (`str`, required)

### Request options

- `idempotency_key` (`str`, optional) — Unique key used to safely retry this write for 24 hours without applying it twice.

### Returns

`RecoveryLink`

## get

`commet.subscriptions.get(...)`

`GET /subscriptions/{id}` · operation `get-subscription`

Get a subscription by its public ID, regardless of status (including pending_payment and past_due).

### Parameters

- `id` (`str`, required)

### Returns

`Subscription`

## uncancel

`commet.subscriptions.uncancel(...)`

`POST /subscriptions/{id}/uncancel` · operation `uncancel-subscription`

Revert a scheduled cancellation and return the updated subscription. Only works before cancellation takes effect.

### Parameters

- `id` (`str`, required)

### Request options

- `idempotency_key` (`str`, optional) — Unique key used to safely retry this write for 24 hours without applying it twice.

### Returns

`Subscription`

## get_active

`commet.subscriptions.get_active(...)`

`GET /subscriptions/active` · operation `get-active-subscription`

Get the active subscription for a customer. Returns null if none.

### Parameters

- `customer_id` (`str`, required)

### Returns

`Subscription | None`

## list

`commet.subscriptions.list(...)`

`GET /subscriptions` · operation `list-subscriptions`

List all subscriptions. Filter by customer ID or status.

### Parameters

- `customer_id` (`str`, optional)
- `status` (`SubscriptionStatus`, optional)

### Returns

`SubscriptionsListResult`

## create

`commet.subscriptions.create(...)`

`POST /subscriptions` · operation `create-subscription`

Create a subscription for a customer. Commet selects the default price when priceId is omitted and resolves its market from the customer's billing country. Without an offer override, Commet applies the price's automatic introductory Offer. Pass offerId to apply an active compatible Offer directly, or cardPromotionId to preselect a card-eligible Promotional Offer for the initial checkout when card promotions are enabled for the organization. For the initial checkout, provider accepts either a processor name or an exact payment connection ID.

### Parameters

- `customer_id` (`str`, required)
- `billing_interval` (`Literal["weekly", "monthly", "quarterly", "yearly", "one_time"] | null`, optional)
- `price_id` (`str`, optional) — Public price ID. When omitted, Commet selects the default price for the billing interval and still applies its market pricing.
- `initial_seats` (`dict[str, int]`, optional)
- `provider` (`Literal["stripe"] | Literal["commet"] | Literal["dlocal"] | str`, optional) — Payment provider name or exact public payment connection ID for the initial checkout. Overrides country routing when present.
- `name` (`str`, optional)
- `start_date` (`str`, optional)
- `success_url` (`str`, optional)
- `offer_id` (`str`, optional)
- `promo_code` (`str`, optional)
- `custom_trial_days` (`int`, optional)
- `skip_trial` (`bool`, optional)
- `plan_id` (`str`, optional)
- `plan_code` (`str`, optional)
- `card_promotion_id` (`str`, optional) — Public card promotion ID. The offer is shown immediately and remains conditional on card eligibility until checkout confirmation.

### Valid parameter combinations

- `customer_id` + `plan_id`
- `customer_id` + `plan_code`
- `customer_id` + `offer_id` + `plan_id`
- `customer_id` + `offer_id` + `plan_code`
- `customer_id` + `card_promotion_id` + `plan_id`
- `customer_id` + `card_promotion_id` + `plan_code`

### Request options

- `idempotency_key` (`str`, optional) — Unique key used to safely retry this write for 24 hours without applying it twice.

### Returns

`CreatedSubscription`
