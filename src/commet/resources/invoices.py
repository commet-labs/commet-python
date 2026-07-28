# ruff: noqa: E501

from __future__ import annotations

from typing import Any, Literal

from .._http import CommetHTTPClient
from .._shared import build_body
from ..types import (
    Invoice,
    InvoiceDownload,
    InvoicesListResult,
    SentInvoice,
    _parse_data,
)


class InvoicesResource:
    def __init__(self, http: CommetHTTPClient) -> None:
        self._http = http

    def get_download_url(self, id: str, *, idempotency_key: str | None = None) -> InvoiceDownload:
        """Generate a signed URL to download the invoice as a PDF. The URL expires after 7 days."""
        return _parse_data(
            self._http.post(f"/invoices/{id}/download-links", idempotency_key=idempotency_key),
            InvoiceDownload,
        )

    def get(self, id: str) -> Invoice:
        """Retrieve a single invoice by its public ID, including line items."""
        return _parse_data(self._http.get(f"/invoices/{id}"), Invoice)

    def send(self, id: str, *, idempotency_key: str | None = None) -> SentInvoice:
        """Send the invoice to the customer via email."""
        return _parse_data(
            self._http.post(f"/invoices/{id}/send", idempotency_key=idempotency_key), SentInvoice
        )

    def update_status(
        self, id: str, *, status: Literal["paid", "void"], idempotency_key: str | None = None
    ) -> Invoice:
        """Mark an outstanding invoice as "paid" or "void" and return the updated invoice. Cannot change the status of already paid or voided invoices."""
        body = build_body(status=status)
        return _parse_data(
            self._http.patch(f"/invoices/{id}/status", body, idempotency_key=idempotency_key),
            Invoice,
        )

    def list(
        self,
        *,
        cursor: str | None = None,
        limit: int | None = None,
        customer_id: str | None = None,
        status: Literal["draft", "outstanding", "paid", "void", "uncollectible"] | None = None,
        subscription_id: str | None = None,
    ) -> InvoicesListResult:
        """List invoices with cursor-based pagination. Filter by customer, status, or subscription."""
        query = build_body(
            cursor=cursor,
            limit=limit,
            customer_id=customer_id,
            status=status,
            subscription_id=subscription_id,
        )
        return _parse_data(self._http.get("/invoices", query), InvoicesListResult)

    def create_adjustment(
        self,
        *,
        customer_id: str,
        amount: int,
        description: str,
        metadata: dict[str, Any] | None = None,
        idempotency_key: str | None = None,
    ) -> Invoice:
        """Create a one-off adjustment invoice and return the created invoice. Use a negative amount for a credit."""
        body = build_body(
            customer_id=customer_id, amount=amount, description=description, metadata=metadata
        )
        return _parse_data(
            self._http.post("/invoices", body, idempotency_key=idempotency_key), Invoice
        )
