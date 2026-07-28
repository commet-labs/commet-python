# ruff: noqa: E501

from __future__ import annotations

from typing import Literal

from .._async_http import AsyncCommetHTTPClient
from .._shared import build_body
from ..types import (
    Addon,
    AddonsListActiveResult,
    AddonsListResult,
    DeletedObject,
    _parse_data,
)


class AsyncAddonsResource:
    def __init__(self, http: AsyncCommetHTTPClient) -> None:
        self._http = http

    async def list_active(self, *, customer_id: str) -> AddonsListActiveResult:
        """List all active add-ons for a customer's subscription."""
        query = build_body(customer_id=customer_id)
        return _parse_data(await self._http.get("/active-addons", query), AddonsListActiveResult)

    async def get(self, id: str) -> Addon:
        """Retrieve an add-on by its public ID or slug."""
        return _parse_data(await self._http.get(f"/addons/{id}"), Addon)

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
    ) -> Addon:
        """Update an add-on's name, description, or pricing."""
        body = build_body(
            name=name,
            description=description,
            base_price=base_price,
            included_units=included_units,
            overage_rate=overage_rate,
        )
        return _parse_data(
            await self._http.patch(f"/addons/{id}", body, idempotency_key=idempotency_key), Addon
        )

    async def delete(self, id: str) -> DeletedObject:
        """Soft-delete an add-on. Fails if the add-on has active subscriptions."""
        return _parse_data(await self._http.delete(f"/addons/{id}"), DeletedObject)

    async def list(
        self, *, cursor: str | None = None, limit: int | None = None
    ) -> AddonsListResult:
        """List all add-ons with cursor-based pagination."""
        query = build_body(cursor=cursor, limit=limit)
        return _parse_data(await self._http.get("/addons", query), AddonsListResult)

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
    ) -> Addon:
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
        return _parse_data(
            await self._http.post("/addons", body, idempotency_key=idempotency_key), Addon
        )
