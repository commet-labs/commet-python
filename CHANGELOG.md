# Changelog

## 9.10.0

- Plans have versions. Editing a plan publishes a new version, and existing subscriptions stay on theirs until moved. `plans.list_versions`, `plans.get_version`, `plans.compare_versions` and `plans.create_version` read and publish versions; `plans.create_draft`, `plans.update_draft`, `plans.publish_draft` and the other draft methods prepare one; `plans.create_experiment`, `plans.make_experiment_current`, `plans.archive_experiment` and the other experiment methods sell a version through its own code; `plans.create_move`, `plans.cancel_move` and the other move methods move subscribers to a newer version; `plans.list_subscribers_needing_a_change` and `plans.keep_subscriber_on_version` handle the subscribers that do not fit it.
- `subscriptions.change_version` moves one subscription to a newer version of its plan, now or at the end of the period, and `subscriptions.revoke_scheduled_version_change` cancels a pending move. Subscriptions return `plan_version` and `scheduled_version_change`.
- `subscriptions.create` accepts `plan_version_id`, and `plan_code` as `<plan code>:<experiment code>` to sell an experiment. `subscriptions.list` filters by `plan_version_id`.
- Plans return `countries`. `addons.create`, `addons.update`, `credit_packs.create` and `credit_packs.update` accept `plan_ids`, and add-ons and credit packs return them. `subscriptions.preview_change` returns `deactivated_addons`.
- New webhook events `subscription.version_changed` and `subscription.version_change_canceled`.
- New errors `plan_version_not_found`, `plan_experiment_not_found`, `subscribers_do_not_fit`, `version_not_newer`, `addon_unavailable` and `credit_pack_unavailable`.

## 9.9.0

- Subscriptions on a balance plan split their balance in two parts: the plan balance (spent first, replaced or rolled over at each reset) and the purchased balance (top-ups and manual adjustments, kept until the subscription ends), plus the total. Credits subscriptions add their plan credits and total. The existing remaining amount keeps its meaning.
- `plans.create` and `plans.update` accept `unused_plan_balance` (expire or roll over up to a maximum plan balance) and `plan_balance_limit` (the most plan balance spent per day or week), and `plans.update` accepts `block_on_exhaustion` to turn overage on or off. Plans return both settings.
- `subscriptions.update_auto_top_up` accepts `amount` for balance plans and `subscriptions.get_auto_top_up` returns it, so balance subscriptions top up automatically; `amount_below_minimum` is a new failure reason.
- Usage checks, usage events and the `customer.state_changed` balance add the plan balance limit window and the plan, purchased and total balance parts.
- New webhook events `balance.granted`, `balance.expired` and `payment_method.detached`.
- `customers.create` and `customers.update` accept `business_tax_id`, and customers return it.
- `subscriptions.create` accepts `payment_method_types` to limit the payment methods its initial checkout offers.

## 9.8.0

- `subscriptions.purchase_credits` buys a chosen `quantity` of credits at the plan's price, besides a `credit_pack_id`.
- `subscriptions.get_auto_top_up` and `subscriptions.update_auto_top_up` read and configure automatic credit purchases.
- `subscriptions.change_plan` and `subscriptions.preview_change` accept `promo_code`, as an alternative to `offer_id`.
- `subscriptions.revoke_scheduled_plan_change` keeps a subscription on its current plan by revoking the change scheduled for the end of the period.
- `customers.create` and `customers.create_batch` accept `plan_group_id`, so a customer starts on that plan group's starting plan.
- `plans.create` and `plans.update` accept `unused_plan_credits`, `plan_credit_limit` and `is_default`, and plan prices accept `trial_requires_payment_method`.
- `promo_codes.create` and `promo_codes.update` accept `first_purchase_only`.
- Creating a subscription accepts a custom trial length or skipping the trial together with an Offer.
- Responses add whether a subscription has a payment method, which integration manages an Offer or promo code, whether a promo code is limited to a first purchase, the unused plan credit and plan credit limit settings of plans, and the plan credit limit window of usage checks and events.
- Creating or updating an Offer no longer accepts a `free_trial` phase, which the API already rejects; trials belong to plan prices. The generated offer phase variants are renumbered: `CreateOfferParamsPhasesItemVariant1`, `Variant2` and `Variant3` are now the percentage, amount-off and fixed-price phases, and the same applies to `UpdateOfferParamsPhasesItem` and `OfferPhasesItem`.

## 9.7.0

- Add paying billing periods in advance: create a prepaid-periods checkout for a subscription, and set `prepaidPeriods` and `cancelAtPeriodEnd` when creating one.
- Support the `prepayment` invoice type and payment reason, the `prepaid_period` invoice line type, and the `google_pay` and `smartpix` payment methods.

## 9.6.0

- Add the `semiannual` billing interval.

## 9.5.0

- Install the webhooks contract (`docs/webhooks.openapi.json`) with the SDK documentation in place of per-event pages, and refresh the documentation from commet.co/docs.

## 9.4.0

- Add subscription pause, pause updates, pause revocation, resume, and their lifecycle webhooks, including indefinite pauses.
- Support restricted API keys and permission-scoped key creation.
- Expose payment context, payment methods, and subscription payment methods from API `2026-08-27`.
- Refresh the installed API documentation to match the released contract.

## 9.3.0

- Align currency inputs and active-subscription Offer behavior with the current API contract.
- Install the complete version-matched Commet documentation with the SDK package.

## 9.2.0

- Add customer credits and Plan Grant management, including effective versus base feature access and Plan Grant lifecycle webhooks.
- Add pending-checkout Offer application, card-promotion selection, exact payment-connection routing, and provider details on payment recovery webhooks.
- Expose durable test-clock runs and latest-run state.
- Align deprecated payout verification and manual test-clock billing methods with their current no-payload contracts.
- Preserve exact server request IDs on API errors and never fabricate correlation IDs locally.

## 9.0.0

- Pin requests to API `2026-07-31`.
- Replace pricing Market Groups with the top-level Markets resource.
- Make Offers independent from purposes and plan-price associations.
- Expose target-aware Offer Applications on subscriptions.

## 8.0.1

- Document Offers, reusable pricing Market Groups, and selectable price variants.
- Clarify plan-change preview behavior for plan sort order and billing intervals.

## 8.0.0

- Add pricing markets and selectable price variants, including market groups and explicit price selection.
- Add Promotional Offers and the current usage check, track, and set operations.
- Add webhook endpoint management while preserving signature verification and event dispatch helpers.
- Return typed resources and list envelopes directly from API methods.
- Align subscription, feature access, invoice, payout, seat, and transaction types with API v8.
- Rename legacy request fields to their v8 replacements, including `feature_code` and `offer_id`.
