# ruff: noqa: E501

from __future__ import annotations

import builtins
from typing import Literal

from .._async_http import AsyncCommetHTTPClient
from .._shared import build_body
from ..types import (
    PromoCode,
    PromoCodesListResult,
    _parse_data,
)


class AsyncPromoCodesResource:
    def __init__(self, http: AsyncCommetHTTPClient) -> None:
        self._http = http

    async def get(self, id: str) -> PromoCode:
        """Retrieve a promo code by its public ID."""
        return _parse_data(await self._http.get(f"/promo-codes/{id}"), PromoCode)

    async def update(
        self,
        id: str,
        *,
        billing_interval: Literal["weekly", "monthly", "quarterly", "yearly", "one_time"]
        | None = None,
        max_redemptions: int | None = None,
        expires_at: str | None = None,
        active: bool | None = None,
        plan_ids: builtins.list[str] | None = None,
        idempotency_key: str | None = None,
    ) -> PromoCode:
        """Update a promo code's billing interval, redemption limits, expiration, active status, or plan restrictions."""
        body = build_body(
            billing_interval=billing_interval,
            max_redemptions=max_redemptions,
            expires_at=expires_at,
            active=active,
            plan_ids=plan_ids,
        )
        return _parse_data(
            await self._http.patch(f"/promo-codes/{id}", body, idempotency_key=idempotency_key),
            PromoCode,
        )

    async def list(
        self, *, cursor: str | None = None, limit: int | None = None
    ) -> PromoCodesListResult:
        """List promo codes with cursor-based pagination."""
        query = build_body(cursor=cursor, limit=limit)
        return _parse_data(await self._http.get("/promo-codes", query), PromoCodesListResult)

    async def create(
        self,
        *,
        code: str,
        offer_id: str,
        billing_interval: Literal["weekly", "monthly", "quarterly", "yearly", "one_time"]
        | None = None,
        max_redemptions: int | None = None,
        expires_at: str | None = None,
        plan_ids: builtins.list[str] | None = None,
        idempotency_key: str | None = None,
    ) -> PromoCode:
        """Create a distribution code for an existing promotional offer. Offer economics remain owned by the referenced Offer."""
        body = build_body(
            code=code,
            offer_id=offer_id,
            billing_interval=billing_interval,
            max_redemptions=max_redemptions,
            expires_at=expires_at,
            plan_ids=plan_ids,
        )
        return _parse_data(
            await self._http.post("/promo-codes", body, idempotency_key=idempotency_key), PromoCode
        )
