# Plans

API version: `2026-08-27`

## publish_draft

`commet.plans.publish_draft(...)`

`POST /plans/{id}/drafts/{draftId}/publish` · operation `publish-plan-draft`

Publish a draft as the plan's current version, as a new experiment with its own code, or as the next version of the experiment it started from. A country missing a price, or removing the signup trial of the plan's group from the current version, stops the publication. With move, subscribers of earlier versions move at their renewal or now; if any of them does not fit the new version, nothing is published and the response lists each one with what would make it fit, to send back in changes. Paused subscribers stay where they are. Send preview to check without publishing.

### Parameters

- `id` (`str`, required)
- `draft_id` (`str`, required)
- `publish_as` (`Literal["current", "experiment", "experiment_version"]`, required) — current sells the draft to every new buyer.
- `move` (`Literal["keep", "period_end", "now"]`, optional) — What happens to subscribers of earlier versions: keep them, move them at their next renewal, or move them now (features and balance change today, the price at renewal). Nobody moves unless every one of them fits or has a change below.
- `changes` (`list[PublishPlanDraftParamsChangesItem]`, optional) — Per-subscriber changes that make each one fit, applied at its renewal.
- `preview` (`bool`, optional) — Check everything without publishing.
- `experiment_code` (`str`, optional) — The experiment's own code, after the plan's code.

### Valid parameter combinations

- `publish_as`
- `publish_as` + `experiment_code`
- `publish_as`

### Request options

- `idempotency_key` (`str`, optional) — Unique key used to safely retry this write for 24 hours without applying it twice.

### Returns

`PlanDraftPublication`

## get_draft

`commet.plans.get_draft(...)`

`GET /plans/{id}/drafts/{draftId}` · operation `get-plan-draft`

Retrieve a draft with the version it started from and what it changes.

### Parameters

- `id` (`str`, required)
- `draft_id` (`str`, required)

### Returns

`PlanDraft`

## update_draft

`commet.plans.update_draft(...)`

`PATCH /plans/{id}/drafts/{draftId}` · operation `update-plan-draft`

Change a draft's prices per interval, trials, the interval shown first, countries with their currency and prices, and credit or balance rules, or undo single changes. Each block sent replaces that block; blocks left out stay as they are. Buyers and subscribers see nothing until the draft is published.

### Parameters

- `id` (`str`, required)
- `draft_id` (`str`, required)
- `prices` (`list[UpdatePlanDraftParamsPricesItem]`, optional) — Every interval the draft sells. An interval the draft sold and this list leaves out is removed from the draft.
- `countries` (`list[UpdatePlanDraftParamsCountriesItem]`, optional) — Every country with its own currency or prices. A country the draft sold and this list leaves out is removed. A country missing a price blocks publishing.
- `rules` (`UpdatePlanDraftParamsRules`, optional) — Credit or balance rules; fields left out stay as they are.
- `undo` (`list[str]`, optional) — Change keys to put back as the version the draft started from had them.

### Request options

- `idempotency_key` (`str`, optional) — Unique key used to safely retry this write for 24 hours without applying it twice.

### Returns

`PlanDraft`

## delete_draft

`commet.plans.delete_draft(...)`

`DELETE /plans/{id}/drafts/{draftId}` · operation `delete-plan-draft`

Discard a draft. Nothing it changed was ever sold.

### Parameters

- `id` (`str`, required)
- `draft_id` (`str`, required)

### Returns

`DeletedObject`

## list_drafts

`commet.plans.list_drafts(...)`

`GET /plans/{id}/drafts` · operation `list-plan-drafts`

List the plan's open drafts, oldest first, each with the version it started from and what it changes. Drafts sell nothing until published.

### Parameters

- `id` (`str`, required)

### Returns

`PlansListDraftsResult`

## create_draft

`commet.plans.create_draft(...)`

`POST /plans/{id}/drafts` · operation `create-plan-draft`

Start a draft from a version of the plan: the current one, an experiment's version or an older one. A plan can have any number of drafts. Edit it, then publish it as the current version, as an experiment or as an experiment's next version; nothing changes for buyers or subscribers until then.

### Parameters

- `id` (`str`, required)
- `from_version_id` (`str`, optional) — The version to start from: the current version, an experiment's version or an older version. Defaults to the current version.

### Request options

- `idempotency_key` (`str`, optional) — Unique key used to safely retry this write for 24 hours without applying it twice.

### Returns

`PlanDraft`

## archive_experiment

`commet.plans.archive_experiment(...)`

`POST /plans/{id}/experiments/{code}/archive` · operation `archive-plan-experiment`

Stop selling the experiment. Its code sells the plan's current version from then on, so links already shared keep working. Choose what happens to its subscribers: keep them on its versions, or move them to the current version at their renewal or now. If any of them does not fit, nothing changes and the response lists each one with what would make it fit, to send back in changes.

### Parameters

- `id` (`str`, required)
- `code` (`str`, required)
- `subscribers` (`Literal["keep", "period_end", "now"]`, optional) — What happens to the experiment's subscribers: keep them on its versions, move them to the plan's current version at their next renewal, or move them now. Nobody moves, and the experiment keeps running, unless every one of them fits or has a change.
- `changes` (`list[ArchivePlanExperimentParamsChangesItem]`, optional) — Per-subscriber changes that make each one fit, applied at its renewal.
- `preview` (`bool`, optional) — Check the archive and the move without changing anything.

### Request options

- `idempotency_key` (`str`, optional) — Unique key used to safely retry this write for 24 hours without applying it twice.

### Returns

`PlanExperimentArchive`

## make_experiment_current

`commet.plans.make_experiment_current(...)`

`POST /plans/{id}/experiments/{code}/make-current` · operation `make-plan-experiment-current`

Make the experiment's latest version the plan's current version, with exactly its content and the next version number. New buyers get it; its subscribers are already on it. The experiment closes, and its code sells the plan's current version from then on. Nobody else moves.

### Parameters

- `id` (`str`, required)
- `code` (`str`, required)

### Request options

- `idempotency_key` (`str`, optional) — Unique key used to safely retry this write for 24 hours without applying it twice.

### Returns

`PlanVersion`

## get_experiment

`commet.plans.get_experiment(...)`

`GET /plans/{id}/experiments/{code}` · operation `get-plan-experiment`

Get one experiment of a plan by its own code, with the version it sells and how many subscriptions are on it.

### Parameters

- `id` (`str`, required)
- `code` (`str`, required)

### Returns

`PlanExperiment`

## create_experiment_version

`commet.plans.create_experiment_version(...)`

`POST /plans/{id}/experiments/{code}/versions` · operation `create-plan-experiment-version`

Publish the experiment's next version from its latest version with the changes given. Its code sells the new version from now on; subscribers on its earlier versions stay where they are until moved.

### Parameters

- `id` (`str`, required)
- `code` (`str`, required)
- `prices` (`list[CreatePlanExperimentVersionParamsPricesItem]`, optional)
- `currencies` (`list[CreatePlanExperimentVersionParamsCurrenciesItem]`, optional) — Currencies the current version does not sell, with the exchange rate (local units per USD) used for the amounts not listed, credit purchases, add-ons and overage.
- `max_plan_credits` (`int | null`, optional) — Credits plans that roll over unused credits: the most plan credits a subscription can hold. Null removes the cap.
- `max_plan_balance` (`int | null`, optional) — Balance plans that roll over unused balance: the most plan balance a subscription can hold, in USD cents. Other currencies convert it with the plan's exchange rate unless the dashboard sets a custom amount for that currency. Null removes the cap.

### Request options

- `idempotency_key` (`str`, optional) — Unique key used to safely retry this write for 24 hours without applying it twice.

### Returns

`PlanVersion`

## list_experiments

`commet.plans.list_experiments(...)`

`GET /plans/{id}/experiments` · operation `list-plan-experiments`

List a plan's experiments, newest first, with the version each one sells and how many subscriptions are on them.

### Parameters

- `id` (`str`, required)

### Returns

`PlansListExperimentsResult`

## create_experiment

`commet.plans.create_experiment(...)`

`POST /plans/{id}/experiments` · operation `create-plan-experiment`

Start an experiment from the plan's current version with the changes given. It is sold only through its code (planCode `<plan code>:<code>`); new buyers of the plan keep getting the current version.

### Parameters

- `id` (`str`, required)
- `prices` (`list[CreatePlanExperimentParamsPricesItem]`, optional)
- `currencies` (`list[CreatePlanExperimentParamsCurrenciesItem]`, optional) — Currencies the current version does not sell, with the exchange rate (local units per USD) used for the amounts not listed, credit purchases, add-ons and overage.
- `max_plan_credits` (`int | null`, optional) — Credits plans that roll over unused credits: the most plan credits a subscription can hold. Null removes the cap.
- `max_plan_balance` (`int | null`, optional) — Balance plans that roll over unused balance: the most plan balance a subscription can hold, in USD cents. Other currencies convert it with the plan's exchange rate unless the dashboard sets a custom amount for that currency. Null removes the cap.
- `code` (`str`, required) — The experiment's own code: lowercase letters, numbers, hyphens and underscores. It is sold as planCode `<plan code>:<code>` and is never reused in the plan.

### Request options

- `idempotency_key` (`str`, optional) — Unique key used to safely retry this write for 24 hours without applying it twice.

### Returns

`PlanExperiment`

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

## cancel_move

`commet.plans.cancel_move(...)`

`POST /plans/{id}/moves/{moveId}/cancel` · operation `cancel-plan-move`

Cancel a move for every subscriber who has not moved yet. They stay on their version; those already moved stay moved.

### Parameters

- `id` (`str`, required)
- `move_id` (`str`, required)

### Request options

- `idempotency_key` (`str`, optional) — Unique key used to safely retry this write for 24 hours without applying it twice.

### Returns

`PlanMove`

## get_move

`commet.plans.get_move(...)`

`GET /plans/{id}/moves/{moveId}` · operation `get-plan-move`

Read a move of subscribers between plan versions with each subscriber's status: moving, moved, needs a change, left out, canceled or kept on its version.

### Parameters

- `id` (`str`, required)
- `move_id` (`str`, required)

### Returns

`PlanMove`

## cancel_move_subscription

`commet.plans.cancel_move_subscription(...)`

`POST /plans/{id}/moves/{moveId}/subscriptions/{subscriptionId}/cancel` · operation `cancel-plan-move-subscription`

Cancel a move for one subscriber who has not moved yet. It stays on its version; the rest of the move continues.

### Parameters

- `id` (`str`, required)
- `move_id` (`str`, required)
- `subscription_id` (`str`, required)

### Request options

- `idempotency_key` (`str`, optional) — Unique key used to safely retry this write for 24 hours without applying it twice.

### Returns

`PlanMove`

## list_moves

`commet.plans.list_moves(...)`

`GET /plans/{id}/moves` · operation `list-plan-moves`

List a plan's latest moves of subscribers between versions, newest first, including the change of a single subscription, with how many are moving, moved, need a change, were left out, canceled or kept on their version.

### Parameters

- `id` (`str`, required)

### Returns

`PlansListMovesResult`

## create_move

`commet.plans.create_move(...)`

`POST /plans/{id}/moves` · operation `create-plan-move`

Move a list of subscriptions, or every subscription of another version, to a newer version of the plan, at their next renewal or now. Nobody moves unless every one of them fits or has a change in changes; otherwise the response lists each one with what would make it fit. Only active, trialing and past due subscriptions move. Paused ones, and listed subscriptions in another status or already on the destination, are left out. Send preview to check without moving anyone.

### Parameters

- `id` (`str`, required)
- `subscription_ids` (`list[str]`, optional) — Public IDs of the subscriptions to move.
- `to_version_id` (`str`, required) — The version subscribers move to.
- `effective` (`Literal["now", "period_end"]`, required) — now changes features and the included amount today and the price at renewal; period_end moves each subscriber at its next renewal.
- `changes` (`list[CreatePlanMoveParamsChangesItem]`, optional) — Per-subscriber changes that make each one fit, applied at its renewal.
- `preview` (`bool`, optional) — Check every subscriber without moving anyone.
- `from_version_id` (`str`, optional) — Move every active, trialing and past due subscription on this version of the plan.

### Valid parameter combinations

- `subscription_ids` + `to_version_id` + `effective`
- `from_version_id` + `to_version_id` + `effective`

### Request options

- `idempotency_key` (`str`, optional) — Unique key used to safely retry this write for 24 hours without applying it twice.

### Returns

`PlanMove`

## keep_subscriber_on_version

`commet.plans.keep_subscriber_on_version(...)`

`POST /plans/{id}/needs-a-change/{subscriptionId}/keep` · operation `keep-plan-subscriber-on-version`

Leave a subscriber that needs a change on its version. It stops appearing among the subscribers that need a change; move it later like any other subscriber.

### Parameters

- `id` (`str`, required)
- `subscription_id` (`str`, required)

### Request options

- `idempotency_key` (`str`, optional) — Unique key used to safely retry this write for 24 hours without applying it twice.

### Returns

`KeptOnVersion`

## list_subscribers_needing_achange

`commet.plans.list_subscribers_needing_achange(...)`

`GET /plans/{id}/needs-a-change` · operation `list-plan-subscribers-needing-a-change`

List the plan's subscribers whose move could not complete, with the version they stay on, the one they could not move to and why. Move them again with a change, or keep them on their version so they leave this list.

### Parameters

- `id` (`str`, required)

### Returns

`PlansListSubscribersNeedingAChangeResult`

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
- `trial_requires_payment_method` (`bool`, optional) — Set to false so the price's free trial starts without a payment method. Requires trialDays on the price.
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

Archive a price for new subscriptions. This publishes a new version of the plan; existing subscriptions that selected the price keep paying it on their version until moved.

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
- `billing_interval` (`Literal["weekly", "monthly", "quarterly", "semiannual", "yearly", "one_time"]`, required)
- `metadata` (`dict[str, Any]`, optional)
- `price` (`int`, optional)
- `trial_days` (`int`, optional)
- `trial_requires_payment_method` (`bool`, optional) — Set to false so the price's free trial starts without a payment method. Requires trialDays on the price.
- `is_default` (`bool`, optional)
- `included_balance` (`int | null`, optional)
- `included_credits` (`int | null`, optional)
- `market_prices` (`list[AddPlanPriceParamsMarketPricesItem]`, optional)
- `inherits_from_price_id` (`str`, optional)

### Valid parameter combinations

- `billing_interval` + `price`
- `billing_interval` + `inherits_from_price_id` + `market_prices`

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
- `currency` (`Literal["usd", "ars", "brl", "clp", "cop", "pen", "uyu", "pyg", "bob", "mxn", "cad", "eur", "gbp", "jpy", "cny", "krw", "hkd", "sgd", "twd", "inr", "thb"]`, required)
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

Update a plan's name, description, visibility, default status, metadata, overage behavior, what happens to its unused plan credits or plan balance, or its plan credit or plan balance limit.

### Parameters

- `id` (`str`, required)
- `name` (`str`, optional)
- `description` (`str | null`, optional)
- `metadata` (`dict[str, Any]`, optional)
- `is_public` (`bool`, optional)
- `unused_plan_credits` (`UpdatePlanParamsUnusedPlanCredits`, optional) — Credits plans only. What happens to unused plan credits at each reset. Changing it publishes a new version of the plan; each subscription stays on its version until moved.
- `plan_credit_limit` (`UpdatePlanParamsPlanCreditLimit | null`, optional) — Credits plans only. The most plan credits a subscription spends per day or per week; null removes the limit. Changing it publishes a new version of the plan; each subscription stays on its version until moved.
- `unused_plan_balance` (`UpdatePlanParamsUnusedPlanBalance`, optional) — Balance plans only. What happens to unused plan balance at each reset. Changing it publishes a new version of the plan; each subscription stays on its version until moved.
- `plan_balance_limit` (`UpdatePlanParamsPlanBalanceLimit | null`, optional) — Balance plans only. The most plan balance a subscription spends per day or per week, in USD cents; null removes the limit. Changing it publishes a new version of the plan; each subscription stays on its version until moved.
- `block_on_exhaustion` (`bool`, optional) — Credits and balance plans only. false lets usage continue past the plan and purchased amounts and bills the missing amount as overage at the next renewal; a credits plan bills it at the price per credit and needs one. Trials and free plans always stop, so free plans accept only true. Changing it publishes a new version of the plan; each subscription stays on its version until moved.
- `is_default` (`bool`, optional) — Make this plan the default plan of its plan group: customers created with that planGroupId start on it, and a paid plan of the group that ends from the customer portal, a revoked payment authorization or exhausted dunning moves to it instead of canceling. Requires a free plan in a plan group; replaces the group's previous default plan. false unmarks it.

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

## compare_versions

`commet.plans.compare_versions(...)`

`GET /plans/{id}/versions/{versionId}/changes` · operation `compare-plan-versions`

List what changes from one version of a plan to another: prices, trials, features, rules, add-ons, credit packs and countries.

### Parameters

- `id` (`str`, required)
- `version_id` (`str`, required)
- `against` (`str`, required)

### Returns

`PlanVersionComparison`

## get_version

`commet.plans.get_version(...)`

`GET /plans/{id}/versions/{versionId}` · operation `get-plan-version`

Get one published version of a plan with its prices and how many subscriptions are on it.

### Parameters

- `id` (`str`, required)
- `version_id` (`str`, required)

### Returns

`PlanVersion`

## list_versions

`commet.plans.list_versions(...)`

`GET /plans/{id}/versions` · operation `list-plan-versions`

List a plan's published versions, newest first, with their prices and how many subscriptions are on each. Versions published before Commet recorded every term are not listed.

### Parameters

- `id` (`str`, required)
- `cursor` (`str`, optional)
- `limit` (`int`, optional)

### Returns

`PlansListVersionsResult`

## create_version

`commet.plans.create_version(...)`

`POST /plans/{id}/versions` · operation `create-plan-version`

Publish a new current version of the plan from its current version, changing prices per interval, included credits or balance, per-currency amounts and the rollover cap. New buyers get it; every subscriber stays on its version until moved. To try changes without selling them to everyone, create an experiment instead.

### Parameters

- `id` (`str`, required)
- `prices` (`list[CreatePlanVersionParamsPricesItem]`, optional)
- `currencies` (`list[CreatePlanVersionParamsCurrenciesItem]`, optional) — Currencies the current version does not sell, with the exchange rate (local units per USD) used for the amounts not listed, credit purchases, add-ons and overage.
- `max_plan_credits` (`int | null`, optional) — Credits plans that roll over unused credits: the most plan credits a subscription can hold. Null removes the cap.
- `max_plan_balance` (`int | null`, optional) — Balance plans that roll over unused balance: the most plan balance a subscription can hold, in USD cents. Other currencies convert it with the plan's exchange rate unless the dashboard sets a custom amount for that currency. Null removes the cap.

### Request options

- `idempotency_key` (`str`, optional) — Unique key used to safely retry this write for 24 hours without applying it twice.

### Returns

`PlanVersion`

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

Create a new plan with optional consumption model, visibility, plan group assignment, overage behavior, and the rollover and spend limit of its plan credits or plan balance.

### Parameters

- `name` (`str`, required)
- `code` (`str`, required)
- `description` (`str`, optional)
- `consumption_model` (`Literal["metered", "credits", "balance"]`, optional)
- `is_public` (`bool`, optional)
- `is_free` (`bool`, optional)
- `block_on_exhaustion` (`bool`, optional) — Credits and balance plans. Omitted, credits plans and free plans stop usage when the plan and purchased amounts run out, and paid balance plans bill the missing balance as overage. A new credits plan always stops usage: it allows overage only with a price per credit, which is set after creation, and then `PATCH /v1/plans/{id}` turns overage on.
- `unused_plan_credits` (`CreatePlanParamsUnusedPlanCredits`, optional) — Credits plans only. What happens to unused plan credits at each reset; omitted means they expire.
- `plan_credit_limit` (`CreatePlanParamsPlanCreditLimit | null`, optional) — Credits plans only. The most plan credits a subscription spends per day or per week; omitted or null means no limit.
- `unused_plan_balance` (`CreatePlanParamsUnusedPlanBalance`, optional) — Balance plans only. What happens to unused plan balance at each reset; omitted means it expires.
- `plan_balance_limit` (`CreatePlanParamsPlanBalanceLimit | null`, optional) — Balance plans only. The most plan balance a subscription spends per day or per week, in USD cents; omitted or null means no limit.
- `plan_group_id` (`str`, optional)
- `is_default` (`bool`, optional) — Make this plan the default plan of its plan group: customers created with that planGroupId start on it, and a paid plan of the group that ends from the customer portal, a revoked payment authorization or exhausted dunning moves to it instead of canceling. Requires a free plan with a planGroupId; replaces the group's previous default plan.
- `metadata` (`dict[str, Any]`, optional)

### Request options

- `idempotency_key` (`str`, optional) — Unique key used to safely retry this write for 24 hours without applying it twice.

### Returns

`Plan`
