from __future__ import annotations

from .._async_http import AsyncCommetHTTPClient
from .._http import ApiResponse
from .._resource_mixins import (
    parse_credit_pack_detail,
    parse_credit_pack_list,
    parse_delete_result,
)
from .._shared import build_body
from ..types import CreditPack, CreditPackDetail, DeleteResult


class AsyncCreditPacksResource:
    def __init__(self, http: AsyncCommetHTTPClient) -> None:
        self._http = http

    async def list(self) -> ApiResponse[list[CreditPack]]:
        return parse_credit_pack_list(await self._http.get("/credit-packs"))

    async def create(
        self,
        *,
        name: str,
        credits: int,
        price: int,
        description: str | None = None,
        is_active: bool | None = None,
        idempotency_key: str | None = None,
    ) -> ApiResponse[CreditPackDetail]:
        return parse_credit_pack_detail(await self._http.post(
            "/credit-packs/manage",
            build_body(name=name, credits=credits, price=price, description=description, is_active=is_active),
            idempotency_key=idempotency_key,
        ))

    async def update(
        self,
        credit_pack_id: str,
        *,
        name: str | None = None,
        description: str | None = None,
        credits: int | None = None,
        price: int | None = None,
        is_active: bool | None = None,
        idempotency_key: str | None = None,
    ) -> ApiResponse[CreditPackDetail]:
        return parse_credit_pack_detail(await self._http.put(
            f"/credit-packs/{credit_pack_id}",
            build_body(name=name, description=description, credits=credits, price=price, is_active=is_active),
            idempotency_key=idempotency_key,
        ))

    async def delete(
        self,
        credit_pack_id: str,
        *,
        idempotency_key: str | None = None,
    ) -> ApiResponse[DeleteResult]:
        return parse_delete_result(await self._http.delete(
            f"/credit-packs/{credit_pack_id}", idempotency_key=idempotency_key,
        ))
