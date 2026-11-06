# ruff: noqa: E501

from __future__ import annotations

import builtins
from typing import Any, Literal

from .._http import CommetHTTPClient
from .._shared import build_body
from ..types import (
    AddPlanFeatureParamsOverage,
    AddPlanPriceParamsMarketPricesItem,
    ArchivePlanExperimentParamsChangesItem,
    CreatePlanExperimentParamsCurrenciesItem,
    CreatePlanExperimentParamsPricesItem,
    CreatePlanExperimentVersionParamsCurrenciesItem,
    CreatePlanExperimentVersionParamsPricesItem,
    CreatePlanMoveParamsChangesItem,
    CreatePlanParamsPlanBalanceLimit,
    CreatePlanParamsPlanCreditLimit,
    CreatePlanParamsUnusedPlanBalance,
    CreatePlanParamsUnusedPlanCredits,
    CreatePlanVersionParamsCurrenciesItem,
    CreatePlanVersionParamsPricesItem,
    DeletedObject,
    DeletedPlanRegionalPricing,
    KeptOnVersion,
    Plan,
    PlanDraft,
    PlanDraftPublication,
    PlanExperiment,
    PlanExperimentArchive,
    PlanFeature,
    PlanMove,
    PlanPrice,
    PlanRegionalPricing,
    PlanRegionalPricingResult,
    PlansListDraftsResult,
    PlansListExperimentsResult,
    PlansListMovesResult,
    PlansListResult,
    PlansListSubscribersNeedingAChangeResult,
    PlansListVersionsResult,
    PlanVersion,
    PlanVersionComparison,
    PublishPlanDraftParamsChangesItem,
    RemovedPlanFeature,
    SetPlanRegionalPricingParamsFeaturesItem,
    SetPlanRegionalPricingParamsPricesItem,
    UpdatePlanDraftParamsCountriesItem,
    UpdatePlanDraftParamsPricesItem,
    UpdatePlanDraftParamsRules,
    UpdatePlanFeatureParamsOverage,
    UpdatePlanParamsPlanBalanceLimit,
    UpdatePlanParamsPlanCreditLimit,
    UpdatePlanParamsUnusedPlanBalance,
    UpdatePlanParamsUnusedPlanCredits,
    UpdatePlanPriceParamsMarketPricesItem,
    UpsertRegionalPricesParamsOverridesItem,
    _parse_data,
)


class PlansResource:
    def __init__(self, http: CommetHTTPClient) -> None:
        self._http = http

    def publish_draft(
        self,
        id: str,
        draft_id: str,
        *,
        publish_as: Literal["current", "experiment", "experiment_version"],
        move: Literal["keep", "period_end", "now"] | None = None,
        changes: builtins.list[PublishPlanDraftParamsChangesItem] | None = None,
        preview: bool | None = None,
        experiment_code: str | None = None,
        idempotency_key: str | None = None,
    ) -> PlanDraftPublication:
        """Publish a draft as the plan's current version, as a new experiment with its own code, or as the next version of the experiment it started from. A country missing a price, or removing the signup trial of the plan's group from the current version, stops the publication. With move, subscribers of earlier versions move at their renewal or now; if any of them does not fit the new version, nothing is published and the response lists each one with what would make it fit, to send back in changes. Paused subscribers stay where they are. Send preview to check without publishing."""
        body = build_body(
            publish_as=publish_as,
            move=move,
            changes=changes,
            preview=preview,
            experiment_code=experiment_code,
        )
        return _parse_data(
            self._http.post(
                f"/plans/{id}/drafts/{draft_id}/publish", body, idempotency_key=idempotency_key
            ),
            PlanDraftPublication,
        )

    def get_draft(self, id: str, draft_id: str) -> PlanDraft:
        """Retrieve a draft with the version it started from and what it changes."""
        return _parse_data(self._http.get(f"/plans/{id}/drafts/{draft_id}"), PlanDraft)

    def update_draft(
        self,
        id: str,
        draft_id: str,
        *,
        prices: builtins.list[UpdatePlanDraftParamsPricesItem] | None = None,
        countries: builtins.list[UpdatePlanDraftParamsCountriesItem] | None = None,
        rules: UpdatePlanDraftParamsRules | None = None,
        undo: builtins.list[str] | None = None,
        idempotency_key: str | None = None,
    ) -> PlanDraft:
        """Change a draft's prices per interval, trials, the interval shown first, countries with their currency and prices, and credit or balance rules, or undo single changes. Each block sent replaces that block; blocks left out stay as they are. Buyers and subscribers see nothing until the draft is published."""
        body = build_body(prices=prices, countries=countries, rules=rules, undo=undo)
        return _parse_data(
            self._http.patch(
                f"/plans/{id}/drafts/{draft_id}", body, idempotency_key=idempotency_key
            ),
            PlanDraft,
        )

    def delete_draft(self, id: str, draft_id: str) -> DeletedObject:
        """Discard a draft. Nothing it changed was ever sold."""
        return _parse_data(self._http.delete(f"/plans/{id}/drafts/{draft_id}"), DeletedObject)

    def list_drafts(self, id: str) -> PlansListDraftsResult:
        """List the plan's open drafts, oldest first, each with the version it started from and what it changes. Drafts sell nothing until published."""
        return _parse_data(self._http.get(f"/plans/{id}/drafts"), PlansListDraftsResult)

    def create_draft(
        self, id: str, *, from_version_id: str | None = None, idempotency_key: str | None = None
    ) -> PlanDraft:
        """Start a draft from a version of the plan: the current one, an experiment's version or an older one. A plan can have any number of drafts. Edit it, then publish it as the current version, as an experiment or as an experiment's next version; nothing changes for buyers or subscribers until then."""
        body = build_body(from_version_id=from_version_id)
        return _parse_data(
            self._http.post(f"/plans/{id}/drafts", body, idempotency_key=idempotency_key), PlanDraft
        )

    def archive_experiment(
        self,
        id: str,
        code: str,
        *,
        subscribers: Literal["keep", "period_end", "now"] | None = None,
        changes: builtins.list[ArchivePlanExperimentParamsChangesItem] | None = None,
        preview: bool | None = None,
        idempotency_key: str | None = None,
    ) -> PlanExperimentArchive:
        """Stop selling the experiment. Its code sells the plan's current version from then on, so links already shared keep working. Choose what happens to its subscribers: keep them on its versions, or move them to the current version at their renewal or now. If any of them does not fit, nothing changes and the response lists each one with what would make it fit, to send back in changes."""
        body = build_body(subscribers=subscribers, changes=changes, preview=preview)
        return _parse_data(
            self._http.post(
                f"/plans/{id}/experiments/{code}/archive", body, idempotency_key=idempotency_key
            ),
            PlanExperimentArchive,
        )

    def make_experiment_current(
        self, id: str, code: str, *, idempotency_key: str | None = None
    ) -> PlanVersion:
        """Make the experiment's latest version the plan's current version, with exactly its content and the next version number. New buyers get it; its subscribers are already on it. The experiment closes, and its code sells the plan's current version from then on. Nobody else moves."""
        return _parse_data(
            self._http.post(
                f"/plans/{id}/experiments/{code}/make-current", idempotency_key=idempotency_key
            ),
            PlanVersion,
        )

    def get_experiment(self, id: str, code: str) -> PlanExperiment:
        """Get one experiment of a plan by its own code, with the version it sells and how many subscriptions are on it."""
        return _parse_data(self._http.get(f"/plans/{id}/experiments/{code}"), PlanExperiment)

    def create_experiment_version(
        self,
        id: str,
        code: str,
        *,
        prices: builtins.list[CreatePlanExperimentVersionParamsPricesItem] | None = None,
        currencies: builtins.list[CreatePlanExperimentVersionParamsCurrenciesItem] | None = None,
        max_plan_credits: int | None = None,
        max_plan_balance: int | None = None,
        idempotency_key: str | None = None,
    ) -> PlanVersion:
        """Publish the experiment's next version from its latest version with the changes given. Its code sells the new version from now on; subscribers on its earlier versions stay where they are until moved."""
        body = build_body(
            prices=prices,
            currencies=currencies,
            max_plan_credits=max_plan_credits,
            max_plan_balance=max_plan_balance,
        )
        return _parse_data(
            self._http.post(
                f"/plans/{id}/experiments/{code}/versions", body, idempotency_key=idempotency_key
            ),
            PlanVersion,
        )

    def list_experiments(self, id: str) -> PlansListExperimentsResult:
        """List a plan's experiments, newest first, with the version each one sells and how many subscriptions are on them."""
        return _parse_data(self._http.get(f"/plans/{id}/experiments"), PlansListExperimentsResult)

    def create_experiment(
        self,
        id: str,
        *,
        code: str,
        prices: builtins.list[CreatePlanExperimentParamsPricesItem] | None = None,
        currencies: builtins.list[CreatePlanExperimentParamsCurrenciesItem] | None = None,
        max_plan_credits: int | None = None,
        max_plan_balance: int | None = None,
        idempotency_key: str | None = None,
    ) -> PlanExperiment:
        """Start an experiment from the plan's current version with the changes given. It is sold only through its code (planCode `<plan code>:<code>`); new buyers of the plan keep getting the current version."""
        body = build_body(
            prices=prices,
            currencies=currencies,
            max_plan_credits=max_plan_credits,
            max_plan_balance=max_plan_balance,
            code=code,
        )
        return _parse_data(
            self._http.post(f"/plans/{id}/experiments", body, idempotency_key=idempotency_key),
            PlanExperiment,
        )

    def update_feature(
        self,
        id: str,
        feature_id: str,
        *,
        enabled: bool | None = None,
        included_amount: int | None = None,
        unlimited: bool | None = None,
        overage: UpdatePlanFeatureParamsOverage | None = None,
        credits_per_unit: int | None = None,
        idempotency_key: str | None = None,
    ) -> PlanFeature:
        """Update limits, overage, or enabled status of a feature on a plan."""
        body = build_body(
            enabled=enabled,
            included_amount=included_amount,
            unlimited=unlimited,
            overage=overage,
            credits_per_unit=credits_per_unit,
        )
        return _parse_data(
            self._http.patch(
                f"/plans/{id}/features/{feature_id}", body, idempotency_key=idempotency_key
            ),
            PlanFeature,
        )

    def remove_feature(self, id: str, feature_id: str) -> RemovedPlanFeature:
        """Detach a feature from a plan."""
        return _parse_data(
            self._http.delete(f"/plans/{id}/features/{feature_id}"), RemovedPlanFeature
        )

    def add_feature(
        self,
        id: str,
        *,
        feature_id: str,
        enabled: bool | None = None,
        included_amount: int | None = None,
        unlimited: bool | None = None,
        overage: AddPlanFeatureParamsOverage | None = None,
        credits_per_unit: int | None = None,
        pricing_mode: Literal["fixed", "ai_model"] | None = None,
        margin: int | None = None,
        idempotency_key: str | None = None,
    ) -> PlanFeature:
        """Attach a feature to a plan with limits, overage, and credits configuration."""
        body = build_body(
            feature_id=feature_id,
            enabled=enabled,
            included_amount=included_amount,
            unlimited=unlimited,
            overage=overage,
            credits_per_unit=credits_per_unit,
            pricing_mode=pricing_mode,
            margin=margin,
        )
        return _parse_data(
            self._http.post(f"/plans/{id}/features", body, idempotency_key=idempotency_key),
            PlanFeature,
        )

    def cancel_move(self, id: str, move_id: str, *, idempotency_key: str | None = None) -> PlanMove:
        """Cancel a move for every subscriber who has not moved yet. They stay on their version; those already moved stay moved."""
        return _parse_data(
            self._http.post(f"/plans/{id}/moves/{move_id}/cancel", idempotency_key=idempotency_key),
            PlanMove,
        )

    def get_move(self, id: str, move_id: str) -> PlanMove:
        """Read a move of subscribers between plan versions with each subscriber's status: moving, moved, needs a change, left out, canceled or kept on its version."""
        return _parse_data(self._http.get(f"/plans/{id}/moves/{move_id}"), PlanMove)

    def cancel_move_subscription(
        self, id: str, move_id: str, subscription_id: str, *, idempotency_key: str | None = None
    ) -> PlanMove:
        """Cancel a move for one subscriber who has not moved yet. It stays on its version; the rest of the move continues."""
        return _parse_data(
            self._http.post(
                f"/plans/{id}/moves/{move_id}/subscriptions/{subscription_id}/cancel",
                idempotency_key=idempotency_key,
            ),
            PlanMove,
        )

    def list_moves(self, id: str) -> PlansListMovesResult:
        """List a plan's latest moves of subscribers between versions, newest first, with how many are moving, moved, need a change, were left out, canceled or kept on their version."""
        return _parse_data(self._http.get(f"/plans/{id}/moves"), PlansListMovesResult)

    def create_move(
        self,
        id: str,
        *,
        to_version_id: str,
        effective: Literal["now", "period_end"],
        subscription_ids: builtins.list[str] | None = None,
        changes: builtins.list[CreatePlanMoveParamsChangesItem] | None = None,
        preview: bool | None = None,
        from_version_id: str | None = None,
        idempotency_key: str | None = None,
    ) -> PlanMove:
        """Move a list of subscriptions, or every subscription of another version, to a newer version of the plan, at their next renewal or now. Nobody moves unless every one of them fits or has a change in changes; otherwise the response lists each one with what would make it fit. Only active, trialing and past due subscriptions move. Paused ones, and listed subscriptions in another status or already on the destination, are left out. Send preview to check without moving anyone."""
        body = build_body(
            subscription_ids=subscription_ids,
            to_version_id=to_version_id,
            effective=effective,
            changes=changes,
            preview=preview,
            from_version_id=from_version_id,
        )
        return _parse_data(
            self._http.post(f"/plans/{id}/moves", body, idempotency_key=idempotency_key), PlanMove
        )

    def keep_subscriber_on_version(
        self, id: str, subscription_id: str, *, idempotency_key: str | None = None
    ) -> KeptOnVersion:
        """Leave a subscriber that needs a change on its version. It stops appearing among the subscribers that need a change; move it later like any other subscriber."""
        return _parse_data(
            self._http.post(
                f"/plans/{id}/needs-a-change/{subscription_id}/keep",
                idempotency_key=idempotency_key,
            ),
            KeptOnVersion,
        )

    def list_subscribers_needing_a_change(
        self, id: str
    ) -> PlansListSubscribersNeedingAChangeResult:
        """List the plan's subscribers whose move could not complete, with the version they stay on, the one they could not move to and why. Move them again with a change, or keep them on their version so they leave this list."""
        return _parse_data(
            self._http.get(f"/plans/{id}/needs-a-change"), PlansListSubscribersNeedingAChangeResult
        )

    def set_default_price(
        self, id: str, price_id: str, *, idempotency_key: str | None = None
    ) -> PlanPrice:
        """Set a specific price as the default and return the updated plan price."""
        return _parse_data(
            self._http.put(
                f"/plans/{id}/prices/{price_id}/default", idempotency_key=idempotency_key
            ),
            PlanPrice,
        )

    def set_regional_prices(
        self,
        id: str,
        price_id: str,
        *,
        overrides: builtins.list[UpsertRegionalPricesParamsOverridesItem],
        idempotency_key: str | None = None,
    ) -> PlanRegionalPricing:
        """Create or update regional currency price overrides for a plan price."""
        body = build_body(overrides=overrides)
        return _parse_data(
            self._http.put(
                f"/plans/{id}/prices/{price_id}/regional", body, idempotency_key=idempotency_key
            ),
            PlanRegionalPricing,
        )

    def delete_regional_prices(self, id: str, price_id: str) -> DeletedPlanRegionalPricing:
        """Remove all regional currency overrides for a plan price. The request is rejected while billable subscriptions depend on an override."""
        return _parse_data(
            self._http.delete(f"/plans/{id}/prices/{price_id}/regional"), DeletedPlanRegionalPricing
        )

    def update_price(
        self,
        id: str,
        price_id: str,
        *,
        price: int | None = None,
        is_default: bool | None = None,
        trial_days: int | None = None,
        trial_requires_payment_method: bool | None = None,
        included_balance: int | None = None,
        included_credits: int | None = None,
        metadata: dict[str, Any] | None = None,
        market_prices: builtins.list[UpdatePlanPriceParamsMarketPricesItem] | None = None,
        idempotency_key: str | None = None,
    ) -> PlanPrice:
        """Update a base price or market price variant. Removing a base market override is rejected while a variant depends on it. Offer terms are managed through Offers."""
        body = build_body(
            price=price,
            is_default=is_default,
            trial_days=trial_days,
            trial_requires_payment_method=trial_requires_payment_method,
            included_balance=included_balance,
            included_credits=included_credits,
            metadata=metadata,
            market_prices=market_prices,
        )
        return _parse_data(
            self._http.patch(
                f"/plans/{id}/prices/{price_id}", body, idempotency_key=idempotency_key
            ),
            PlanPrice,
        )

    def delete_price(self, id: str, price_id: str) -> DeletedObject:
        """Archive a price for new subscriptions. This publishes a new version of the plan; existing subscriptions that selected the price keep paying it on their version until moved."""
        return _parse_data(self._http.delete(f"/plans/{id}/prices/{price_id}"), DeletedObject)

    def add_price(
        self,
        id: str,
        *,
        billing_interval: Literal[
            "weekly", "monthly", "quarterly", "semiannual", "yearly", "one_time"
        ],
        metadata: dict[str, Any] | None = None,
        price: int | None = None,
        trial_days: int | None = None,
        trial_requires_payment_method: bool | None = None,
        is_default: bool | None = None,
        included_balance: int | None = None,
        included_credits: int | None = None,
        market_prices: builtins.list[AddPlanPriceParamsMarketPricesItem] | None = None,
        inherits_from_price_id: str | None = None,
        idempotency_key: str | None = None,
    ) -> PlanPrice:
        """Add a base price or a selectable market price variant. Variants inherit their base price outside the markets they override. Configure introductory and promotional benefits through Offers."""
        body = build_body(
            billing_interval=billing_interval,
            metadata=metadata,
            price=price,
            trial_days=trial_days,
            trial_requires_payment_method=trial_requires_payment_method,
            is_default=is_default,
            included_balance=included_balance,
            included_credits=included_credits,
            market_prices=market_prices,
            inherits_from_price_id=inherits_from_price_id,
        )
        return _parse_data(
            self._http.post(f"/plans/{id}/prices", body, idempotency_key=idempotency_key), PlanPrice
        )

    def set_regional_pricing(
        self,
        id: str,
        *,
        currency: Literal[
            "usd",
            "ars",
            "brl",
            "clp",
            "cop",
            "pen",
            "uyu",
            "pyg",
            "bob",
            "mxn",
            "cad",
            "eur",
            "gbp",
            "jpy",
            "cny",
            "krw",
            "hkd",
            "sgd",
            "twd",
            "inr",
            "thb",
        ],
        exchange_rate: float,
        prices: builtins.list[SetPlanRegionalPricingParamsPricesItem] | None = None,
        features: builtins.list[SetPlanRegionalPricingParamsFeaturesItem] | None = None,
        idempotency_key: str | None = None,
    ) -> PlanRegionalPricingResult:
        """Configure regional prices and feature overage values for one currency. Currency-specific offer terms are managed through Offers."""
        body = build_body(
            currency=currency, exchange_rate=exchange_rate, prices=prices, features=features
        )
        return _parse_data(
            self._http.put(f"/plans/{id}/regional", body, idempotency_key=idempotency_key),
            PlanRegionalPricingResult,
        )

    def get(self, id: str) -> Plan:
        """Get a plan with public price IDs and their automatic introductory offer IDs."""
        return _parse_data(self._http.get(f"/plans/{id}"), Plan)

    def update(
        self,
        id: str,
        *,
        name: str | None = None,
        description: str | None = None,
        metadata: dict[str, Any] | None = None,
        is_public: bool | None = None,
        unused_plan_credits: UpdatePlanParamsUnusedPlanCredits | None = None,
        plan_credit_limit: UpdatePlanParamsPlanCreditLimit | None = None,
        unused_plan_balance: UpdatePlanParamsUnusedPlanBalance | None = None,
        plan_balance_limit: UpdatePlanParamsPlanBalanceLimit | None = None,
        block_on_exhaustion: bool | None = None,
        is_default: bool | None = None,
        idempotency_key: str | None = None,
    ) -> Plan:
        """Update a plan's name, description, visibility, default status, metadata, overage behavior, what happens to its unused plan credits or plan balance, or its plan credit or plan balance limit."""
        body = build_body(
            name=name,
            description=description,
            metadata=metadata,
            is_public=is_public,
            unused_plan_credits=unused_plan_credits,
            plan_credit_limit=plan_credit_limit,
            unused_plan_balance=unused_plan_balance,
            plan_balance_limit=plan_balance_limit,
            block_on_exhaustion=block_on_exhaustion,
            is_default=is_default,
        )
        return _parse_data(
            self._http.patch(f"/plans/{id}", body, idempotency_key=idempotency_key), Plan
        )

    def delete(self, id: str) -> DeletedObject:
        """Soft-delete a plan."""
        return _parse_data(self._http.delete(f"/plans/{id}"), DeletedObject)

    def compare_versions(self, id: str, version_id: str, *, against: str) -> PlanVersionComparison:
        """List what changes from one version of a plan to another: prices, trials, features, rules, add-ons, credit packs and countries."""
        query = build_body(against=against)
        return _parse_data(
            self._http.get(f"/plans/{id}/versions/{version_id}/changes", query),
            PlanVersionComparison,
        )

    def get_version(self, id: str, version_id: str) -> PlanVersion:
        """Get one published version of a plan with its prices and how many subscriptions are on it."""
        return _parse_data(self._http.get(f"/plans/{id}/versions/{version_id}"), PlanVersion)

    def list_versions(
        self, id: str, *, cursor: str | None = None, limit: int | None = None
    ) -> PlansListVersionsResult:
        """List a plan's published versions, newest first, with their prices and how many subscriptions are on each. Versions published before Commet recorded every term are not listed."""
        query = build_body(cursor=cursor, limit=limit)
        return _parse_data(self._http.get(f"/plans/{id}/versions", query), PlansListVersionsResult)

    def create_version(
        self,
        id: str,
        *,
        prices: builtins.list[CreatePlanVersionParamsPricesItem] | None = None,
        currencies: builtins.list[CreatePlanVersionParamsCurrenciesItem] | None = None,
        max_plan_credits: int | None = None,
        max_plan_balance: int | None = None,
        idempotency_key: str | None = None,
    ) -> PlanVersion:
        """Publish a new current version of the plan from its current version, changing prices per interval, included credits or balance, per-currency amounts and the rollover cap. New buyers get it; every subscriber stays on its version until moved. To try changes without selling them to everyone, create an experiment instead."""
        body = build_body(
            prices=prices,
            currencies=currencies,
            max_plan_credits=max_plan_credits,
            max_plan_balance=max_plan_balance,
        )
        return _parse_data(
            self._http.post(f"/plans/{id}/versions", body, idempotency_key=idempotency_key),
            PlanVersion,
        )

    def set_visibility(
        self, id: str, *, is_public: bool, idempotency_key: str | None = None
    ) -> Plan:
        """Set a plan's public visibility and return the updated plan."""
        body = build_body(is_public=is_public)
        return _parse_data(
            self._http.put(f"/plans/{id}/visibility", body, idempotency_key=idempotency_key), Plan
        )

    def list(self, *, include_private: bool | None = None) -> PlansListResult:
        """List plans with public price IDs and their automatic introductory offer IDs."""
        query = build_body(include_private=include_private)
        return _parse_data(self._http.get("/plans", query), PlansListResult)

    def create(
        self,
        *,
        name: str,
        code: str,
        description: str | None = None,
        consumption_model: Literal["metered", "credits", "balance"] | None = None,
        is_public: bool | None = None,
        is_free: bool | None = None,
        block_on_exhaustion: bool | None = None,
        unused_plan_credits: CreatePlanParamsUnusedPlanCredits | None = None,
        plan_credit_limit: CreatePlanParamsPlanCreditLimit | None = None,
        unused_plan_balance: CreatePlanParamsUnusedPlanBalance | None = None,
        plan_balance_limit: CreatePlanParamsPlanBalanceLimit | None = None,
        plan_group_id: str | None = None,
        is_default: bool | None = None,
        metadata: dict[str, Any] | None = None,
        idempotency_key: str | None = None,
    ) -> Plan:
        """Create a new plan with optional consumption model, visibility, plan group assignment, overage behavior, and the rollover and spend limit of its plan credits or plan balance."""
        body = build_body(
            name=name,
            code=code,
            description=description,
            consumption_model=consumption_model,
            is_public=is_public,
            is_free=is_free,
            block_on_exhaustion=block_on_exhaustion,
            unused_plan_credits=unused_plan_credits,
            plan_credit_limit=plan_credit_limit,
            unused_plan_balance=unused_plan_balance,
            plan_balance_limit=plan_balance_limit,
            plan_group_id=plan_group_id,
            is_default=is_default,
            metadata=metadata,
        )
        return _parse_data(self._http.post("/plans", body, idempotency_key=idempotency_key), Plan)
