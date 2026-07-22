from __future__ import annotations

from .._async_http import AsyncCommetHTTPClient
from .._http import ApiResponse
from .._preserved_types import UsageAdjustment, UsageCheckResult, UsageEvent, _parse
from .._shared import build_body
from ..resources.usage import build_usage_track_body


class AsyncUsageResource:
    def __init__(self, http: AsyncCommetHTTPClient) -> None:
        self._http = http

    async def track(
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
            await self._http.post("/usage/events", body, idempotency_key=idempotency_key),
            UsageEvent,
        )

    async def track_model_tokens(
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
        return await self.track(
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

    async def check(
        self,
        *,
        customer_id: str,
        feature_code: str,
        quantity: int,
    ) -> ApiResponse[UsageCheckResult]:
        body = build_body(customer_id=customer_id, feature_code=feature_code, quantity=quantity)
        return _parse(await self._http.post("/usage/check", body), UsageCheckResult)

    async def set(
        self,
        *,
        customer_id: str,
        feature: str,
        value: int,
        idempotency_key: str | None = None,
        reason: str | None = None,
    ) -> ApiResponse[UsageAdjustment]:
        body = build_body(
            customer_id=customer_id,
            feature=feature,
            value=value,
            idempotency_key=idempotency_key,
            reason=reason,
        )
        return _parse(
            await self._http.put("/usage", body, idempotency_key=idempotency_key),
            UsageAdjustment,
        )
