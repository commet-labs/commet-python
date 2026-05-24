from __future__ import annotations

from .._http import ApiResponse, CommetHTTPClient
from .._resource_mixins import build_subscription_create_body, parse_subscription
from .._shared import build_body
from ..types import Subscription


class SubscriptionsResource:
    def __init__(self, http: CommetHTTPClient) -> None:
        self._http = http

    def create(
        self,
        *,
        customer_id: str | None = None,
        plan_code: str | None = None,
        plan_id: str | None = None,
        billing_interval: str | None = None,
        initial_seats: dict[str, int] | None = None,
        skip_trial: bool | None = None,
        name: str | None = None,
        start_date: str | None = None,
        success_url: str | None = None,
        idempotency_key: str | None = None,
    ) -> ApiResponse[Subscription]:
        body = build_subscription_create_body(
            customer_id=customer_id, plan_code=plan_code, plan_id=plan_id,
            billing_interval=billing_interval, initial_seats=initial_seats,
            skip_trial=skip_trial, name=name, start_date=start_date,
            success_url=success_url,
        )
        return parse_subscription(
            self._http.post("/subscriptions", body, idempotency_key=idempotency_key)
        )

    def get(self, customer_id: str) -> ApiResponse[Subscription]:
        return parse_subscription(
            self._http.get("/subscriptions/active", {"customer_id": customer_id})
        )

    def cancel(
        self,
        subscription_id: str,
        *,
        reason: str | None = None,
        immediate: bool | None = None,
        idempotency_key: str | None = None,
    ) -> ApiResponse[Subscription]:
        return parse_subscription(
            self._http.post(
                f"/subscriptions/{subscription_id}/cancel",
                build_body(reason=reason, immediate=immediate),
                idempotency_key=idempotency_key,
            )
        )

    def uncancel(
        self,
        subscription_id: str,
        *,
        idempotency_key: str | None = None,
    ) -> ApiResponse[Subscription]:
        return parse_subscription(
            self._http.post(
                f"/subscriptions/{subscription_id}/uncancel",
                {},
                idempotency_key=idempotency_key,
            )
        )
