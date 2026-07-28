# ruff: noqa: E501

from __future__ import annotations

from typing import Literal

from .._async_http import AsyncCommetHTTPClient
from .._shared import build_body
from ..types import (
    DeletedObject,
    Feature,
    FeaturesListResult,
    _parse_data,
)


class AsyncFeaturesResource:
    def __init__(self, http: AsyncCommetHTTPClient) -> None:
        self._http = http

    async def get(self, code: str) -> Feature:
        """Get a single feature definition by code from the organization's feature catalog."""
        return _parse_data(await self._http.get(f"/features/{code}"), Feature)

    async def update(
        self,
        code: str,
        *,
        name: str | None = None,
        description: str | None = None,
        unit_name: str | None = None,
        idempotency_key: str | None = None,
    ) -> Feature:
        """Update a feature's name, description, or unit name. At least one field must be provided."""
        body = build_body(name=name, description=description, unit_name=unit_name)
        return _parse_data(
            await self._http.patch(f"/features/{code}", body, idempotency_key=idempotency_key),
            Feature,
        )

    async def delete(self, code: str) -> DeletedObject:
        """Delete a feature. Fails if the feature is attached to active plans or has an active add-on."""
        return _parse_data(await self._http.delete(f"/features/{code}"), DeletedObject)

    async def list(self) -> FeaturesListResult:
        """List every feature defined in the organization. This is the organization's feature catalog (definitions), not a customer's feature access."""
        return _parse_data(await self._http.get("/features"), FeaturesListResult)

    async def create(
        self,
        *,
        name: str,
        code: str,
        type: Literal["boolean", "usage", "seats", "quota"],
        description: str | None = None,
        unit_name: str | None = None,
        idempotency_key: str | None = None,
    ) -> Feature:
        """Create a new feature. Code must be lowercase alphanumeric with underscores."""
        body = build_body(
            name=name, code=code, type=type, description=description, unit_name=unit_name
        )
        return _parse_data(
            await self._http.post("/features", body, idempotency_key=idempotency_key), Feature
        )
