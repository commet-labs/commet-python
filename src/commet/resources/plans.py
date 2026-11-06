# ruff: noqa: E501

from __future__ import annotations

import builtins
from typing import Any, Literal

from .._http import CommetHTTPClient
from .._shared import build_body
from ..types import (
    AddPlanFeatureParamsOverage,
    AddPlanPriceParamsMarketPricesItem,
    CreatePlanParamsPlanBalanceLimit,
    CreatePlanParamsPlanCreditLimit,
    CreatePlanParamsUnusedPlanBalance,
    CreatePlanParamsUnusedPlanCredits,
    DeletedObject,
    DeletedPlanRegionalPricing,
    Plan,
    PlanFeature,
    PlanPrice,
    PlanRegionalPricing,
    PlanRegionalPricingResult,
    PlansListResult,
    RemovedPlanFeature,
    SetPlanRegionalPricingParamsFeaturesItem,
    SetPlanRegionalPricingParamsPricesItem,
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
        """Archive a price for new subscriptions. Existing subscriptions that selected it continue using its current catalog value."""
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
