from __future__ import annotations

from typing import Any

from .._http import ApiResponse, CommetHTTPClient
from .._resource_mixins import build_usage_track_body, parse_usage_event
from ..types import UsageEvent


class UsageResource:
    def __init__(self, http: CommetHTTPClient) -> None:
        self._http = http

    def track(
        self,
        *,
        feature: str,
        customer_id: str,
        value: int | None = None,
        model: str | None = None,
        input_tokens: int | None = None,
        output_tokens: int | None = None,
        cache_read_tokens: int | None = None,
        cache_write_tokens: int | None = None,
        idempotency_key: str | None = None,
        timestamp: str | None = None,
        properties: dict[str, str] | None = None,
    ) -> ApiResponse[UsageEvent]:
        body = build_usage_track_body(
            feature=feature, customer_id=customer_id, value=value, model=model,
            input_tokens=input_tokens, output_tokens=output_tokens,
            cache_read_tokens=cache_read_tokens, cache_write_tokens=cache_write_tokens,
            idempotency_key=idempotency_key, timestamp=timestamp, properties=properties,
        )
        return parse_usage_event(self._http.post("/usage/events", body, idempotency_key=idempotency_key))

    def check(
        self,
        *,
        customer_id: str,
        feature_code: str,
        quantity: int,
    ) -> ApiResponse[dict[str, Any]]:
        return self._http.post(
            "/usage/check",
            {"customer_id": customer_id, "feature_code": feature_code, "quantity": quantity},
        )
