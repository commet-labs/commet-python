from __future__ import annotations

import json
import os
import platform
import sys

from ._shared import get_version

_cached_client_info: str | None = None
_cached_user_agent: str | None = None

_registered_integrations: set[str] = set()


def register_integration(name: str, version: str) -> None:
    global _cached_client_info
    _registered_integrations.add(f"{name}@{version}")
    _cached_client_info = None


def _detect_runtime() -> tuple[str, str]:
    impl = platform.python_implementation().lower()
    return impl, platform.python_version()


def _detect_execution_context() -> str | None:
    if "pytest" in sys.modules or os.environ.get("PYTEST_CURRENT_TEST"):
        return "test"
    env = os.environ
    if env.get("CI") or env.get("GITHUB_ACTIONS") or env.get("GITLAB_CI") or env.get("CIRCLECI"):
        return "ci"
    return None


def get_client_info_header() -> str:
    global _cached_client_info
    if _cached_client_info is None:
        runtime_name, runtime_version = _detect_runtime()
        info: dict[str, object] = {
            "sdk": "commet-python",
            "sdk_version": get_version(),
            "lang": "python",
            "lang_version": platform.python_version(),
            "platform": sys.platform,
            "arch": platform.machine(),
            "runtime": runtime_name,
            "runtime_version": runtime_version,
            "integrations": sorted(_registered_integrations),
        }
        execution_context = _detect_execution_context()
        if execution_context is not None:
            info["execution_context"] = execution_context
        _cached_client_info = json.dumps(info)
    return _cached_client_info


def get_user_agent() -> str:
    global _cached_user_agent
    if _cached_user_agent is None:
        runtime_name, runtime_version = _detect_runtime()
        _cached_user_agent = (
            f"commet-python/{get_version()} {runtime_name}/{runtime_version}"
            f" {sys.platform}/{platform.machine()}"
        )
    return _cached_user_agent


def format_request_metrics(request_id: str, duration_ms: int) -> str:
    return json.dumps(
        {"last_request_metrics": {"request_id": request_id, "duration_ms": duration_ms}}
    )
