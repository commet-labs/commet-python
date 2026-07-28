from __future__ import annotations

import asyncio
import logging
import time
from typing import Any
from uuid import uuid4

import httpx

from ._exceptions import CommetAPIError
from ._http import _BODY_METHODS, ApiResponse
from ._shared import (
    _BASE_URL,
    _RETRYABLE_STATUS_CODES,
    API_VERSION,
    backoff_delay_seconds,
    build_headers,
    convert_keys,
    handle_error,
    query_value,
    retry_delay_seconds,
    to_camel,
    to_snake,
)
from ._telemetry import format_request_metrics

logger = logging.getLogger("commet")


class AsyncCommetHTTPClient:
    def __init__(
        self,
        api_key: str,
        *,
        api_version: str = API_VERSION,
        timeout: float = 30.0,
        retries: int = 3,
        telemetry: bool = True,
    ) -> None:
        self._api_version = api_version
        self._telemetry_enabled = telemetry
        self._last_request_metrics: dict[str, Any] | None = None
        self._client = httpx.AsyncClient(
            base_url=f"{_BASE_URL}/api/v1",
            headers=build_headers(api_key, api_version, telemetry=telemetry),
            timeout=timeout,
        )
        self._max_retries = retries

    async def close(self) -> None:
        await self._client.aclose()

    async def get(
        self,
        endpoint: str,
        params: dict[str, Any] | None = None,
        *,
        api_version: str | None = None,
        idempotency_key: str | None = None,
        timeout: float | None = None,
    ) -> ApiResponse[Any]:
        clean = (
            {to_camel(k): query_value(v) for k, v in params.items() if v is not None}
            if params
            else None
        )
        return await self._request(
            "GET",
            endpoint,
            params=clean,
            api_version=api_version,
            idempotency_key=idempotency_key,
            timeout=timeout,
        )

    async def post(
        self,
        endpoint: str,
        body: dict[str, Any] | None = None,
        *,
        api_version: str | None = None,
        idempotency_key: str | None = None,
        timeout: float | None = None,
    ) -> ApiResponse[Any]:
        return await self._request(
            "POST",
            endpoint,
            body=body,
            api_version=api_version,
            idempotency_key=idempotency_key,
            timeout=timeout,
        )

    async def put(
        self,
        endpoint: str,
        body: dict[str, Any] | None = None,
        *,
        api_version: str | None = None,
        idempotency_key: str | None = None,
        timeout: float | None = None,
    ) -> ApiResponse[Any]:
        return await self._request(
            "PUT",
            endpoint,
            body=body,
            api_version=api_version,
            idempotency_key=idempotency_key,
            timeout=timeout,
        )

    async def patch(
        self,
        endpoint: str,
        body: dict[str, Any] | None = None,
        *,
        api_version: str | None = None,
        idempotency_key: str | None = None,
        timeout: float | None = None,
    ) -> ApiResponse[Any]:
        return await self._request(
            "PATCH",
            endpoint,
            body=body,
            api_version=api_version,
            idempotency_key=idempotency_key,
            timeout=timeout,
        )

    async def delete(
        self,
        endpoint: str,
        body: dict[str, Any] | None = None,
        *,
        api_version: str | None = None,
        idempotency_key: str | None = None,
        timeout: float | None = None,
    ) -> ApiResponse[Any]:
        return await self._request(
            "DELETE",
            endpoint,
            body=body,
            api_version=api_version,
            idempotency_key=idempotency_key,
            timeout=timeout,
        )

    async def _request(
        self,
        method: str,
        endpoint: str,
        *,
        body: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
        api_version: str | None = None,
        idempotency_key: str | None = None,
        timeout: float | None = None,
    ) -> ApiResponse[Any]:
        headers: dict[str, str] = {}
        if api_version is not None:
            headers["commet-version"] = api_version
        if method in _BODY_METHODS and self._max_retries > 0 and not idempotency_key:
            headers["Idempotency-Key"] = f"commet-python-retry-{uuid4()}"
        elif idempotency_key:
            headers["Idempotency-Key"] = idempotency_key

        json_body = convert_keys(body, to_camel) if body else None

        logger.debug("%s %s", method, endpoint)
        if json_body:
            logger.debug("Body: %s", json_body)

        return await self._execute(
            method, endpoint, json_body=json_body, params=params, headers=headers, timeout=timeout
        )

    async def _execute(
        self,
        method: str,
        endpoint: str,
        *,
        json_body: Any = None,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        timeout: float | None = None,
        attempt: int = 1,
    ) -> ApiResponse[Any]:
        if headers is None:
            headers = {}
        if self._telemetry_enabled and self._last_request_metrics is not None:
            headers["commet-client-telemetry"] = format_request_metrics(
                self._last_request_metrics["request_id"],
                self._last_request_metrics["duration_ms"],
            )
            self._last_request_metrics = None

        request_start = time.monotonic()
        try:
            resp = await self._client.request(
                method, endpoint, json=json_body, params=params, headers=headers, timeout=timeout
            )
        except httpx.TimeoutException:
            if attempt <= self._max_retries:
                await self._wait(backoff_delay_seconds(attempt), attempt)
                return await self._execute(
                    method,
                    endpoint,
                    json_body=json_body,
                    params=params,
                    headers=headers,
                    timeout=timeout,
                    attempt=attempt + 1,
                )
            raise

        logger.debug("Response: %d", resp.status_code)

        if resp.status_code in _RETRYABLE_STATUS_CODES and attempt <= self._max_retries:
            delay = retry_delay_seconds(resp.status_code, resp.headers.get("retry-after"), attempt)
            if delay is not None:
                await self._wait(delay, attempt)
                return await self._execute(
                    method,
                    endpoint,
                    json_body=json_body,
                    params=params,
                    headers=headers,
                    timeout=timeout,
                    attempt=attempt + 1,
                )

        try:
            data = resp.json()
        except Exception:
            raise CommetAPIError(
                f"Invalid JSON response: {resp.status_code}",
                status_code=resp.status_code,
                code="INVALID_JSON",
            )

        if resp.is_error:
            logger.debug("Error response: %s", data)
            handle_error(resp.status_code, data)

        if self._telemetry_enabled:
            duration_ms = int((time.monotonic() - request_start) * 1000)
            request_id = resp.headers.get("x-request-id", f"req_{int(time.time())}")
            self._last_request_metrics = {"request_id": request_id, "duration_ms": duration_ms}

        converted = convert_keys(data, to_snake)
        is_envelope = (
            isinstance(converted, dict)
            and isinstance(converted.get("success"), bool)
            and "data" in converted
        )
        if not is_envelope:
            return ApiResponse(success=True, data=converted)
        return ApiResponse(
            success=converted.get("success", True),
            data=converted.get("data"),
            code=converted.get("code"),
            message=converted.get("message"),
            has_more=converted.get("has_more"),
            next_cursor=converted.get("next_cursor"),
        )

    async def _wait(self, delay: float, attempt: int) -> None:
        logger.debug("Retrying in %ss (attempt %d/%d)", delay, attempt, self._max_retries)
        await asyncio.sleep(delay)
