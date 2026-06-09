# ruff: noqa: E501

from __future__ import annotations

from .._http import ApiResponse, CommetHTTPClient
from .._shared import build_body
from ..types import (
    ApiKey,
    CreatedApiKey,
    DeletedObject,
    _parse,
    _parse_list,
)


class ApiKeysResource:
    def __init__(self, http: CommetHTTPClient) -> None:
        self._http = http

    def list(
        self, *, cursor: str | None = None, limit: int | None = None
    ) -> ApiResponse[list[ApiKey]]:
        """List API keys with cursor-based pagination. Keys are returned without the full secret."""
        query = build_body(cursor=cursor, limit=limit)
        return _parse_list(self._http.get("/api-keys", query), ApiKey)

    def create(
        self, *, name: str, expires_in_days: int | None = None, idempotency_key: str | None = None
    ) -> ApiResponse[CreatedApiKey]:
        """Create a new API key. The full key is only returned once in the response."""
        body = build_body(name=name, expires_in_days=expires_in_days)
        return _parse(
            self._http.post("/api-keys", body, idempotency_key=idempotency_key), CreatedApiKey
        )

    def delete(self, id: str) -> ApiResponse[DeletedObject]:
        """Permanently revoke and delete an API key."""
        return _parse(self._http.delete(f"/api-keys/{id}"), DeletedObject)
