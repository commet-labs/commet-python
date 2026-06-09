from __future__ import annotations

from datetime import datetime, timezone

from .._http import ApiResponse, CommetHTTPClient
from .._preserved_types import UsageCheckResult, UsageEvent, _parse
from .._shared import build_body


def build_usage_track_body(
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
) -> dict[str, object]:
    props = [{"property": k, "value": v} for k, v in properties.items()] if properties else None

    body = build_body(
        feature=feature,
        customer_id=customer_id,
        idempotency_key=idempotency_key,
        timestamp=timestamp or datetime.now(timezone.utc).isoformat(),
        properties=props,
    )

    if model:
        body.update(
            build_body(
                model=model,
                input_tokens=input_tokens,
                output_tokens=output_tokens,
                cache_read_tokens=cache_read_tokens,
                cache_write_tokens=cache_write_tokens,
            )
        )
    elif value is not None:
        body["value"] = value

    return body


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
            feature=feature,
            customer_id=customer_id,
            value=value,
            model=model,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            cache_read_tokens=cache_read_tokens,
            cache_write_tokens=cache_write_tokens,
            idempotency_key=idempotency_key,
            timestamp=timestamp,
            properties=properties,
        )
        return _parse(
            self._http.post("/usage/events", body, idempotency_key=idempotency_key), UsageEvent
        )

    def track_model_tokens(
        self,
        *,
        feature: str,
        customer_id: str,
        model: str,
        input_tokens: int,
        output_tokens: int,
        cache_read_tokens: int | None = None,
        cache_write_tokens: int | None = None,
        idempotency_key: str | None = None,
        timestamp: str | None = None,
        properties: dict[str, str] | None = None,
    ) -> ApiResponse[UsageEvent]:
        return self.track(
            feature=feature,
            customer_id=customer_id,
            model=model,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            cache_read_tokens=cache_read_tokens,
            cache_write_tokens=cache_write_tokens,
            idempotency_key=idempotency_key,
            timestamp=timestamp,
            properties=properties,
        )

    def check(
        self,
        *,
        customer_id: str,
        feature_code: str,
        quantity: int,
    ) -> ApiResponse[UsageCheckResult]:
        body = build_body(customer_id=customer_id, feature_code=feature_code, quantity=quantity)
        return _parse(self._http.post("/usage/check", body), UsageCheckResult)
