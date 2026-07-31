# ruff: noqa: E501

from __future__ import annotations

import builtins
from typing import Any

from .._async_http import AsyncCommetHTTPClient
from .._shared import build_body
from ..types import (
    DeletedObject,
    Market,
    MarketsListResult,
    _parse_data,
)


class AsyncMarketsResource:
    def __init__(self, http: AsyncCommetHTTPClient) -> None:
        self._http = http

    async def get(self, id: str) -> Market:
        """Get one reusable market."""
        return _parse_data(await self._http.get(f"/markets/{id}"), Market)

    async def update(
        self,
        id: str,
        *,
        name: str,
        country_codes: builtins.list[str],
        metadata: dict[str, Any] | None = None,
        idempotency_key: str | None = None,
    ) -> Market:
        """Replace the name, countries, and metadata of a market."""
        body = build_body(name=name, country_codes=country_codes, metadata=metadata)
        return _parse_data(
            await self._http.patch(f"/markets/{id}", body, idempotency_key=idempotency_key), Market
        )

    async def delete(self, id: str) -> DeletedObject:
        """Delete an unused market. Markets referenced by prices or subscriptions cannot be deleted."""
        return _parse_data(await self._http.delete(f"/markets/{id}"), DeletedObject)

    async def list(self) -> MarketsListResult:
        """List reusable country groups that resolve market-specific prices independently from currency."""
        return _parse_data(await self._http.get("/markets"), MarketsListResult)

    async def create(
        self,
        *,
        name: str,
        country_codes: builtins.list[str],
        metadata: dict[str, Any] | None = None,
        idempotency_key: str | None = None,
    ) -> Market:
        """Create a reusable market without attaching it to a plan or price. Countries can belong to only one active market."""
        body = build_body(name=name, country_codes=country_codes, metadata=metadata)
        return _parse_data(
            await self._http.post("/markets", body, idempotency_key=idempotency_key), Market
        )
