# ruff: noqa: E501

from __future__ import annotations

import builtins
from typing import Any

from .._async_http import AsyncCommetHTTPClient
from .._shared import build_body
from ..types import (
    DeletedObject,
    MarketGroup,
    PricingListMarketGroupsResult,
    _parse_data,
)


class AsyncPricingResource:
    def __init__(self, http: AsyncCommetHTTPClient) -> None:
        self._http = http

    async def get_market_group(self, id: str) -> MarketGroup:
        """Get one reusable pricing market group."""
        return _parse_data(await self._http.get(f"/pricing/market-groups/{id}"), MarketGroup)

    async def update_market_group(
        self,
        id: str,
        *,
        name: str,
        country_codes: builtins.list[str],
        metadata: dict[str, Any] | None = None,
        idempotency_key: str | None = None,
    ) -> MarketGroup:
        """Replace the name, countries, and metadata of a pricing market group."""
        body = build_body(name=name, country_codes=country_codes, metadata=metadata)
        return _parse_data(
            await self._http.patch(
                f"/pricing/market-groups/{id}", body, idempotency_key=idempotency_key
            ),
            MarketGroup,
        )

    async def delete_market_group(self, id: str) -> DeletedObject:
        """Delete an unused pricing market group. Groups referenced by prices or subscriptions cannot be deleted."""
        return _parse_data(await self._http.delete(f"/pricing/market-groups/{id}"), DeletedObject)

    async def list_market_groups(self) -> PricingListMarketGroupsResult:
        """List reusable country groups used to resolve market-specific prices independently from currency."""
        return _parse_data(
            await self._http.get("/pricing/market-groups"), PricingListMarketGroupsResult
        )

    async def create_market_group(
        self,
        *,
        name: str,
        country_codes: builtins.list[str],
        metadata: dict[str, Any] | None = None,
        idempotency_key: str | None = None,
    ) -> MarketGroup:
        """Create a reusable country group. Countries can belong to only one active group; each price chooses its currency independently."""
        body = build_body(name=name, country_codes=country_codes, metadata=metadata)
        return _parse_data(
            await self._http.post("/pricing/market-groups", body, idempotency_key=idempotency_key),
            MarketGroup,
        )
