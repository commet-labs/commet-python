# Changelog

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
