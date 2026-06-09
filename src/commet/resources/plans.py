# ruff: noqa: E501

from __future__ import annotations

import builtins
from typing import Any, Literal

from .._http import ApiResponse, CommetHTTPClient
from .._shared import build_body
from ..types import (
    AddPlanFeatureParamsOverage,
    AddPlanPriceParamsIntroOffer,
    BillingInterval,
    ConsumptionModel,
    DefaultPlanPrice,
    DeletedObject,
    DeletedPlanRegionalPricing,
    Plan,
    PlanFeature,
    PlanPrice,
    PlanRegionalPricing,
    PlanRegionalPricingResult,
    PlanVisibility,
    RemovedPlanFeature,
    SetPlanRegionalPricingParamsFeaturesItem,
    SetPlanRegionalPricingParamsIntroOffersItem,
    SetPlanRegionalPricingParamsPricesItem,
    UpdatePlanFeatureParamsOverage,
    UpdatePlanPriceParamsIntroOffer,
    UpsertRegionalPricesParamsOverridesItem,
    _parse,
    _parse_list,
)


class PlansResource:
    def __init__(self, http: CommetHTTPClient) -> None:
        self._http = http

    def list(
        self, *, include_private: Literal["true", "false"] | None = None
    ) -> ApiResponse[list[Plan]]:
        """List all plans with their prices and features. Optionally include private plans."""
        query = build_body(include_private=include_private)
        return _parse_list(self._http.get("/plans", query), Plan)

    def get(self, id: str) -> ApiResponse[Plan]:
        """Get detailed plan information by code or ID."""
        return _parse(self._http.get(f"/plans/{id}"), Plan)

    def create(
        self,
        *,
        name: str,
        code: str,
        description: str | None = None,
        consumption_model: ConsumptionModel | None = None,
        is_public: bool | None = None,
        is_free: bool | None = None,
        block_on_exhaustion: bool | None = None,
        plan_group_id: str | None = None,
        metadata: dict[str, Any] | None = None,
        idempotency_key: str | None = None,
    ) -> ApiResponse[Plan]:
        """Create a new plan with optional consumption model, visibility, and plan group assignment."""
        body = build_body(
            name=name,
            code=code,
            description=description,
            consumption_model=consumption_model,
            is_public=is_public,
            is_free=is_free,
            block_on_exhaustion=block_on_exhaustion,
            plan_group_id=plan_group_id,
            metadata=metadata,
        )
        return _parse(self._http.post("/plans/manage", body, idempotency_key=idempotency_key), Plan)

    def update(
        self,
        id: str,
        *,
        name: str | None = None,
        description: str | None = None,
        metadata: dict[str, Any] | None = None,
        is_public: bool | None = None,
        idempotency_key: str | None = None,
    ) -> ApiResponse[Plan]:
        """Update a plan's name, description, visibility, or metadata."""
        body = build_body(
            name=name, description=description, metadata=metadata, is_public=is_public
        )
        return _parse(
            self._http.put(f"/plans/{id}/manage", body, idempotency_key=idempotency_key), Plan
        )

    def delete(self, id: str) -> ApiResponse[DeletedObject]:
        """Soft-delete a plan."""
        return _parse(self._http.delete(f"/plans/{id}/manage"), DeletedObject)

    def set_visibility(
        self, id: str, *, is_public: bool, idempotency_key: str | None = None
    ) -> ApiResponse[PlanVisibility]:
        """Toggle a plan between public and private."""
        body = build_body(is_public=is_public)
        return _parse(
            self._http.put(f"/plans/{id}/visibility", body, idempotency_key=idempotency_key),
            PlanVisibility,
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
    ) -> ApiResponse[PlanFeature]:
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
        return _parse(
            self._http.post(f"/plans/{id}/features", body, idempotency_key=idempotency_key),
            PlanFeature,
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
    ) -> ApiResponse[PlanFeature]:
        """Update limits, overage, or enabled status of a feature on a plan."""
        body = build_body(
            enabled=enabled,
            included_amount=included_amount,
            unlimited=unlimited,
            overage=overage,
            credits_per_unit=credits_per_unit,
        )
        return _parse(
            self._http.put(
                f"/plans/{id}/features/{feature_id}", body, idempotency_key=idempotency_key
            ),
            PlanFeature,
        )

    def remove_feature(self, id: str, feature_id: str) -> ApiResponse[RemovedPlanFeature]:
        """Detach a feature from a plan."""
        return _parse(self._http.delete(f"/plans/{id}/features/{feature_id}"), RemovedPlanFeature)

    def add_price(
        self,
        id: str,
        *,
        billing_interval: BillingInterval,
        price: int,
        trial_days: int | None = None,
        is_default: bool | None = None,
        included_balance: int | None = None,
        included_credits: int | None = None,
        intro_offer: AddPlanPriceParamsIntroOffer | None = None,
        idempotency_key: str | None = None,
    ) -> ApiResponse[PlanPrice]:
        """Add a billing interval price to a plan with optional trial days and included balance/credits."""
        body = build_body(
            billing_interval=billing_interval,
            price=price,
            trial_days=trial_days,
            is_default=is_default,
            included_balance=included_balance,
            included_credits=included_credits,
            intro_offer=intro_offer,
        )
        return _parse(
            self._http.post(f"/plans/{id}/prices", body, idempotency_key=idempotency_key), PlanPrice
        )

    def update_price(
        self,
        id: str,
        price_id: str,
        *,
        price: int | None = None,
        is_default: bool | None = None,
        trial_days: int | None = None,
        included_balance: int | None = None,
        included_credits: int | None = None,
        intro_offer: UpdatePlanPriceParamsIntroOffer | None = None,
        idempotency_key: str | None = None,
    ) -> ApiResponse[PlanPrice]:
        """Update an existing price on a plan."""
        body = build_body(
            price=price,
            is_default=is_default,
            trial_days=trial_days,
            included_balance=included_balance,
            included_credits=included_credits,
            intro_offer=intro_offer,
        )
        return _parse(
            self._http.put(f"/plans/{id}/prices/{price_id}", body, idempotency_key=idempotency_key),
            PlanPrice,
        )

    def delete_price(self, id: str, price_id: str) -> ApiResponse[DeletedObject]:
        """Remove a price from a plan."""
        return _parse(self._http.delete(f"/plans/{id}/prices/{price_id}"), DeletedObject)

    def set_default_price(
        self, id: str, price_id: str, *, idempotency_key: str | None = None
    ) -> ApiResponse[DefaultPlanPrice]:
        """Set a specific price as the default for its plan. Unsets previous default."""
        return _parse(
            self._http.put(
                f"/plans/{id}/prices/{price_id}/default", idempotency_key=idempotency_key
            ),
            DefaultPlanPrice,
        )

    def set_regional_prices(
        self,
        id: str,
        price_id: str,
        *,
        overrides: builtins.list[UpsertRegionalPricesParamsOverridesItem],
        idempotency_key: str | None = None,
    ) -> ApiResponse[PlanRegionalPricing]:
        """Create or update regional currency price overrides for a plan price."""
        body = build_body(overrides=overrides)
        return _parse(
            self._http.put(
                f"/plans/{id}/prices/{price_id}/regional", body, idempotency_key=idempotency_key
            ),
            PlanRegionalPricing,
        )

    def set_regional_pricing(
        self,
        id: str,
        *,
        currency: Literal[
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
        intro_offers: builtins.list[SetPlanRegionalPricingParamsIntroOffersItem] | None = None,
        idempotency_key: str | None = None,
    ) -> ApiResponse[PlanRegionalPricingResult]:
        """Configure a plan's regional pricing for one currency. Sending only currency and exchangeRate derives every regional value (base price, included balance, feature overage, intro offer) from the USD value at that rate. Optional per-price and per-feature overrides are stored as manual values."""
        body = build_body(
            currency=currency,
            exchange_rate=exchange_rate,
            prices=prices,
            features=features,
            intro_offers=intro_offers,
        )
        return _parse(
            self._http.put(f"/plans/{id}/regional", body, idempotency_key=idempotency_key),
            PlanRegionalPricingResult,
        )

    def delete_regional_prices(
        self, id: str, price_id: str
    ) -> ApiResponse[DeletedPlanRegionalPricing]:
        """Remove all regional currency overrides for a plan price."""
        return _parse(
            self._http.delete(f"/plans/{id}/prices/{price_id}/regional"), DeletedPlanRegionalPricing
        )
