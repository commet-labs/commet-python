from __future__ import annotations

from typing import Any

from .._http import ApiResponse, CommetHTTPClient
from .._shared import build_body


class PromoCodesResource:
    def __init__(self, http: CommetHTTPClient) -> None:
        self._http = http

    def list(
        self,
        *,
        limit: int | None = None,
        cursor: str | None = None,
    ) -> ApiResponse[Any]:
        return self._http.get("/promo-codes", build_body(limit=limit, cursor=cursor))

    def get(self, promo_code_id: str) -> ApiResponse[Any]:
        return self._http.get(f"/promo-codes/{promo_code_id}")

    def create(
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
    ) -> ApiResponse[Any]:
        return self._http.post(
            "/promo-codes",
            build_body(
                code=code, discount_type=discount_type, discount_value=discount_value,
                duration_cycles=duration_cycles, max_redemptions=max_redemptions,
                expires_at=expires_at, plan_ids=plan_ids,
            ),
            idempotency_key=idempotency_key,
        )

    def update(
        self,
        promo_code_id: str,
        *,
        max_redemptions: int | None = None,
        expires_at: str | None = None,
        active: bool | None = None,
        plan_ids: list[str] | None = None,
        idempotency_key: str | None = None,
    ) -> ApiResponse[Any]:
        return self._http.put(
            f"/promo-codes/{promo_code_id}",
            build_body(
                max_redemptions=max_redemptions, expires_at=expires_at,
                active=active, plan_ids=plan_ids,
            ),
            idempotency_key=idempotency_key,
        )
