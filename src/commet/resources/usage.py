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
        customer_id: str | None = None,
        external_id: str | None = None,
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
            external_id=external_id,
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

    def track_batch(
        self,
        events: list[dict[str, Any]],
        *,
        idempotency_key: str | None = None,
    ) -> ApiResponse:
        mapped = []
        for evt in events:
            props = evt.get("properties")
            formatted_props = (
                [{"property": k, "value": v} for k, v in props.items()] if props else None
            )

            entry = build_body(
                feature=evt.get("feature"),
                customer_id=evt.get("customer_id"),
                external_id=evt.get("external_id"),
                idempotency_key=evt.get("idempotency_key"),
                timestamp=evt.get("timestamp") or datetime.now(timezone.utc).isoformat(),
                properties=formatted_props,
            )

            if evt.get("model"):
                entry.update(build_body(
                    model=evt["model"],
                    input_tokens=evt.get("input_tokens"),
                    output_tokens=evt.get("output_tokens"),
                    cache_read_tokens=evt.get("cache_read_tokens"),
                    cache_write_tokens=evt.get("cache_write_tokens"),
                ))
            elif evt.get("value") is not None:
                entry["value"] = evt["value"]

            mapped.append(entry)

        return self._http.post(
            "/usage/events/batch", {"events": mapped}, idempotency_key=idempotency_key
        )
