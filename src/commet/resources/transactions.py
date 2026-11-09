# ruff: noqa: E501

from __future__ import annotations

from .._http import CommetHTTPClient
from .._shared import build_body
from ..types import (
    Refund,
    Transaction,
    TransactionRetry,
    TransactionsListResult,
    TransactionStatus,
    _parse_data,
)


class TransactionsResource:
    def __init__(self, http: CommetHTTPClient) -> None:
        self._http = http

    def refund(
        self, id: str, *, amount: int | None = None, idempotency_key: str | None = None
    ) -> Refund:
        """Refund a positive amount in the payment currency’s smallest unit, or omit amount to refund the remaining amount. Returns the refund resource with its actual status."""
        body = build_body(amount=amount)
        return _parse_data(
            self._http.post(f"/transactions/{id}/refund", body, idempotency_key=idempotency_key),
            Refund,
        )

    def retry(self, id: str, *, idempotency_key: str | None = None) -> TransactionRetry:
        """Retry a failed subscription renewal and return an honest retry result. The original failed transaction remains immutable."""
        return _parse_data(
            self._http.post(f"/transactions/{id}/retry", idempotency_key=idempotency_key),
            TransactionRetry,
        )

    def get(self, id: str) -> Transaction:
        """Retrieve a single payment transaction by its public ID, including provider details."""
        return _parse_data(self._http.get(f"/transactions/{id}"), Transaction)

    def list(
        self,
        *,
        cursor: str | None = None,
        limit: int | None = None,
        status: TransactionStatus | None = None,
        customer_email: str | None = None,
    ) -> TransactionsListResult:
        """List payment transactions with cursor-based pagination. Filter by status or customer email."""
        query = build_body(cursor=cursor, limit=limit, status=status, customer_email=customer_email)
        return _parse_data(self._http.get("/transactions", query), TransactionsListResult)
