from __future__ import annotations

from typing import Any

from .._http import ApiResponse, CommetHTTPClient
from .._resource_mixins import parse_seat_balance, parse_seat_event
from .._shared import build_body
from ..types import SeatBalance, SeatEvent


def _resolve_code(feature_code: str | None, seat_type: str | None) -> str:
    code = feature_code or seat_type
    if not code:
        raise ValueError("Either feature_code or seat_type must be provided")
    return code


class SeatsResource:
    def __init__(self, http: CommetHTTPClient) -> None:
        self._http = http

    def add(
        self,
        *,
        feature_code: str | None = None,
        seat_type: str | None = None,
        count: int,
        customer_id: str,
        idempotency_key: str | None = None,
    ) -> ApiResponse[SeatEvent]:
        """Add seats.

        Args:
            feature_code: The feature code identifying the seat type.
            seat_type: Deprecated. Use feature_code instead.
            count: Number of seats to add.
            customer_id: The customer ID.
            idempotency_key: Optional idempotency key.
        """
        code = _resolve_code(feature_code, seat_type)
        return parse_seat_event(self._http.post(
            "/seats",
            build_body(seat_type=code, count=count, customer_id=customer_id),
            idempotency_key=idempotency_key,
        ))

    def remove(
        self,
        *,
        feature_code: str | None = None,
        seat_type: str | None = None,
        count: int,
        customer_id: str,
        idempotency_key: str | None = None,
    ) -> ApiResponse[SeatEvent]:
        """Remove seats.

        Args:
            feature_code: The feature code identifying the seat type.
            seat_type: Deprecated. Use feature_code instead.
            count: Number of seats to remove.
            customer_id: The customer ID.
            idempotency_key: Optional idempotency key.
        """
        code = _resolve_code(feature_code, seat_type)
        return parse_seat_event(self._http.delete(
            "/seats",
            build_body(seat_type=code, count=count, customer_id=customer_id),
            idempotency_key=idempotency_key,
        ))

    def set(
        self,
        *,
        feature_code: str | None = None,
        seat_type: str | None = None,
        count: int,
        customer_id: str,
        idempotency_key: str | None = None,
    ) -> ApiResponse[SeatEvent]:
        """Set seat count.

        Args:
            feature_code: The feature code identifying the seat type.
            seat_type: Deprecated. Use feature_code instead.
            count: Absolute seat count to set.
            customer_id: The customer ID.
            idempotency_key: Optional idempotency key.
        """
        code = _resolve_code(feature_code, seat_type)
        return parse_seat_event(self._http.put(
            "/seats",
            build_body(seat_type=code, count=count, customer_id=customer_id),
            idempotency_key=idempotency_key,
        ))

    def set_all(
        self,
        *,
        seats: dict[str, int],
        customer_id: str,
        idempotency_key: str | None = None,
    ) -> ApiResponse[Any]:
        return self._http.put(
            "/seats/bulk",
            build_body(seats=seats, customer_id=customer_id),
            idempotency_key=idempotency_key,
        )

    def get_balance(
        self,
        *,
        feature_code: str | None = None,
        seat_type: str | None = None,
        customer_id: str,
    ) -> ApiResponse[SeatBalance]:
        """Get seat balance.

        Args:
            feature_code: The feature code identifying the seat type.
            seat_type: Deprecated. Use feature_code instead.
            customer_id: The customer ID.
        """
        code = _resolve_code(feature_code, seat_type)
        return parse_seat_balance(self._http.get(
            "/seats/balance",
            build_body(seat_type=code, customer_id=customer_id),
        ))

    def get_all_balances(
        self,
        *,
        customer_id: str,
    ) -> ApiResponse[dict[str, Any]]:
        return self._http.get(
            "/seats/balances",
            build_body(customer_id=customer_id),
        )
