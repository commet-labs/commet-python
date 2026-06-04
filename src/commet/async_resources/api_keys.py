from __future__ import annotations

from .._async_http import AsyncCommetHTTPClient
from .._http import ApiResponse
from .._resource_mixins import parse_api_key_created, parse_api_key_list
from .._shared import build_body
from ..types import ApiKeyCreated, ApiKeyData


class AsyncApiKeysResource:
    def __init__(self, http: AsyncCommetHTTPClient) -> None:
        self._http = http

    async def list(
        self,
        *,
        limit: int | None = None,
        cursor: str | None = None,
    ) -> ApiResponse[list[ApiKeyData]]:
        return parse_api_key_list(
            await self._http.get("/api-keys", build_body(limit=limit, cursor=cursor))
        )

    async def create(
        self,
        *,
        name: str,
        expires_in_days: int | None = None,
        idempotency_key: str | None = None,
    ) -> ApiResponse[ApiKeyCreated]:
        return parse_api_key_created(await self._http.post(
            "/api-keys",
            build_body(name=name, expires_in_days=expires_in_days),
            idempotency_key=idempotency_key,
        ))

    async def delete(
        self,
        api_key_id: str,
        *,
        idempotency_key: str | None = None,
    ) -> ApiResponse[None]:
        return await self._http.delete(
            f"/api-keys/{api_key_id}", idempotency_key=idempotency_key,
        )
