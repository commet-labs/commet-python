from __future__ import annotations

import logging
import re
import time
from dataclasses import dataclass
from typing import Any
from uuid import uuid4

import httpx

from ._exceptions import CommetAPIError, CommetValidationError

logger = logging.getLogger("commet")

# -- Case conversion --

_UPPER_AFTER_LOWER = re.compile(r"(.)([A-Z][a-z]+)")
_LOWER_BEFORE_UPPER = re.compile(r"([a-z0-9])([A-Z])")

_RETRYABLE_STATUS_CODES = frozenset({408, 429, 500, 502, 503, 504})

_BASE_URLS = {
    "production": "https://commet.co",
    "sandbox": "https://sandbox.commet.co",
}


def _to_snake(name: str) -> str:
    return _LOWER_BEFORE_UPPER.sub(r"\1_\2", _UPPER_AFTER_LOWER.sub(r"\1_\2", name)).lower()


def _to_camel(name: str) -> str:
    parts = name.split("_")
    return parts[0] + "".join(p.capitalize() for p in parts[1:])


def _convert_keys(obj: Any, fn: Any) -> Any:
    if isinstance(obj, dict):
        return {fn(k): _convert_keys(v, fn) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_convert_keys(i, fn) for i in obj]
    return obj


def build_body(**kwargs: Any) -> dict[str, Any]:
    """Build request body, stripping None values."""
    return {k: v for k, v in kwargs.items() if v is not None}


# -- Response --


@dataclass
class ApiResponse:
    success: bool
    data: Any = None
    code: str | None = None
    message: str | None = None
    has_more: bool | None = None
    next_cursor: str | None = None


# -- HTTP Client --


class CommetHTTPClient:
    def __init__(
        self,
        api_key: str,
        environment: str,
        *,
        timeout: float = 30.0,
        retries: int = 3,
    ) -> None:
        base_url = _BASE_URLS[environment]
        self._client = httpx.Client(
            base_url=f"{base_url}/api",
            headers={
                "x-api-key": api_key,
                "Content-Type": "application/json",
                "User-Agent": f"commet-python/{_get_version()}",
            },
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
    ) -> ApiResponse:
        clean = (
            {_to_camel(k): v for k, v in params.items() if v is not None}
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
    ) -> ApiResponse:
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
    ) -> ApiResponse:
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
    ) -> ApiResponse:
        return self._request(
            "DELETE", endpoint, body=body, idempotency_key=idempotency_key, timeout=timeout
        )

    # -- Internals --

    def _request(
        self,
        method: str,
        endpoint: str,
        *,
        body: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
        idempotency_key: str | None = None,
        timeout: float | None = None,
    ) -> ApiResponse:
        headers: dict[str, str] = {}
        if method == "POST":
            headers["Idempotency-Key"] = idempotency_key or f"sdk_{uuid4().hex}"

        json_body = _convert_keys(body, _to_camel) if body else None

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
    ) -> ApiResponse:
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
            if resp.status_code == 404:
                return ApiResponse(success=False, code="not_found", message="Resource not found")
            raise CommetAPIError(
                f"Invalid JSON response: {resp.status_code}",
                status_code=resp.status_code,
                code="INVALID_JSON",
            )

        if resp.is_error:
            self._handle_error(resp.status_code, data)

        converted = _convert_keys(data, _to_snake)
        return ApiResponse(
            success=converted.get("success", True),
            data=converted.get("data"),
            code=converted.get("code"),
            message=converted.get("message"),
            has_more=converted.get("has_more"),
            next_cursor=converted.get("next_cursor"),
        )

    def _handle_error(self, status_code: int, data: Any) -> None:
        if not isinstance(data, dict):
            raise CommetAPIError(
                f"Request failed with status {status_code}", status_code=status_code
            )

        if data.get("code") == "validation_error" and isinstance(data.get("details"), list):
            errors: dict[str, list[str]] = {}
            for detail in data["details"]:
                field = detail.get("field", "unknown")
                errors.setdefault(field, []).append(detail.get("message", ""))
            raise CommetValidationError(
                data.get("message", "Validation failed"), validation_errors=errors
            )

        raise CommetAPIError(
            data.get("message", f"Request failed with status {status_code}"),
            status_code=status_code,
            code=data.get("code"),
            details=data.get("details"),
        )

    def _wait(self, attempt: int) -> None:
        delay = min(1.0 * (2 ** (attempt - 1)), 8.0)
        logger.debug("Retrying in %ss (attempt %d/%d)", delay, attempt, self._max_retries)
        time.sleep(delay)


def _get_version() -> str:
    try:
        from importlib.metadata import version

        return version("commet")
    except Exception:
        return "0.1.0"
