from __future__ import annotations

from typing import Any

from .._http import ApiResponse, CommetHTTPClient
from .._resource_mixins import (
    parse_delete_result,
    parse_plan_detail,
    parse_plan_feature_manage,
    parse_plan_list,
    parse_plan_manage,
    parse_plan_price_manage,
    parse_regional_price_result,
    parse_remove_result,
)
from .._shared import build_body
from ..types import (
    ConsumptionModel,
    DeleteResult,
    Plan,
    PlanDetail,
    PlanFeatureManage,
    PlanManage,
    PlanPriceManage,
    RegionalPriceResult,
    RemoveResult,
)


class PlansResource:
    def __init__(self, http: CommetHTTPClient) -> None:
        self._http = http

    def list(
        self,
        *,
        include_private: bool | None = None,
        limit: int | None = None,
        cursor: str | None = None,
    ) -> ApiResponse[list[Plan]]:
        return parse_plan_list(self._http.get("/plans", build_body(
            include_private=include_private, limit=limit, cursor=cursor
        )))

    def get(self, plan_id: str) -> ApiResponse[PlanDetail]:
        return parse_plan_detail(self._http.get(f"/plans/{plan_id}"))

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
    ) -> ApiResponse[PlanManage]:
        return parse_plan_manage(self._http.post(
            "/plans/manage",
            build_body(
                name=name, code=code, description=description,
                consumption_model=consumption_model, is_public=is_public,
                is_free=is_free, block_on_exhaustion=block_on_exhaustion,
                plan_group_id=plan_group_id, metadata=metadata,
            ),
            idempotency_key=idempotency_key,
        ))

    def update(
        self,
        plan_id: str,
        *,
        name: str | None = None,
        description: str | None = None,
        metadata: dict[str, Any] | None = None,
        is_public: bool | None = None,
        idempotency_key: str | None = None,
    ) -> ApiResponse[PlanManage]:
        return parse_plan_manage(self._http.put(
            f"/plans/{plan_id}/manage",
            build_body(name=name, description=description, metadata=metadata, is_public=is_public),
            idempotency_key=idempotency_key,
        ))

    def delete(
        self,
        plan_id: str,
        *,
        idempotency_key: str | None = None,
    ) -> ApiResponse[DeleteResult]:
        return parse_delete_result(
            self._http.delete(f"/plans/{plan_id}/manage", idempotency_key=idempotency_key)
        )

    def set_visibility(
        self,
        plan_id: str,
        *,
        is_public: bool,
        idempotency_key: str | None = None,
    ) -> ApiResponse[PlanManage]:
        return parse_plan_manage(self._http.put(
            f"/plans/{plan_id}/visibility",
            build_body(is_public=is_public),
            idempotency_key=idempotency_key,
        ))

    def add_feature(
        self,
        plan_id: str,
        *,
        feature_id: str,
        enabled: bool | None = None,
        included_amount: int | None = None,
        unlimited: bool | None = None,
        overage_enabled: bool | None = None,
        credits_per_unit: int | None = None,
        pricing_mode: str | None = None,
        overage_unit_price: int | None = None,
        margin: int | None = None,
        idempotency_key: str | None = None,
    ) -> ApiResponse[PlanFeatureManage]:
        return parse_plan_feature_manage(self._http.post(
            f"/plans/{plan_id}/features",
            build_body(
                feature_id=feature_id, enabled=enabled, included_amount=included_amount,
                unlimited=unlimited, overage_enabled=overage_enabled,
                credits_per_unit=credits_per_unit, pricing_mode=pricing_mode,
                overage_unit_price=overage_unit_price, margin=margin,
            ),
            idempotency_key=idempotency_key,
        ))

    def update_feature(
        self,
        plan_id: str,
        feature_id: str,
        *,
        enabled: bool | None = None,
        included_amount: int | None = None,
        unlimited: bool | None = None,
        overage_enabled: bool | None = None,
        credits_per_unit: int | None = None,
        pricing_mode: str | None = None,
        overage_unit_price: int | None = None,
        margin: int | None = None,
        idempotency_key: str | None = None,
    ) -> ApiResponse[PlanFeatureManage]:
        return parse_plan_feature_manage(self._http.put(
            f"/plans/{plan_id}/features/{feature_id}",
            build_body(
                enabled=enabled, included_amount=included_amount,
                unlimited=unlimited, overage_enabled=overage_enabled,
                credits_per_unit=credits_per_unit, pricing_mode=pricing_mode,
                overage_unit_price=overage_unit_price, margin=margin,
            ),
            idempotency_key=idempotency_key,
        ))

    def remove_feature(
        self,
        plan_id: str,
        feature_id: str,
        *,
        idempotency_key: str | None = None,
    ) -> ApiResponse[RemoveResult]:
        return parse_remove_result(self._http.delete(
            f"/plans/{plan_id}/features/{feature_id}",
            idempotency_key=idempotency_key,
        ))

    def add_price(
        self,
        plan_id: str,
        *,
        billing_interval: str,
        price: int,
        trial_days: int | None = None,
        is_default: bool | None = None,
        included_balance: int | None = None,
        included_credits: int | None = None,
        intro_offer_enabled: bool | None = None,
        intro_offer_discount_type: str | None = None,
        intro_offer_discount_value: int | None = None,
        intro_offer_duration_cycles: int | None = None,
        idempotency_key: str | None = None,
    ) -> ApiResponse[PlanPriceManage]:
        return parse_plan_price_manage(self._http.post(
            f"/plans/{plan_id}/prices",
            build_body(
                billing_interval=billing_interval, price=price, trial_days=trial_days,
                is_default=is_default, included_balance=included_balance,
                included_credits=included_credits, intro_offer_enabled=intro_offer_enabled,
                intro_offer_discount_type=intro_offer_discount_type,
                intro_offer_discount_value=intro_offer_discount_value,
                intro_offer_duration_cycles=intro_offer_duration_cycles,
            ),
            idempotency_key=idempotency_key,
        ))

    def update_price(
        self,
        plan_id: str,
        price_id: str,
        *,
        price: int | None = None,
        is_default: bool | None = None,
        trial_days: int | None = None,
        included_balance: int | None = None,
        included_credits: int | None = None,
        intro_offer_enabled: bool | None = None,
        intro_offer_discount_type: str | None = None,
        intro_offer_discount_value: int | None = None,
        intro_offer_duration_cycles: int | None = None,
        idempotency_key: str | None = None,
    ) -> ApiResponse[PlanPriceManage]:
        return parse_plan_price_manage(self._http.put(
            f"/plans/{plan_id}/prices/{price_id}",
            build_body(
                price=price, is_default=is_default, trial_days=trial_days,
                included_balance=included_balance, included_credits=included_credits,
                intro_offer_enabled=intro_offer_enabled,
                intro_offer_discount_type=intro_offer_discount_type,
                intro_offer_discount_value=intro_offer_discount_value,
                intro_offer_duration_cycles=intro_offer_duration_cycles,
            ),
            idempotency_key=idempotency_key,
        ))

    def delete_price(
        self,
        plan_id: str,
        price_id: str,
        *,
        idempotency_key: str | None = None,
    ) -> ApiResponse[DeleteResult]:
        return parse_delete_result(self._http.delete(
            f"/plans/{plan_id}/prices/{price_id}",
            idempotency_key=idempotency_key,
        ))

    def set_default_price(
        self,
        plan_id: str,
        price_id: str,
        *,
        idempotency_key: str | None = None,
    ) -> ApiResponse[PlanPriceManage]:
        return parse_plan_price_manage(self._http.put(
            f"/plans/{plan_id}/prices/{price_id}/default",
            {},
            idempotency_key=idempotency_key,
        ))

    def set_regional_prices(
        self,
        plan_id: str,
        price_id: str,
        *,
        overrides: list[dict[str, Any]],
        idempotency_key: str | None = None,
    ) -> ApiResponse[RegionalPriceResult]:
        return parse_regional_price_result(self._http.put(
            f"/plans/{plan_id}/prices/{price_id}/regional",
            build_body(overrides=overrides),
            idempotency_key=idempotency_key,
        ))

    def delete_regional_prices(
        self,
        plan_id: str,
        price_id: str,
        *,
        idempotency_key: str | None = None,
    ) -> ApiResponse[DeleteResult]:
        return parse_delete_result(self._http.delete(
            f"/plans/{plan_id}/prices/{price_id}/regional",
            idempotency_key=idempotency_key,
        ))
