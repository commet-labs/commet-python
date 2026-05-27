from __future__ import annotations

from typing import Any

from .._async_http import AsyncCommetHTTPClient
from .._http import ApiResponse
from .._shared import build_body


class AsyncInvoicesResource:
    def __init__(self, http: AsyncCommetHTTPClient) -> None:
        self._http = http

    async def list(
        self,
        *,
        customer_id: str | None = None,
        status: str | None = None,
        subscription_id: str | None = None,
        limit: int | None = None,
        cursor: str | None = None,
    ) -> ApiResponse[Any]:
        return await self._http.get("/invoices", build_body(
            customer_id=customer_id, status=status, subscription_id=subscription_id,
            limit=limit, cursor=cursor,
        ))

    async def get(self, invoice_id: str) -> ApiResponse[Any]:
        return await self._http.get(f"/invoices/{invoice_id}")

    async def create_adjustment(
        self,
        *,
        customer_id: str,
        amount: int,
        description: str | None = None,
        metadata: dict[str, Any] | None = None,
        idempotency_key: str | None = None,
    ) -> ApiResponse[Any]:
        return await self._http.post(
            "/invoices",
            build_body(
                customer_id=customer_id, amount=amount,
                description=description, metadata=metadata,
            ),
            idempotency_key=idempotency_key,
        )

    async def get_download_url(self, invoice_id: str) -> ApiResponse[Any]:
        return await self._http.get(f"/invoices/{invoice_id}/download")

    async def send(
        self,
        invoice_id: str,
        *,
        idempotency_key: str | None = None,
    ) -> ApiResponse[Any]:
        return await self._http.post(
            f"/invoices/{invoice_id}/send", {}, idempotency_key=idempotency_key,
        )

    async def update_status(
        self,
        invoice_id: str,
        *,
        status: str,
        idempotency_key: str | None = None,
    ) -> ApiResponse[Any]:
        return await self._http.put(
            f"/invoices/{invoice_id}/status",
            build_body(status=status),
            idempotency_key=idempotency_key,
        )
