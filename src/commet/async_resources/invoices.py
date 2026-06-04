from __future__ import annotations

from typing import Any, Literal

from .._async_http import AsyncCommetHTTPClient
from .._http import ApiResponse
from .._resource_mixins import (
    parse_create_adjustment_result,
    parse_invoice_detail,
    parse_invoice_download_result,
    parse_invoice_list,
    parse_invoice_send_result,
    parse_invoice_status_result,
)
from .._shared import build_body
from ..types import (
    CreateAdjustmentResult,
    InvoiceDetail,
    InvoiceDownloadResult,
    InvoiceListItem,
    InvoiceSendResult,
    InvoiceStatus,
    InvoiceStatusResult,
)


class AsyncInvoicesResource:
    def __init__(self, http: AsyncCommetHTTPClient) -> None:
        self._http = http

    async def list(
        self,
        *,
        customer_id: str | None = None,
        status: InvoiceStatus | None = None,
        subscription_id: str | None = None,
        limit: int | None = None,
        cursor: str | None = None,
    ) -> ApiResponse[list[InvoiceListItem]]:
        return parse_invoice_list(await self._http.get("/invoices", build_body(
            customer_id=customer_id, status=status, subscription_id=subscription_id,
            limit=limit, cursor=cursor,
        )))

    async def get(self, invoice_id: str) -> ApiResponse[InvoiceDetail]:
        return parse_invoice_detail(await self._http.get(f"/invoices/{invoice_id}"))

    async def create_adjustment(
        self,
        *,
        customer_id: str,
        amount: int,
        description: str | None = None,
        metadata: dict[str, Any] | None = None,
        idempotency_key: str | None = None,
    ) -> ApiResponse[CreateAdjustmentResult]:
        return parse_create_adjustment_result(await self._http.post(
            "/invoices",
            build_body(
                customer_id=customer_id, amount=amount,
                description=description, metadata=metadata,
            ),
            idempotency_key=idempotency_key,
        ))

    async def get_download_url(self, invoice_id: str) -> ApiResponse[InvoiceDownloadResult]:
        return parse_invoice_download_result(
            await self._http.get(f"/invoices/{invoice_id}/download")
        )

    async def send(
        self,
        invoice_id: str,
        *,
        idempotency_key: str | None = None,
    ) -> ApiResponse[InvoiceSendResult]:
        return parse_invoice_send_result(await self._http.post(
            f"/invoices/{invoice_id}/send", {}, idempotency_key=idempotency_key,
        ))

    async def update_status(
        self,
        invoice_id: str,
        *,
        status: Literal["paid", "void"],
        idempotency_key: str | None = None,
    ) -> ApiResponse[InvoiceStatusResult]:
        return parse_invoice_status_result(await self._http.put(
            f"/invoices/{invoice_id}/status",
            build_body(status=status),
            idempotency_key=idempotency_key,
        ))
