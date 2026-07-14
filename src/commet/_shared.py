from __future__ import annotations

import logging
import re
from enum import Enum
from typing import Any, Callable

from ._exceptions import CommetAPIError, CommetValidationError

logger = logging.getLogger("commet")

_UPPER_AFTER_LOWER = re.compile(r"(.)([A-Z][a-z]+)")
_LOWER_BEFORE_UPPER = re.compile(r"([a-z0-9])([A-Z])")

_RETRYABLE_STATUS_CODES = frozenset({408, 429, 500, 502, 503, 504})

_RETRY_AFTER_CAP_SECONDS = 30.0


def backoff_delay_seconds(attempt: int) -> float:
    return min(1.0 * (2 ** (attempt - 1)), 8.0)


def retry_delay_seconds(
    status_code: int, retry_after_header: str | None, attempt: int
) -> float | None:
    """429 retries wait exactly what the rate limiter reports in Retry-After
    (seconds until the window resets); a 429 without the header did not come
    from the rate limiter, so it is not retried (returns None). Exponential
    backoff only applies to statuses that carry no server-provided wait."""
    if status_code != 429:
        return backoff_delay_seconds(attempt)
    try:
        seconds = float(retry_after_header) if retry_after_header is not None else 0.0
    except ValueError:
        return None
    if seconds <= 0:
        return None
    return min(seconds, _RETRY_AFTER_CAP_SECONDS)


_BASE_URL = "https://commet.co"

API_VERSION = "2026-07-11"


def to_snake(name: str) -> str:
    return _LOWER_BEFORE_UPPER.sub(r"\1_\2", _UPPER_AFTER_LOWER.sub(r"\1_\2", name)).lower()


def to_camel(name: str) -> str:
    parts = name.split("_")
    return parts[0] + "".join(p.capitalize() for p in parts[1:])


def convert_keys(obj: Any, fn: Callable[[str], str]) -> Any:
    if isinstance(obj, dict):
        return {fn(k): convert_keys(v, fn) for k, v in obj.items()}
    if isinstance(obj, list):
        return [convert_keys(i, fn) for i in obj]
    return obj


def build_body(**kwargs: Any) -> dict[str, Any]:
    return {k: v for k, v in kwargs.items() if v is not None}


def query_value(value: Any) -> Any:
    if isinstance(value, Enum):
        return value.value
    return value


def handle_error(status_code: int, data: Any) -> None:
    if not isinstance(data, dict):
        raise CommetAPIError(f"Request failed with status {status_code}", status_code=status_code)

    error_obj = data.get("error")
    if isinstance(error_obj, dict):
        source = error_obj
    else:
        source = data

    error_type = source.get("type", "api_error")
    error_code = source.get("code", "unknown")
    error_message = source.get("message", f"Request failed with status {status_code}")
    error_param = source.get("param")
    error_details = source.get("details")
    error_doc_url = source.get("doc_url")

    if error_code == "validation_error" and isinstance(error_details, list):
        errors: dict[str, list[str]] = {}
        for detail in error_details:
            field = detail.get("field", "unknown")
            errors.setdefault(field, []).append(detail.get("message", ""))
        raise CommetValidationError(error_message, validation_errors=errors)

    raise CommetAPIError(
        error_message,
        status_code=status_code,
        code=error_code,
        details=error_details,
        type=error_type,
        param=error_param,
        doc_url=error_doc_url,
    )


def get_version() -> str:
    try:
        from importlib.metadata import version

        return version("commet-sdk")
    except Exception:
        return "0.1.0"


def build_headers(api_key: str, api_version: str, *, telemetry: bool = True) -> dict[str, str]:
    from ._telemetry import get_client_info_header, get_user_agent

    headers = {
        "x-api-key": api_key,
        "commet-version": api_version,
        "Content-Type": "application/json",
        "User-Agent": get_user_agent(),
    }
    if telemetry:
        headers["commet-client-info"] = get_client_info_header()
    return headers
