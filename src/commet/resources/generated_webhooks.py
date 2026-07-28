# ruff: noqa: E501

from __future__ import annotations

import builtins
from typing import Literal

from .._http import CommetHTTPClient
from .._shared import build_body
from ..types import (
    CreatedWebhook,
    DeletedObject,
    Webhook,
    WebhooksListResult,
    WebhookTest,
    _parse_data,
)


class GeneratedWebhooksResource:
    def __init__(self, http: CommetHTTPClient) -> None:
        self._http = http

    def get(self, id: str) -> Webhook:
        """Retrieve a webhook endpoint by its public ID."""
        return _parse_data(self._http.get(f"/webhooks/{id}"), Webhook)

    def update(
        self,
        id: str,
        *,
        url: str | None = None,
        events: builtins.list[
            Literal[
                "subscription.created",
                "subscription.activated",
                "subscription.reactivated",
                "subscription.canceled",
                "subscription.updated",
                "subscription.plan_changed",
                "subscription.cancellation_scheduled",
                "subscription.cancellation_revoked",
                "subscription.plan_change_scheduled",
                "subscription.plan_change_revoked",
                "subscription.past_due",
                "trial.started",
                "trial.converted",
                "trial.expired",
                "trial.will_end",
                "trial.checkout_ready",
                "checkout.ready",
                "payment.received",
                "payment.failed",
                "payment.recovered",
                "payment.retry_failed",
                "payment.refunded",
                "payment.disputed",
                "payment.dispute_resolved",
                "payment_link.created",
                "payment_link.completed",
                "payment_link.failed",
                "payment_link.canceled",
                "invoice.created",
                "invoice.voided",
                "invoice.overdue",
                "invoice.upcoming",
                "payment_method.attached",
                "payment_method.updated",
                "customer.created",
                "customer.updated",
                "customer.state_changed",
                "credits.granted",
                "credits.purchased",
                "credits.low",
                "credits.depleted",
                "credits.expired",
                "balance.topped_up",
                "balance.low",
                "balance.depleted",
                "quota.threshold_reached",
                "quota.exceeded",
                "seats.updated",
                "seats.limit_reached",
                "addon.activated",
                "addon.deactivated",
                "usage.recorded",
                "payout.available",
                "payout.created",
                "payout.paid",
                "payout.failed",
            ]
        ]
        | None = None,
        description: str | None = None,
        is_active: bool | None = None,
        api_version: str | None = None,
        idempotency_key: str | None = None,
    ) -> Webhook:
        """Update a webhook endpoint. Only the provided fields change."""
        body = build_body(
            url=url,
            events=events,
            description=description,
            is_active=is_active,
            api_version=api_version,
        )
        return _parse_data(
            self._http.patch(f"/webhooks/{id}", body, idempotency_key=idempotency_key), Webhook
        )

    def delete(self, id: str) -> DeletedObject:
        """Permanently delete a webhook endpoint."""
        return _parse_data(self._http.delete(f"/webhooks/{id}"), DeletedObject)

    def test(self, id: str, *, idempotency_key: str | None = None) -> WebhookTest:
        """Send a test event to a webhook endpoint to verify connectivity."""
        return _parse_data(
            self._http.post(f"/webhooks/{id}/test", idempotency_key=idempotency_key), WebhookTest
        )

    def list(self, *, cursor: str | None = None, limit: int | None = None) -> WebhooksListResult:
        """List webhook endpoints with cursor-based pagination."""
        query = build_body(cursor=cursor, limit=limit)
        return _parse_data(self._http.get("/webhooks", query), WebhooksListResult)

    def create(
        self,
        *,
        url: str,
        events: builtins.list[
            Literal[
                "subscription.created",
                "subscription.activated",
                "subscription.reactivated",
                "subscription.canceled",
                "subscription.updated",
                "subscription.plan_changed",
                "subscription.cancellation_scheduled",
                "subscription.cancellation_revoked",
                "subscription.plan_change_scheduled",
                "subscription.plan_change_revoked",
                "subscription.past_due",
                "trial.started",
                "trial.converted",
                "trial.expired",
                "trial.will_end",
                "trial.checkout_ready",
                "checkout.ready",
                "payment.received",
                "payment.failed",
                "payment.recovered",
                "payment.retry_failed",
                "payment.refunded",
                "payment.disputed",
                "payment.dispute_resolved",
                "payment_link.created",
                "payment_link.completed",
                "payment_link.failed",
                "payment_link.canceled",
                "invoice.created",
                "invoice.voided",
                "invoice.overdue",
                "invoice.upcoming",
                "payment_method.attached",
                "payment_method.updated",
                "customer.created",
                "customer.updated",
                "customer.state_changed",
                "credits.granted",
                "credits.purchased",
                "credits.low",
                "credits.depleted",
                "credits.expired",
                "balance.topped_up",
                "balance.low",
                "balance.depleted",
                "quota.threshold_reached",
                "quota.exceeded",
                "seats.updated",
                "seats.limit_reached",
                "addon.activated",
                "addon.deactivated",
                "usage.recorded",
                "payout.available",
                "payout.created",
                "payout.paid",
                "payout.failed",
            ]
        ],
        description: str | None = None,
        api_version: str | None = None,
        idempotency_key: str | None = None,
    ) -> CreatedWebhook:
        """Create a new webhook endpoint. The response includes the signing secret which is only returned once."""
        body = build_body(url=url, events=events, description=description, api_version=api_version)
        return _parse_data(
            self._http.post("/webhooks", body, idempotency_key=idempotency_key), CreatedWebhook
        )
