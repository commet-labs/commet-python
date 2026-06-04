from __future__ import annotations

from .._async_http import AsyncCommetHTTPClient
from .._http import ApiResponse
from .._resource_mixins import (
    parse_seat_balance,
    parse_seat_balance_map,
    parse_seat_event,
    parse_seat_event_list,
)
from .._shared import build_body
from ..types import SeatBalance, SeatEvent


class AsyncSeatsResource:
    def __init__(self, http: AsyncCommetHTTPClient) -> None:
        self._http = http

    async def add(
        self,
        *,
        feature_code: str,
        count: int = 1,
        customer_id: str,
        idempotency_key: str | None = None,
    ) -> ApiResponse[SeatEvent]:
        return parse_seat_event(await self._http.post(
            "/seats",
            build_body(feature_code=feature_code, count=count, customer_id=customer_id),
            idempotency_key=idempotency_key,
        ))

    async def remove(
        self,
        *,
        feature_code: str,
        count: int = 1,
        customer_id: str,
        idempotency_key: str | None = None,
    ) -> ApiResponse[SeatEvent]:
        return parse_seat_event(await self._http.delete(
            "/seats",
            build_body(feature_code=feature_code, count=count, customer_id=customer_id),
            idempotency_key=idempotency_key,
        ))

    async def set(
        self,
        *,
        feature_code: str,
        count: int,
        customer_id: str,
        idempotency_key: str | None = None,
    ) -> ApiResponse[SeatEvent]:
        return parse_seat_event(await self._http.put(
            "/seats",
            build_body(feature_code=feature_code, count=count, customer_id=customer_id),
            idempotency_key=idempotency_key,
        ))

    async def set_all(
        self,
        *,
        seats: dict[str, int],
        customer_id: str,
        idempotency_key: str | None = None,
    ) -> ApiResponse[list[SeatEvent]]:
        return parse_seat_event_list(await self._http.put(
            "/seats/bulk",
            build_body(seats=seats, customer_id=customer_id),
            idempotency_key=idempotency_key,
        ))

    async def get_balance(
        self,
        *,
        feature_code: str,
        customer_id: str,
    ) -> ApiResponse[SeatBalance]:
        return parse_seat_balance(await self._http.get(
            "/seats/balance",
            build_body(feature_code=feature_code, customer_id=customer_id),
        ))

    async def get_all_balances(
        self,
        *,
        customer_id: str,
    ) -> ApiResponse[dict[str, SeatBalance]]:
        return parse_seat_balance_map(await self._http.get(
            "/seats/balances",
            build_body(customer_id=customer_id),
        ))
