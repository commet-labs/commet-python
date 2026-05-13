from __future__ import annotations

import logging
import re
from typing import Any, Callable

from ._exceptions import CommetAPIError, CommetValidationError

logger = logging.getLogger("commet")

_UPPER_AFTER_LOWER = re.compile(r"(.)([A-Z][a-z]+)")
_LOWER_BEFORE_UPPER = re.compile(r"([a-z0-9])([A-Z])")

_RETRYABLE_STATUS_CODES = frozenset({408, 429, 500, 502, 503, 504})

_BASE_URL = "https://commet.co"

API_VERSION = "2026-05-12"


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


def handle_error(status_code: int, data: Any) -> None:
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
