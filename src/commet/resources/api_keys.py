from __future__ import annotations

from .._http import ApiResponse, CommetHTTPClient
from .._resource_mixins import parse_api_key_created, parse_api_key_list
from .._shared import build_body
from ..types import ApiKeyCreated, ApiKeyData


class ApiKeysResource:
    def __init__(self, http: CommetHTTPClient) -> None:
        self._http = http

    def list(
        self,
        *,
        limit: int | None = None,
        cursor: str | None = None,
    ) -> ApiResponse[list[ApiKeyData]]:
        return parse_api_key_list(
            self._http.get("/api-keys", build_body(limit=limit, cursor=cursor))
        )

    def create(
        self,
        *,
        name: str,
        expires_in_days: int | None = None,
        idempotency_key: str | None = None,
    ) -> ApiResponse[ApiKeyCreated]:
        return parse_api_key_created(self._http.post(
            "/api-keys",
            build_body(name=name, expires_in_days=expires_in_days),
            idempotency_key=idempotency_key,
        ))

    def delete(
        self,
        api_key_id: str,
        *,
        idempotency_key: str | None = None,
    ) -> ApiResponse[None]:
        return self._http.delete(f"/api-keys/{api_key_id}", idempotency_key=idempotency_key)
