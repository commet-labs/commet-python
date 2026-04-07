from __future__ import annotations

from .._http import ApiResponse, CommetHTTPClient, build_body


class SeatsResource:
    def __init__(self, http: CommetHTTPClient) -> None:
        self._http = http

    def add(
        self,
        *,
        seat_type: str,
        count: int,
        customer_id: str,
        idempotency_key: str | None = None,
    ) -> ApiResponse:
        return self._http.post(
            "/seats",
            build_body(
                seat_type=seat_type, count=count,
                customer_id=customer_id,
            ),
            idempotency_key=idempotency_key,
        )

    def remove(
        self,
        *,
        seat_type: str,
        count: int,
        customer_id: str,
        idempotency_key: str | None = None,
    ) -> ApiResponse:
        return self._http.delete(
            "/seats",
            build_body(
                seat_type=seat_type, count=count,
                customer_id=customer_id,
            ),
            idempotency_key=idempotency_key,
        )

    def set(
        self,
        *,
        seat_type: str,
        count: int,
        customer_id: str,
        idempotency_key: str | None = None,
    ) -> ApiResponse:
        return self._http.put(
            "/seats",
            build_body(
                seat_type=seat_type, count=count,
                customer_id=customer_id,
            ),
            idempotency_key=idempotency_key,
        )

    def set_all(
        self,
        *,
        seats: dict[str, int],
        customer_id: str,
        idempotency_key: str | None = None,
    ) -> ApiResponse:
        return self._http.put(
            "/seats/bulk",
            build_body(seats=seats, customer_id=customer_id),
            idempotency_key=idempotency_key,
        )

    def get_balance(
        self,
        *,
        seat_type: str,
        customer_id: str,
    ) -> ApiResponse:
        return self._http.get(
            "/seats/balance",
            build_body(seat_type=seat_type, customer_id=customer_id),
        )

    def get_all_balances(
        self,
        *,
        customer_id: str,
    ) -> ApiResponse:
        return self._http.get(
            "/seats/balances",
            build_body(customer_id=customer_id),
        )
