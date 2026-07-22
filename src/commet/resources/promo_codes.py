# ruff: noqa: E501

from __future__ import annotations

import builtins

from .._http import ApiResponse, CommetHTTPClient
from .._shared import build_body
from ..types import (
    BillingInterval,
    DiscountType,
    PromoCode,
    _parse,
    _parse_list,
)


class PromoCodesResource:
    def __init__(self, http: CommetHTTPClient) -> None:
        self._http = http

    def list(
        self, *, limit: int | None = None, cursor: str | None = None
    ) -> ApiResponse[list[PromoCode]]:
        """List promo codes with cursor-based pagination."""
        query = build_body(limit=limit, cursor=cursor)
        return _parse_list(self._http.get("/promo-codes", query), PromoCode)

    def get(self, id: str) -> ApiResponse[PromoCode]:
        """Retrieve a promo code by its public ID."""
        return _parse(self._http.get(f"/promo-codes/{id}"), PromoCode)

    def create(
        self,
        *,
        code: str,
        discount_type: DiscountType,
        discount_value: int,
        duration_cycles: int | None = None,
        billing_interval: BillingInterval | None = None,
        max_redemptions: int | None = None,
        expires_at: str | None = None,
        plan_ids: builtins.list[str] | None = None,
        idempotency_key: str | None = None,
    ) -> ApiResponse[PromoCode]:
        """
        Create a new promo code. Optionally restrict it to specific plans and a billing interval.

        **100% discounts are not supported.** Percentage codes must be strictly less than 100% (`discountValue` < 10000 basis points). For full waivers, use an introductory offer on the plan instead. At checkout, any code — percentage or fixed amount — that would reduce the total below the currency's minimum charge ($0.50 USD equivalent) is silently dropped.
        """
        body = build_body(
            code=code,
            discount_type=discount_type,
            discount_value=discount_value,
            duration_cycles=duration_cycles,
            billing_interval=billing_interval,
            max_redemptions=max_redemptions,
            expires_at=expires_at,
            plan_ids=plan_ids,
        )
        return _parse(
            self._http.post("/promo-codes", body, idempotency_key=idempotency_key), PromoCode
        )

    def update(
        self,
        id: str,
        *,
        billing_interval: BillingInterval | None = None,
        max_redemptions: int | None = None,
        expires_at: str | None = None,
        active: bool | None = None,
        plan_ids: builtins.list[str] | None = None,
        idempotency_key: str | None = None,
    ) -> ApiResponse[PromoCode]:
        """Update a promo code's billing interval, redemption limits, expiration, active status, or plan restrictions."""
        body = build_body(
            billing_interval=billing_interval,
            max_redemptions=max_redemptions,
            expires_at=expires_at,
            active=active,
            plan_ids=plan_ids,
        )
        return _parse(
            self._http.put(f"/promo-codes/{id}", body, idempotency_key=idempotency_key), PromoCode
        )
