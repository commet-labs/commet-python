# ruff: noqa: E501

from __future__ import annotations

from .._async_http import AsyncCommetHTTPClient
from .._http import ApiResponse
from .._shared import build_body
from ..types import (
    FeatureAccess,
    FeatureLookup,
    _parse,
    _parse_list,
)


class AsyncFeatureAccessResource:
    def __init__(self, http: AsyncCommetHTTPClient) -> None:
        self._http = http

    async def list(self, *, customer_id: str) -> ApiResponse[list[FeatureAccess]]:
        """List all features for a customer's active subscription, scoped by the customerId query parameter."""
        query = build_body(customer_id=customer_id)
        return _parse_list(await self._http.get("/feature-access", query), FeatureAccess)

    async def get(
        self, code: str, *, customer_id: str, action: str | None = None
    ) -> ApiResponse[FeatureLookup]:
        """Get feature access details for a customer. Use action=canUse to check if the customer can consume one more unit."""
        query = build_body(customer_id=customer_id, action=action)
        return _parse(await self._http.get(f"/feature-access/{code}", query), FeatureLookup)

    async def can_use(self, code: str, *, customer_id: str) -> ApiResponse[FeatureLookup]:
        """Get feature access details for a customer. Use action=canUse to check if the customer can consume one more unit."""
        query = build_body(action="canUse", customer_id=customer_id)
        return _parse(await self._http.get(f"/feature-access/{code}", query), FeatureLookup)
