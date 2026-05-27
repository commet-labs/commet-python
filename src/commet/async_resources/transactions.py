from __future__ import annotations

from typing import Any

from .._async_http import AsyncCommetHTTPClient
from .._http import ApiResponse
from .._shared import build_body


class AsyncTransactionsResource:
    def __init__(self, http: AsyncCommetHTTPClient) -> None:
        self._http = http

    async def list(
        self,
        *,
        status: str | None = None,
        customer_email: str | None = None,
        limit: int | None = None,
        cursor: str | None = None,
    ) -> ApiResponse[Any]:
        return await self._http.get("/transactions", build_body(
            status=status, customer_email=customer_email,
            limit=limit, cursor=cursor,
        ))

    async def get(self, transaction_id: str) -> ApiResponse[Any]:
        return await self._http.get(f"/transactions/{transaction_id}")

    async def refund(
        self,
        transaction_id: str,
        *,
        idempotency_key: str | None = None,
    ) -> ApiResponse[Any]:
        return await self._http.post(
            f"/transactions/{transaction_id}/refund", {}, idempotency_key=idempotency_key,
        )

    async def retry(
        self,
        transaction_id: str,
        *,
        idempotency_key: str | None = None,
    ) -> ApiResponse[Any]:
        return await self._http.post(
            f"/transactions/{transaction_id}/retry", {}, idempotency_key=idempotency_key,
        )
