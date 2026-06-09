# ruff: noqa: E501

from __future__ import annotations

import builtins

from .._async_http import AsyncCommetHTTPClient
from .._http import ApiResponse
from .._shared import build_body
from ..types import (
    DiscountType,
    PromoCode,
    _parse,
    _parse_list,
)


class AsyncPromoCodesResource:
    def __init__(self, http: AsyncCommetHTTPClient) -> None:
        self._http = http

    async def list(
        self, *, limit: int | None = None, cursor: str | None = None
    ) -> ApiResponse[list[PromoCode]]:
        """List promo codes with cursor-based pagination."""
        query = build_body(limit=limit, cursor=cursor)
        return _parse_list(await self._http.get("/promo-codes", query), PromoCode)

    async def get(self, id: str) -> ApiResponse[PromoCode]:
        """Retrieve a promo code by its public ID."""
        return _parse(await self._http.get(f"/promo-codes/{id}"), PromoCode)

    async def create(
        self,
        *,
        code: str,
        discount_type: DiscountType,
        discount_value: int,
        duration_cycles: int | None = None,
        max_redemptions: int | None = None,
        expires_at: str | None = None,
        plan_ids: builtins.list[str] | None = None,
        idempotency_key: str | None = None,
    ) -> ApiResponse[PromoCode]:
        """Create a new promo code. Optionally restrict to specific plans."""
        body = build_body(
            code=code,
            discount_type=discount_type,
            discount_value=discount_value,
            duration_cycles=duration_cycles,
            max_redemptions=max_redemptions,
            expires_at=expires_at,
            plan_ids=plan_ids,
        )
        return _parse(
            await self._http.post("/promo-codes", body, idempotency_key=idempotency_key), PromoCode
        )

    async def update(
        self,
        id: str,
        *,
        max_redemptions: int | None = None,
        expires_at: str | None = None,
        active: bool | None = None,
        plan_ids: builtins.list[str] | None = None,
        idempotency_key: str | None = None,
    ) -> ApiResponse[PromoCode]:
        """Update a promo code's redemption limits, expiration, active status, or plan restrictions."""
        body = build_body(
            max_redemptions=max_redemptions, expires_at=expires_at, active=active, plan_ids=plan_ids
        )
        return _parse(
            await self._http.put(f"/promo-codes/{id}", body, idempotency_key=idempotency_key),
            PromoCode,
        )
