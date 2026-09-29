# ruff: noqa: E501

from __future__ import annotations

from .._http import CommetHTTPClient
from .._shared import build_body
from ..types import (
    ApiKeysListResult,
    CreateApiKeyParamsPermissions,
    CreatedApiKey,
    DeletedObject,
    _parse_data,
)


class ApiKeysResource:
    def __init__(self, http: CommetHTTPClient) -> None:
        self._http = http

    def delete(self, id: str) -> DeletedObject:
        """Permanently revoke and delete an API key."""
        return _parse_data(self._http.delete(f"/api-keys/{id}"), DeletedObject)

    def list(self, *, cursor: str | None = None, limit: int | None = None) -> ApiKeysListResult:
        """List API keys with cursor-based pagination. Keys are returned without the full secret."""
        query = build_body(cursor=cursor, limit=limit)
        return _parse_data(self._http.get("/api-keys", query), ApiKeysListResult)

    def create(
        self,
        *,
        name: str,
        expires_in_days: int | None = None,
        permissions: CreateApiKeyParamsPermissions | None = None,
        idempotency_key: str | None = None,
    ) -> CreatedApiKey:
        """Create a full-access or restricted API key. Provide permissions to restrict access; the full key is returned only once. A restricted key with api_key: write may only create restricted keys with the same or fewer permissions, and they expire no later than the key that creates them."""
        body = build_body(name=name, expires_in_days=expires_in_days, permissions=permissions)
        return _parse_data(
            self._http.post("/api-keys", body, idempotency_key=idempotency_key), CreatedApiKey
        )
