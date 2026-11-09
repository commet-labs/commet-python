# Subscriptions

API version: `2026-08-27`

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

Activate an add-on on a subscription. Charges a prorated amount for the current billing period. An add-on that the subscription's plan version does not sell is rejected with addon_unavailable.

### Parameters

- `id` (`str`, required)
- `addon_id` (`str`, required)

### Request options

- `idempotency_key` (`str`, optional) — Unique key used to safely retry this write for 24 hours without applying it twice.

### Returns

`SubscriptionAddon`

## get_auto_top_up

`commet.subscriptions.get_auto_top_up(...)`

`GET /subscriptions/{id}/auto-top-up` · operation `get-subscription-auto-top-up`

Read whether the subscription tops up automatically with its saved payment method when its available credits or balance reach a threshold, with the top-ups used this period and the last failure.

### Parameters

- `id` (`str`, required)

### Returns

`SubscriptionAutoTopUp`

## update_auto_top_up

`commet.subscriptions.update_auto_top_up(...)`

`PATCH /subscriptions/{id}/auto-top-up` · operation `update-subscription-auto-top-up`

Turn automatic top-ups on or off and set the threshold, the size of each top-up and the maximum top-ups per period. Send only the fields that change. On a credits plan each top-up buys `quantity` credits; on a balance plan it adds `amount` in minor units of the subscription currency, plus tax, and `threshold` is in the same minor units. Enabling requires a plan that sells credits or has balance top-ups on. The size must be at least the plan's minimum when auto top-up is enabled or when the size changes, so turning it off keeps working after the minimum rises. Saving it enabled resumes a paused auto top-up.

### Parameters

- `id` (`str`, required)
- `enabled` (`bool`, optional)
- `threshold` (`int`, optional)
- `quantity` (`int`, optional) — Credits each top-up buys. Credits plans only.
- `amount` (`int`, optional) — Minor units of the subscription currency each top-up adds. Balance plans only.
- `max_per_period` (`int`, optional)

### Request options

- `idempotency_key` (`str`, optional) — Unique key used to safely retry this write for 24 hours without applying it twice.

### Returns

`SubscriptionAutoTopUp`

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

Top up a balance subscription. Charges the customer's payment method for the amount plus tax, adds it to the subscription's purchased balance (after paying back any overage owed on the plan balance), creates its invoice and emits `balance.topped_up`. Purchased balance is spent after the plan balance and is kept until the subscription ends. Rejected with 400 when the subscription is not on a balance plan, its plan has top-ups turned off, or the amount is below the effective minimum: the plan's minimum top-up in the subscription currency, raised to the currency's minimum charge.

### Parameters

- `id` (`str`, required)
- `amount` (`int`, required) — The amount to add, in minor units of the subscription currency (cents; whole units for zero-decimal currencies).

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

Upgrade or change billing interval immediately, optionally applying an Offer by offerId or the Offer of a promoCode. Scheduled changes accept neither offerId nor promoCode. From a free plan, a promoCode opens the checkout with the code applied and counts its use when the checkout is paid; without offerId or promoCode, a destination price whose free trial requires no payment method starts that trial right away without checkout. During a trial without a payment method, an immediate change returns 409 no_payment_method; scheduled changes still apply.

### Parameters

- `id` (`str`, required)
- `new_plan_id` (`str`, optional)
- `new_billing_interval` (`Literal["weekly", "monthly", "quarterly", "semiannual", "yearly"]`, optional)
- `success_url` (`str`, optional)
- `offer_id` (`str`, optional)
- `promo_code` (`str`, optional)

### Valid parameter combinations

- `promo_code`

### Request options

- `idempotency_key` (`str`, optional) — Unique key used to safely retry this write for 24 hours without applying it twice.

### Returns

`PlanChange`

## change_version

`commet.subscriptions.change_version(...)`

`POST /subscriptions/{id}/change-version` · operation `change-subscription-version`

Move a subscription to a newer published version of its plan, now or at the end of the period, without proration; an older version is rejected with version_not_newer, and a subscription on a running experiment moves only to a later version of that experiment. The subscription keeps its currency and its price: a destination that does not sell its currency is rejected with missing_regional_price, and one that does not sell the price it pays with price_not_found. A free version moves only to a free version and a paid one only to a paid one (validation_error). A subscription whose usage does not fit the destination, or with an active add-on the destination does not sell, is not moved either, and the error says why. Each change is recorded as a move of this one subscription in the plan's moves. Repeating the same request changes nothing; a new one replaces the pending move.

### Parameters

- `id` (`str`, required)
- `plan_version_id` (`str`, required) — A published version of the subscription's plan.
- `effective` (`Literal["now", "period_end"]`, required) — now changes features, limits and the included credits or balance at once (the included difference is added to or subtracted from the plan credits or plan balance: an increase first pays any plan-part debt, a decrease never creates new debt, and purchased credits and purchased balance are untouched) and charges the new price from the next renewal. period_end changes everything at the next renewal. There is never a proration charge or refund.

### Request options

- `idempotency_key` (`str`, optional) — Unique key used to safely retry this write for 24 hours without applying it twice.

### Returns

`Subscription`

## purchase_credits

`commet.subscriptions.purchase_credits(...)`

`POST /subscriptions/{id}/credits` · operation `purchase-credits`

Purchase a fixed credit pack or choose a whole credit quantity at the subscription plan price and minimum. Charges the saved payment method and adds purchased credits. A credit pack that the subscription's plan version does not sell is rejected with credit_pack_unavailable.

### Parameters

- `id` (`str`, required)
- `credit_pack_id` (`str`, optional)
- `quantity` (`int`, optional)

### Valid parameter combinations

- `credit_pack_id`
- `quantity`

### Request options

- `idempotency_key` (`str`, optional) — Unique key used to safely retry this write for 24 hours without applying it twice.

### Returns

`CreditGrant`

## apply_offer

`commet.subscriptions.apply_offer(...)`

`PUT /subscriptions/{id}/offer` · operation `apply-subscription-offer`

Apply a direct Offer to a subscription. On a pending checkout it quotes or replaces the checkout discount, which starts after the plan price trial when there is one, and the existing checkout URL remains unchanged. On an active subscription it applies the Offer immediately with its discount phases starting at the next billing cycle; the call is rejected while another applied Offer still has active or upcoming discount phases.

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

## pause

`commet.subscriptions.pause(...)`

`POST /subscriptions/{id}/pause` · operation `pause-subscription`

Pause immediately or schedule a pause for the end of the current billing or trial period. Set durationDays to null for an indefinite pause.

### Parameters

- `id` (`str`, required)
- `mode` (`Literal["immediate", "period_end"]`, required)
- `duration_days` (`int | null`, required)

### Request options

- `idempotency_key` (`str`, optional) — Unique key used to safely retry this write for 24 hours without applying it twice.

### Returns

`Subscription`

## update_pause

`commet.subscriptions.update_pause(...)`

`PATCH /subscriptions/{id}/pause` · operation `update-subscription-pause`

Change the duration of a scheduled or active pause. Set durationDays to null to make it indefinite.

### Parameters

- `id` (`str`, required)
- `duration_days` (`int | null`, required)

### Request options

- `idempotency_key` (`str`, optional) — Unique key used to safely retry this write for 24 hours without applying it twice.

### Returns

`Subscription`

## revoke_pause

`commet.subscriptions.revoke_pause(...)`

`DELETE /subscriptions/{id}/pause` · operation `revoke-subscription-pause`

Revoke a pause before it becomes effective. Active pauses must be resumed instead.

### Parameters

- `id` (`str`, required)

### Returns

`Subscription`

## update_payment_method

`commet.subscriptions.update_payment_method(...)`

`POST /subscriptions/{id}/payment-method/update` · operation `update-payment-method`

Creates a hosted checkout to update the payment method of an active, trialing or past_due subscription. Pending-payment subscriptions must use their payment checkout.

### Parameters

- `id` (`str`, required)
- `success_url` (`str`, optional)

### Request options

- `idempotency_key` (`str`, optional) — Unique key used to safely retry this write for 24 hours without applying it twice.

### Returns

`PaymentMethodUpdateCheckout`

## create_prepaid_periods_checkout

`commet.subscriptions.create_prepaid_periods_checkout(...)`

`POST /subscriptions/{id}/prepaid-periods` · operation `create-prepaid-periods-checkout`

Creates a hosted checkout to pay billing periods of a recurring subscription in advance with any payment method. On an active subscription the paid periods start after the last paid period and replace any open prepaid-periods checkout. On a pending-payment subscription the first payment covers the requested periods and replaces its pending checkout. The billing interval does not change.

### Parameters

- `id` (`str`, required)
- `periods` (`int`, required) — Active subscriptions: billing periods to add after the last paid period. Pending-payment subscriptions: total billing periods the first payment covers, including the current one.
- `offer_id` (`str`, optional) — Offer applied from the first added period for its full configured duration. Active subscriptions only; assign an Offer to a pending-payment subscription with PUT /subscriptions/{id}/offer.
- `success_url` (`str`, optional)

### Request options

- `idempotency_key` (`str`, optional) — Unique key used to safely retry this write for 24 hours without applying it twice.

### Returns

`PrepaidPeriodsCheckout`

## preview_change

`commet.subscriptions.preview_change(...)`

`POST /subscriptions/{id}/preview-change` · operation `preview-change-plan`

Preview proration details for an immediate plan change without applying it. Free-to-paid changes are never scheduled and the change-plan endpoint returns hosted checkout for them, except a change without offerId or promoCode to a price whose free trial needs no payment method, for a customer who never had that plan: it starts the trial at once, so the preview reports nothing due today. For paid plans, interval direction takes precedence: a longer interval is immediate and a shorter interval is scheduled. When the interval is unchanged, a higher-sort-order plan is immediate and a lower-sort-order plan is scheduled. A paid-to-free change is always scheduled. Returns credit, charge, and net amount. The target plan must belong to the same plan group as the current plan, otherwise a 400 with code `plans_not_in_same_group` is returned. A change between two free plans has nothing to prorate and returns a zero-amount estimate. Scheduled changes return a 400 with code `plan_change_scheduled`; apply those via the change-plan endpoint. Pass offerId to quote the destination plan with an Offer, or promoCode to quote it with the Offer of a promo code validated with the checkout's rules.

### Parameters

- `id` (`str`, required)
- `plan_id` (`str`, required)
- `billing_interval` (`Literal["weekly", "monthly", "quarterly", "semiannual", "yearly", "one_time"]`, optional)
- `offer_id` (`str`, optional)
- `promo_code` (`str`, optional)

### Valid parameter combinations

- `plan_id`
- `plan_id` + `promo_code`

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

## resume

`commet.subscriptions.resume(...)`

`POST /subscriptions/{id}/resume` · operation `resume-subscription`

Resume a paused subscription. Immediate pauses continue the preserved period without a charge. Period-end pauses charge a new period before access is restored.

### Parameters

- `id` (`str`, required)

### Request options

- `idempotency_key` (`str`, optional) — Unique key used to safely retry this write for 24 hours without applying it twice.

### Returns

`SubscriptionResume`

## get

`commet.subscriptions.get(...)`

`GET /subscriptions/{id}` · operation `get-subscription`

Get a subscription by its public ID, regardless of status (including pending_payment and past_due).

### Parameters

- `id` (`str`, required)

### Returns

`Subscription`

## revoke_scheduled_plan_change

`commet.subscriptions.revoke_scheduled_plan_change(...)`

`DELETE /subscriptions/{id}/scheduled-plan-change` · operation `revoke-scheduled-plan-change`

Revoke the plan or interval change scheduled for the end of the period, so the subscription stays on its current plan. Returns the updated subscription.

### Parameters

- `id` (`str`, required)

### Returns

`Subscription`

## revoke_scheduled_version_change

`commet.subscriptions.revoke_scheduled_version_change(...)`

`DELETE /subscriptions/{id}/scheduled-version-change` · operation `revoke-scheduled-version-change`

Cancel the move to another plan version pending for the next renewal, so the subscription stays on its version, and send subscription.version_change_canceled with reason canceled_by_merchant. A move made now has nothing pending to revoke. With nothing pending it changes nothing. Returns the subscription.

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
- `plan_version_id` (`str`, optional)

### Returns

`SubscriptionsListResult`

## create

`commet.subscriptions.create(...)`

`POST /subscriptions` · operation `create-subscription`

Create a subscription for a customer. Commet selects the default price when priceId is omitted. The subscription starts at the base USD price; market and currency are resolved from the buyer's request country when the checkout opens. Without an offer override, Commet applies the price's automatic introductory Offer. Pass offerId to apply an active compatible Offer directly, or cardPromotionId to preselect a card-eligible Promotional Offer for the initial checkout when card promotions are enabled for the organization. For the initial checkout, provider accepts either a processor name or an exact payment connection ID. When the price's free trial requires no payment method, the subscription starts trialing right away with no checkout (checkoutUrl null, hasPaymentMethod false); it cannot be combined with offerId, promoCode, cardPromotionId or provider, and an organization that cannot charge yet receives 403.

### Parameters

- `customer_id` (`str`, required)
- `billing_interval` (`Literal["weekly", "monthly", "quarterly", "semiannual", "yearly", "one_time"] | null`, optional)
- `price_id` (`str`, optional) — Public price ID. When omitted, Commet selects the default price for the billing interval and still applies its market pricing.
- `initial_seats` (`dict[str, int]`, optional)
- `provider` (`Literal["stripe"] | Literal["commet"] | Literal["dlocal"] | str`, optional) — Payment provider name or exact public payment connection ID for the initial checkout. Overrides country routing when present.
- `payment_method_types` (`list[Literal["card", "oxxo", "mercado_pago", "google_pay", "smartpix"]]`, optional) — Payment methods the initial checkout may offer. Restricts what the checkout already offers for the buyer's country, currency and payment connection; it never enables a method the connection does not have and never changes routing. When none of them is available to the buyer, the checkout shows that it cannot accept payments.
- `name` (`str`, optional)
- `start_date` (`str`, optional)
- `success_url` (`str`, optional)
- `prepaid_periods` (`int`, optional) — Billing periods of the subscription's interval paid with the first payment, including the current one. Defaults to 1. The interval does not change: each paid period renews at zero and the subscription renews normally after the last one unless `cancelAtPeriodEnd` is true.
- `cancel_at_period_end` (`bool`, optional) — Schedules the cancellation from creation so the subscription ends after its last paid period and never renews with any payment method.
- `plan_version_id` (`str`, optional) — Public ID of a published version of the plan, current or not, including an experiment's versions. The subscription is created on that version and stays on it: checkout charges its price and activation grants its credits, add-ons and credit packs. When omitted, the subscription gets the current version, or the version an experiment code (planCode `<plan code>:<experiment code>`) sells.
- `offer_id` (`str`, optional)
- `promo_code` (`str`, optional)
- `custom_trial_days` (`int`, optional) — Trial length in days, replacing the price's trial. A customer who already had this plan, in a trial or paying, gets no trial and goes through the regular checkout.
- `skip_trial` (`bool`, optional)
- `plan_id` (`str`, optional)
- `plan_code` (`str`, optional) — The plan code, or an experiment code as `<plan code>:<experiment code>` to sell the version the experiment sells.
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
