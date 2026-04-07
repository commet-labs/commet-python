from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from .._http import ApiResponse, CommetHTTPClient, build_body


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
    ) -> ApiResponse:
        props = (
            [{"property": k, "value": v} for k, v in properties.items()] if properties else None
        )

        body = build_body(
            feature=feature,
            customer_id=customer_id,
            idempotency_key=idempotency_key,
            timestamp=timestamp or datetime.now(timezone.utc).isoformat(),
            properties=props,
        )

        if model:
            body.update(build_body(
                model=model,
                input_tokens=input_tokens,
                output_tokens=output_tokens,
                cache_read_tokens=cache_read_tokens,
                cache_write_tokens=cache_write_tokens,
            ))
        else:
            if value is not None:
                body["value"] = value

        return self._http.post("/usage/events", body, idempotency_key=idempotency_key)

