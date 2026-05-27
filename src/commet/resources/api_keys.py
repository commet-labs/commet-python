from __future__ import annotations

from typing import Any

from .._http import ApiResponse, CommetHTTPClient
from .._shared import build_body


class ApiKeysResource:
    def __init__(self, http: CommetHTTPClient) -> None:
        self._http = http

    def list(
        self,
        *,
        limit: int | None = None,
        cursor: str | None = None,
    ) -> ApiResponse[Any]:
        return self._http.get("/api-keys", build_body(limit=limit, cursor=cursor))

    def create(
        self,
        *,
        name: str,
        expires_in_days: int | None = None,
        idempotency_key: str | None = None,
    ) -> ApiResponse[Any]:
        return self._http.post(
            "/api-keys",
            build_body(name=name, expires_in_days=expires_in_days),
            idempotency_key=idempotency_key,
        )

    def delete(
        self,
        api_key_id: str,
        *,
        idempotency_key: str | None = None,
    ) -> ApiResponse[Any]:
        return self._http.delete(f"/api-keys/{api_key_id}", idempotency_key=idempotency_key)
