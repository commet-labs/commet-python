from __future__ import annotations

import logging
import time
from dataclasses import dataclass
from typing import Any, Generic, TypeVar
from uuid import uuid4

import httpx

from ._exceptions import CommetAPIError
from ._shared import (
    _BASE_URL,
    _RETRYABLE_STATUS_CODES,
    build_headers,
    convert_keys,
    handle_error,
    to_camel,
    to_snake,
)

logger = logging.getLogger("commet")

T = TypeVar("T")


@dataclass
class ApiResponse(Generic[T]):
    success: bool
    data: T | None = None
    code: str | None = None
    message: str | None = None
    has_more: bool | None = None
    next_cursor: str | None = None


class CommetHTTPClient:
    def __init__(
        self,
        api_key: str,
        *,
        timeout: float = 30.0,
        retries: int = 3,
    ) -> None:
        self._client = httpx.Client(
            base_url=f"{_BASE_URL}/api",
            headers=build_headers(api_key),
            timeout=timeout,
        )
        self._max_retries = retries

    def close(self) -> None:
        self._client.close()

    def get(
        self,
        endpoint: str,
        params: dict[str, Any] | None = None,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
    ) -> ApiResponse[Any]:
        clean = (
            {to_camel(k): v for k, v in params.items() if v is not None}
            if params
            else None
        )
        return self._request(
            "GET", endpoint, params=clean, idempotency_key=idempotency_key, timeout=timeout
        )

    def post(
        self,
        endpoint: str,
        body: dict[str, Any] | None = None,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
    ) -> ApiResponse[Any]:
        return self._request(
            "POST", endpoint, body=body, idempotency_key=idempotency_key, timeout=timeout
        )

    def put(
        self,
        endpoint: str,
        body: dict[str, Any] | None = None,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
    ) -> ApiResponse[Any]:
        return self._request(
            "PUT", endpoint, body=body, idempotency_key=idempotency_key, timeout=timeout
        )

    def delete(
        self,
        endpoint: str,
        body: dict[str, Any] | None = None,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
    ) -> ApiResponse[Any]:
        return self._request(
            "DELETE", endpoint, body=body, idempotency_key=idempotency_key, timeout=timeout
        )

    def _request(
        self,
        method: str,
        endpoint: str,
        *,
        body: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
        idempotency_key: str | None = None,
        timeout: float | None = None,
    ) -> ApiResponse[Any]:
        headers: dict[str, str] = {}
        if method == "POST":
            headers["Idempotency-Key"] = idempotency_key or f"sdk_{uuid4().hex}"

        json_body = convert_keys(body, to_camel) if body else None

        logger.debug("%s %s", method, endpoint)
        if json_body:
            logger.debug("Body: %s", json_body)

        return self._execute(
            method, endpoint, json_body=json_body, params=params, headers=headers, timeout=timeout
        )

    def _execute(
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
            resp = self._client.request(
                method, endpoint, json=json_body, params=params, headers=headers, timeout=timeout
            )
        except httpx.TimeoutException:
            if attempt <= self._max_retries:
                self._wait(attempt)
                return self._execute(
                    method, endpoint, json_body=json_body, params=params,
                    headers=headers, timeout=timeout, attempt=attempt + 1,
                )
            raise

        logger.debug("Response: %d", resp.status_code)

        if resp.status_code in _RETRYABLE_STATUS_CODES and attempt <= self._max_retries:
            self._wait(attempt)
            return self._execute(
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

    def _wait(self, attempt: int) -> None:
        delay = min(1.0 * (2 ** (attempt - 1)), 8.0)
        logger.debug("Retrying in %ss (attempt %d/%d)", delay, attempt, self._max_retries)
        time.sleep(delay)
