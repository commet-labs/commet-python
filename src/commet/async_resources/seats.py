from __future__ import annotations

from typing import Any

from .._async_http import AsyncCommetHTTPClient
from .._http import ApiResponse
from .._resource_mixins import parse_seat_balance, parse_seat_event
from .._shared import build_body
from ..types import SeatBalance, SeatEvent
from ..resources.seats import _resolve_code


class AsyncSeatsResource:
    def __init__(self, http: AsyncCommetHTTPClient) -> None:
        self._http = http

    async def add(
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
        return parse_seat_event(await self._http.post(
            "/seats",
            build_body(seat_type=code, count=count, customer_id=customer_id),
            idempotency_key=idempotency_key,
        ))

    async def remove(
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
        return parse_seat_event(await self._http.delete(
            "/seats",
            build_body(seat_type=code, count=count, customer_id=customer_id),
            idempotency_key=idempotency_key,
        ))

    async def set(
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
        return parse_seat_event(await self._http.put(
            "/seats",
            build_body(seat_type=code, count=count, customer_id=customer_id),
            idempotency_key=idempotency_key,
        ))

    async def set_all(
        self,
        *,
        seats: dict[str, int],
        customer_id: str,
        idempotency_key: str | None = None,
    ) -> ApiResponse[Any]:
        return await self._http.put(
            "/seats/bulk",
            build_body(seats=seats, customer_id=customer_id),
            idempotency_key=idempotency_key,
        )

    async def get_balance(
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
        return parse_seat_balance(await self._http.get(
            "/seats/balance",
            build_body(seat_type=code, customer_id=customer_id),
        ))

    async def get_all_balances(
        self,
        *,
        customer_id: str,
    ) -> ApiResponse[dict[str, Any]]:
        return await self._http.get(
            "/seats/balances",
            build_body(customer_id=customer_id),
        )
