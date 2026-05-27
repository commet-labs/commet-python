from __future__ import annotations

from typing import Any

from .._http import ApiResponse, CommetHTTPClient
from .._shared import build_body


class InvoicesResource:
    def __init__(self, http: CommetHTTPClient) -> None:
        self._http = http

    def list(
        self,
        *,
        customer_id: str | None = None,
        status: str | None = None,
        subscription_id: str | None = None,
        limit: int | None = None,
        cursor: str | None = None,
    ) -> ApiResponse[Any]:
        return self._http.get("/invoices", build_body(
            customer_id=customer_id, status=status, subscription_id=subscription_id,
            limit=limit, cursor=cursor,
        ))

    def get(self, invoice_id: str) -> ApiResponse[Any]:
        return self._http.get(f"/invoices/{invoice_id}")

    def create_adjustment(
        self,
        *,
        customer_id: str,
        amount: int,
        description: str | None = None,
        metadata: dict[str, Any] | None = None,
        idempotency_key: str | None = None,
    ) -> ApiResponse[Any]:
        return self._http.post(
            "/invoices",
            build_body(
                customer_id=customer_id, amount=amount,
                description=description, metadata=metadata,
            ),
            idempotency_key=idempotency_key,
        )

    def get_download_url(self, invoice_id: str) -> ApiResponse[Any]:
        return self._http.get(f"/invoices/{invoice_id}/download")

    def send(
        self,
        invoice_id: str,
        *,
        idempotency_key: str | None = None,
    ) -> ApiResponse[Any]:
        return self._http.post(
            f"/invoices/{invoice_id}/send", {}, idempotency_key=idempotency_key,
        )

    def update_status(
        self,
        invoice_id: str,
        *,
        status: str,
        idempotency_key: str | None = None,
    ) -> ApiResponse[Any]:
        return self._http.put(
            f"/invoices/{invoice_id}/status",
            build_body(status=status),
            idempotency_key=idempotency_key,
        )
