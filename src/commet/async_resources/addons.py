# ruff: noqa: E501

from __future__ import annotations

from typing import Literal

from .._async_http import AsyncCommetHTTPClient
from .._http import ApiResponse
from .._shared import build_body
from ..types import (
    ActiveAddon,
    Addon,
    DeletedObject,
    _parse,
    _parse_list,
)


class AsyncAddonsResource:
    def __init__(self, http: AsyncCommetHTTPClient) -> None:
        self._http = http

    async def list_active(self, *, customer_id: str) -> ApiResponse[list[ActiveAddon]]:
        """List all active add-ons for a customer's subscription."""
        query = build_body(customer_id=customer_id)
        return _parse_list(await self._http.get("/active-addons", query), ActiveAddon)

    async def list(
        self, *, limit: int | None = None, cursor: str | None = None
    ) -> ApiResponse[list[Addon]]:
        """List all add-ons with cursor-based pagination."""
        query = build_body(limit=limit, cursor=cursor)
        return _parse_list(await self._http.get("/addons", query), Addon)

    async def get(self, id: str) -> ApiResponse[Addon]:
        """Retrieve an add-on by its public ID or slug."""
        return _parse(await self._http.get(f"/addons/{id}"), Addon)

    async def create(
        self,
        *,
        name: str,
        base_price: int,
        feature_id: str,
        consumption_model: Literal["boolean", "metered", "credits", "balance"],
        description: str | None = None,
        included_units: int | None = None,
        overage_rate: int | None = None,
        credit_cost: int | None = None,
        idempotency_key: str | None = None,
    ) -> ApiResponse[Addon]:
        """Create a new add-on linked to a feature. Each feature can only be assigned to one add-on."""
        body = build_body(
            name=name,
            description=description,
            base_price=base_price,
            feature_id=feature_id,
            consumption_model=consumption_model,
            included_units=included_units,
            overage_rate=overage_rate,
            credit_cost=credit_cost,
        )
        return _parse(
            await self._http.post("/addons", body, idempotency_key=idempotency_key), Addon
        )

    async def update(
        self,
        id: str,
        *,
        name: str | None = None,
        description: str | None = None,
        base_price: int | None = None,
        included_units: int | None = None,
        overage_rate: int | None = None,
        idempotency_key: str | None = None,
    ) -> ApiResponse[Addon]:
        """Update an add-on's name, description, or pricing."""
        body = build_body(
            name=name,
            description=description,
            base_price=base_price,
            included_units=included_units,
            overage_rate=overage_rate,
        )
        return _parse(
            await self._http.put(f"/addons/{id}", body, idempotency_key=idempotency_key), Addon
        )

    async def delete(self, id: str) -> ApiResponse[DeletedObject]:
        """Soft-delete an add-on. Fails if the add-on has active subscriptions."""
        return _parse(await self._http.delete(f"/addons/{id}"), DeletedObject)
