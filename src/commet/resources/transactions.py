# ruff: noqa: E501

from __future__ import annotations

from .._http import ApiResponse, CommetHTTPClient
from .._shared import build_body
from ..types import (
    Transaction,
    TransactionRefund,
    TransactionRetry,
    TransactionStatus,
    _parse,
    _parse_list,
)


class TransactionsResource:
    def __init__(self, http: CommetHTTPClient) -> None:
        self._http = http

    def list(
        self,
        *,
        status: TransactionStatus | None = None,
        customer_email: str | None = None,
        limit: int | None = None,
        cursor: str | None = None,
    ) -> ApiResponse[list[Transaction]]:
        """List payment transactions with cursor-based pagination. Filter by status or customer email."""
        query = build_body(status=status, customer_email=customer_email, limit=limit, cursor=cursor)
        return _parse_list(self._http.get("/transactions", query), Transaction)

    def get(self, id: str) -> ApiResponse[Transaction]:
        """Retrieve a single payment transaction by its public ID, including provider details."""
        return _parse(self._http.get(f"/transactions/{id}"), Transaction)

    def refund(
        self, id: str, *, idempotency_key: str | None = None
    ) -> ApiResponse[TransactionRefund]:
        """Issue a full refund for a payment transaction."""
        return _parse(
            self._http.post(f"/transactions/{id}/refund", idempotency_key=idempotency_key),
            TransactionRefund,
        )

    def retry(
        self, id: str, *, idempotency_key: str | None = None
    ) -> ApiResponse[TransactionRetry]:
        """Retry a failed payment transaction. Creates a new invoice and initiates a new payment attempt."""
        return _parse(
            self._http.post(f"/transactions/{id}/retry", idempotency_key=idempotency_key),
            TransactionRetry,
        )
