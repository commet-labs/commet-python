from __future__ import annotations

from .._http import ApiResponse, CommetHTTPClient
from .._resource_mixins import (
    parse_seat_balance,
    parse_seat_balance_map,
    parse_seat_event,
    parse_seat_event_list,
)
from .._shared import build_body
from ..types import SeatBalance, SeatEvent


class SeatsResource:
    def __init__(self, http: CommetHTTPClient) -> None:
        self._http = http

    def add(
        self,
        *,
        feature_code: str,
        count: int = 1,
        customer_id: str,
        idempotency_key: str | None = None,
    ) -> ApiResponse[SeatEvent]:
        return parse_seat_event(self._http.post(
            "/seats",
            build_body(feature_code=feature_code, count=count, customer_id=customer_id),
            idempotency_key=idempotency_key,
        ))

    def remove(
        self,
        *,
        feature_code: str,
        count: int = 1,
        customer_id: str,
        idempotency_key: str | None = None,
    ) -> ApiResponse[SeatEvent]:
        return parse_seat_event(self._http.delete(
            "/seats",
            build_body(feature_code=feature_code, count=count, customer_id=customer_id),
            idempotency_key=idempotency_key,
        ))

    def set(
        self,
        *,
        feature_code: str,
        count: int,
        customer_id: str,
        idempotency_key: str | None = None,
    ) -> ApiResponse[SeatEvent]:
        return parse_seat_event(self._http.put(
            "/seats",
            build_body(feature_code=feature_code, count=count, customer_id=customer_id),
            idempotency_key=idempotency_key,
        ))

    def set_all(
        self,
        *,
        seats: dict[str, int],
        customer_id: str,
        idempotency_key: str | None = None,
    ) -> ApiResponse[list[SeatEvent]]:
        return parse_seat_event_list(self._http.put(
            "/seats/bulk",
            build_body(seats=seats, customer_id=customer_id),
            idempotency_key=idempotency_key,
        ))

    def get_balance(
        self,
        *,
        feature_code: str,
        customer_id: str,
    ) -> ApiResponse[SeatBalance]:
        return parse_seat_balance(self._http.get(
            "/seats/balance",
            build_body(feature_code=feature_code, customer_id=customer_id),
        ))

    def get_all_balances(
        self,
        *,
        customer_id: str,
    ) -> ApiResponse[dict[str, SeatBalance]]:
        return parse_seat_balance_map(self._http.get(
            "/seats/balances",
            build_body(customer_id=customer_id),
        ))
