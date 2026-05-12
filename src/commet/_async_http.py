from __future__ import annotations

import asyncio
import logging
from typing import Any
from uuid import uuid4

import httpx

from ._exceptions import CommetAPIError
from ._http import ApiResponse
from ._shared import (
    API_VERSION,
    _BASE_URL,
    _RETRYABLE_STATUS_CODES,
    build_headers,
    convert_keys,
    handle_error,
    to_camel,
    to_snake,
)

logger = logging.getLogger("commet")


class AsyncCommetHTTPClient:
    def __init__(
        self,
        api_key: str,
        *,
        api_version: str = API_VERSION,
        timeout: float = 30.0,
        retries: int = 3,
    ) -> None:
        self._api_version = api_version
        self._client = httpx.AsyncClient(
            base_url=f"{_BASE_URL}/api/v1",
            headers=build_headers(api_key, api_version),
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
            {to_camel(k): v for k, v in params.items() if v is not None}
            if params
            else None
        )
        return await self._request(
            "GET", endpoint, params=clean, api_version=api_version, idempotency_key=idempotency_key, timeout=timeout
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
            "POST", endpoint, body=body, api_version=api_version, idempotency_key=idempotency_key, timeout=timeout
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
            "PUT", endpoint, body=body, api_version=api_version, idempotency_key=idempotency_key, timeout=timeout
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
            "DELETE", endpoint, body=body, api_version=api_version, idempotency_key=idempotency_key, timeout=timeout
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
        if method == "POST":
            headers["Idempotency-Key"] = idempotency_key or f"sdk_{uuid4().hex}"

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
        try:
            resp = await self._client.request(
                method, endpoint, json=json_body, params=params, headers=headers, timeout=timeout
            )
        except httpx.TimeoutException:
            if attempt <= self._max_retries:
                await self._wait(attempt)
                return await self._execute(
                    method, endpoint, json_body=json_body, params=params,
                    headers=headers, timeout=timeout, attempt=attempt + 1,
                )
            raise

        logger.debug("Response: %d", resp.status_code)

        if resp.status_code in _RETRYABLE_STATUS_CODES and attempt <= self._max_retries:
            await self._wait(attempt)
            return await self._execute(
                method, endpoint, json_body=json_body, params=params,
                headers=headers, timeout=timeout, attempt=attempt + 1,
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
            handle_error(resp.status_code, data)

        converted = convert_keys(data, to_snake)
        return ApiResponse(
            success=converted.get("success", True),
            data=converted.get("data"),
            code=converted.get("code"),
            message=converted.get("message"),
            has_more=converted.get("has_more"),
            next_cursor=converted.get("next_cursor"),
        )

    async def _wait(self, attempt: int) -> None:
        delay = min(1.0 * (2 ** (attempt - 1)), 8.0)
        logger.debug("Retrying in %ss (attempt %d/%d)", delay, attempt, self._max_retries)
        await asyncio.sleep(delay)
