# ruff: noqa: E501

from __future__ import annotations

import builtins

from .._http import CommetHTTPClient
from .._shared import build_body
from ..types import (
    TrackUsageParamsPropertiesItem,
    UsageAdjustment,
    UsageCheck,
    UsageEvent,
    _parse_data,
    _parse_union_data,
)


class UsageResource:
    def __init__(self, http: CommetHTTPClient) -> None:
        self._http = http

    def check(
        self,
        *,
        customer_id: str,
        feature_code: str,
        quantity: int | None = None,
        idempotency_key: str | None = None,
    ) -> UsageCheck:
        """Check if a customer can consume a feature before actual consumption. Returns availability and cost estimates based on the plan's consumption model."""
        body = build_body(customer_id=customer_id, feature_code=feature_code, quantity=quantity)
        return _parse_union_data(
            self._http.post("/usage/check", body, idempotency_key=idempotency_key), "UsageCheck"
        )

    def track(
        self,
        *,
        feature_code: str,
        customer_id: str,
        event_id: str | None = None,
        timestamp: str | None = None,
        properties: builtins.list[TrackUsageParamsPropertiesItem] | None = None,
        model: str | None = None,
        input_tokens: int | None = None,
        output_tokens: int | None = None,
        value: float | None = None,
        cache_read_tokens: int | None = None,
        cache_write_tokens: int | None = None,
        idempotency_key: str | None = None,
    ) -> UsageEvent:
        """Track a usage event for a metered feature. Deducts from balance/credits if applicable."""
        body = build_body(
            feature_code=feature_code,
            customer_id=customer_id,
            event_id=event_id,
            timestamp=timestamp,
            properties=properties,
            model=model,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            value=value,
            cache_read_tokens=cache_read_tokens,
            cache_write_tokens=cache_write_tokens,
        )
        return _parse_data(
            self._http.post("/usage/events", body, idempotency_key=idempotency_key), UsageEvent
        )

    def set(
        self,
        *,
        customer_id: str,
        feature_code: str,
        value: int,
        reason: str | None = None,
        idempotency_key: str | None = None,
    ) -> UsageAdjustment:
        """Set a metered feature's usage to an exact value for the current period. Use the Idempotency-Key header to make retries safe."""
        body = build_body(
            customer_id=customer_id, feature_code=feature_code, value=value, reason=reason
        )
        return _parse_data(
            self._http.put("/usage", body, idempotency_key=idempotency_key), UsageAdjustment
        )
