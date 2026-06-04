from __future__ import annotations

from .._async_http import AsyncCommetHTTPClient
from .._http import ApiResponse
from .._resource_mixins import (
    parse_promo_code,
    parse_promo_code_detail,
    parse_promo_code_list,
)
from .._shared import build_body
from ..types import PromoCode, PromoCodeDetail


class AsyncPromoCodesResource:
    def __init__(self, http: AsyncCommetHTTPClient) -> None:
        self._http = http

    async def list(
        self,
        *,
        limit: int | None = None,
        cursor: str | None = None,
    ) -> ApiResponse[list[PromoCode]]:
        return parse_promo_code_list(
            await self._http.get("/promo-codes", build_body(limit=limit, cursor=cursor))
        )

    async def get(self, promo_code_id: str) -> ApiResponse[PromoCodeDetail]:
        return parse_promo_code_detail(await self._http.get(f"/promo-codes/{promo_code_id}"))

    async def create(
        self,
        *,
        code: str,
        discount_type: str,
        discount_value: int,
        duration_cycles: int | None = None,
        max_redemptions: int | None = None,
        expires_at: str | None = None,
        plan_ids: list[str] | None = None,
        idempotency_key: str | None = None,
    ) -> ApiResponse[PromoCode]:
        return parse_promo_code(await self._http.post(
            "/promo-codes",
            build_body(
                code=code, discount_type=discount_type, discount_value=discount_value,
                duration_cycles=duration_cycles, max_redemptions=max_redemptions,
                expires_at=expires_at, plan_ids=plan_ids,
            ),
            idempotency_key=idempotency_key,
        ))

    async def update(
        self,
        promo_code_id: str,
        *,
        max_redemptions: int | None = None,
        expires_at: str | None = None,
        active: bool | None = None,
        plan_ids: list[str] | None = None,
        idempotency_key: str | None = None,
    ) -> ApiResponse[PromoCodeDetail]:
        return parse_promo_code_detail(await self._http.put(
            f"/promo-codes/{promo_code_id}",
            build_body(
                max_redemptions=max_redemptions, expires_at=expires_at,
                active=active, plan_ids=plan_ids,
            ),
            idempotency_key=idempotency_key,
        ))
