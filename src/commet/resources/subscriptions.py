from __future__ import annotations

from typing import Any

from .._http import ApiResponse, CommetHTTPClient
from .._resource_mixins import (
    build_subscription_create_body,
    parse_activate_addon_result,
    parse_active_subscription,
    parse_adjust_balance_result,
    parse_change_plan_result,
    parse_created_subscription,
    parse_deactivate_addon_result,
    parse_preview_change_result,
    parse_purchase_credits_result,
    parse_subscription,
    parse_subscription_list,
    parse_topup_balance_result,
)
from .._shared import build_body
from ..types import (
    ActivateAddonResult,
    ActiveSubscription,
    AdjustBalanceResult,
    ChangePlanResult,
    CreatedSubscription,
    DeactivateAddonResult,
    PreviewChangeResult,
    PurchaseCreditsResult,
    Subscription,
    SubscriptionListItem,
    TopupBalanceResult,
)


class SubscriptionsResource:
    def __init__(self, http: CommetHTTPClient) -> None:
        self._http = http

    def create(
        self,
        *,
        customer_id: str | None = None,
        plan_code: str | None = None,
        plan_id: str | None = None,
        billing_interval: str | None = None,
        initial_seats: dict[str, int] | None = None,
        skip_trial: bool | None = None,
        custom_intro_offer: dict[str, Any] | None = None,
        name: str | None = None,
        start_date: str | None = None,
        success_url: str | None = None,
        idempotency_key: str | None = None,
    ) -> ApiResponse[CreatedSubscription]:
        body = build_subscription_create_body(
            customer_id=customer_id, plan_code=plan_code, plan_id=plan_id,
            billing_interval=billing_interval, initial_seats=initial_seats,
            skip_trial=skip_trial, custom_intro_offer=custom_intro_offer,
            name=name, start_date=start_date, success_url=success_url,
        )
        return parse_created_subscription(
            self._http.post("/subscriptions", body, idempotency_key=idempotency_key)
        )

    def get_active(self, customer_id: str) -> ApiResponse[ActiveSubscription]:
        return parse_active_subscription(
            self._http.get("/subscriptions/active", {"customer_id": customer_id})
        )

    def list(
        self,
        *,
        customer_id: str | None = None,
        status: str | None = None,
        limit: int | None = None,
        cursor: str | None = None,
    ) -> ApiResponse[list[SubscriptionListItem]]:
        return parse_subscription_list(self._http.get("/subscriptions", build_body(
            customer_id=customer_id, status=status, limit=limit, cursor=cursor,
        )))

    def cancel(
        self,
        subscription_id: str,
        *,
        reason: str | None = None,
        immediate: bool | None = None,
        idempotency_key: str | None = None,
    ) -> ApiResponse[Subscription]:
        return parse_subscription(
            self._http.post(
                f"/subscriptions/{subscription_id}/cancel",
                build_body(reason=reason, immediate=immediate),
                idempotency_key=idempotency_key,
            )
        )

    def uncancel(
        self,
        subscription_id: str,
        *,
        idempotency_key: str | None = None,
    ) -> ApiResponse[Subscription]:
        return parse_subscription(
            self._http.post(
                f"/subscriptions/{subscription_id}/uncancel",
                {},
                idempotency_key=idempotency_key,
            )
        )

    def change_plan(
        self,
        subscription_id: str,
        *,
        new_plan_id: str | None = None,
        new_billing_interval: str | None = None,
        success_url: str | None = None,
        idempotency_key: str | None = None,
    ) -> ApiResponse[ChangePlanResult]:
        return parse_change_plan_result(
            self._http.post(
                f"/subscriptions/{subscription_id}/change-plan",
                build_body(
                    new_plan_id=new_plan_id,
                    new_billing_interval=new_billing_interval,
                    success_url=success_url,
                ),
                idempotency_key=idempotency_key,
            )
        )

    def preview_change(
        self,
        subscription_id: str,
        *,
        plan_id: str | None = None,
        billing_interval: str | None = None,
        idempotency_key: str | None = None,
    ) -> ApiResponse[PreviewChangeResult]:
        return parse_preview_change_result(self._http.post(
            f"/subscriptions/{subscription_id}/preview-change",
            build_body(plan_id=plan_id, billing_interval=billing_interval),
            idempotency_key=idempotency_key,
        ))

    def activate_addon(
        self,
        subscription_id: str,
        *,
        addon_id: str,
        idempotency_key: str | None = None,
    ) -> ApiResponse[ActivateAddonResult]:
        return parse_activate_addon_result(self._http.post(
            f"/subscriptions/{subscription_id}/addons",
            build_body(addon_id=addon_id),
            idempotency_key=idempotency_key,
        ))

    def deactivate_addon(
        self,
        subscription_id: str,
        *,
        addon_id: str,
        idempotency_key: str | None = None,
    ) -> ApiResponse[DeactivateAddonResult]:
        return parse_deactivate_addon_result(self._http.delete(
            f"/subscriptions/{subscription_id}/addons/{addon_id}",
            idempotency_key=idempotency_key,
        ))

    def adjust_balance(
        self,
        subscription_id: str,
        *,
        amount: int,
        reason: str | None = None,
        type: str | None = None,
        idempotency_key: str | None = None,
    ) -> ApiResponse[AdjustBalanceResult]:
        return parse_adjust_balance_result(self._http.post(
            f"/subscriptions/{subscription_id}/balance/adjust",
            build_body(amount=amount, reason=reason, type=type),
            idempotency_key=idempotency_key,
        ))

    def topup_balance(
        self,
        subscription_id: str,
        *,
        amount: int,
        idempotency_key: str | None = None,
    ) -> ApiResponse[TopupBalanceResult]:
        return parse_topup_balance_result(self._http.post(
            f"/subscriptions/{subscription_id}/balance/topup",
            build_body(amount=amount),
            idempotency_key=idempotency_key,
        ))

    def purchase_credits(
        self,
        subscription_id: str,
        *,
        credit_pack_id: str,
        idempotency_key: str | None = None,
    ) -> ApiResponse[PurchaseCreditsResult]:
        return parse_purchase_credits_result(self._http.post(
            f"/subscriptions/{subscription_id}/credits",
            build_body(credit_pack_id=credit_pack_id),
            idempotency_key=idempotency_key,
        ))
