# ruff: noqa: E501

from __future__ import annotations

from .._http import CommetHTTPClient
from .._shared import build_body
from ..types import (
    SeatBalance,
    SeatBalanceCollection,
    SeatEvent,
    SeatsSetAllResult,
    _parse_data,
)


class SeatsResource:
    def __init__(self, http: CommetHTTPClient) -> None:
        self._http = http

    def get_balance(self, *, customer_id: str, feature_code: str) -> SeatBalance:
        """Get current balance for a specific seat type."""
        query = build_body(customer_id=customer_id, feature_code=feature_code)
        return _parse_data(self._http.get("/seats/balance", query), SeatBalance)

    def get_all_balances(self, *, customer_id: str) -> SeatBalanceCollection:
        """Get the current balance for all seat types in a customer's subscription."""
        query = build_body(customer_id=customer_id)
        return _parse_data(self._http.get("/seats/balances", query), SeatBalanceCollection)

    def set_all(
        self, *, customer_id: str, seats: dict[str, int], idempotency_key: str | None = None
    ) -> SeatsSetAllResult:
        """Set all seat types at once."""
        body = build_body(customer_id=customer_id, seats=seats)
        return _parse_data(
            self._http.put("/seats/bulk", body, idempotency_key=idempotency_key), SeatsSetAllResult
        )

    def remove(
        self, *, customer_id: str, feature_code: str, count: int, idempotency_key: str | None = None
    ) -> SeatEvent:
        """Remove seats from a customer's subscription. Takes effect at the end of the billing period."""
        body = build_body(customer_id=customer_id, feature_code=feature_code, count=count)
        return _parse_data(
            self._http.post("/seats/remove", body, idempotency_key=idempotency_key), SeatEvent
        )

    def add(
        self, *, customer_id: str, feature_code: str, count: int, idempotency_key: str | None = None
    ) -> SeatEvent:
        """Add seats to a customer's subscription. Prorates charges for the current billing period."""
        body = build_body(customer_id=customer_id, feature_code=feature_code, count=count)
        return _parse_data(
            self._http.post("/seats", body, idempotency_key=idempotency_key), SeatEvent
        )

    def set(
        self, *, customer_id: str, feature_code: str, count: int, idempotency_key: str | None = None
    ) -> SeatEvent:
        """Set seats to an exact count."""
        body = build_body(customer_id=customer_id, feature_code=feature_code, count=count)
        return _parse_data(
            self._http.put("/seats", body, idempotency_key=idempotency_key), SeatEvent
        )
