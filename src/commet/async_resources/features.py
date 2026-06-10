# ruff: noqa: E501

from __future__ import annotations

from .._async_http import AsyncCommetHTTPClient
from .._http import ApiResponse
from .._shared import build_body
from ..types import (
    DeletedObject,
    Feature,
    FeatureType,
    _parse,
    _parse_list,
)


class AsyncFeaturesResource:
    def __init__(self, http: AsyncCommetHTTPClient) -> None:
        self._http = http

    async def list(self) -> ApiResponse[list[Feature]]:
        """List every feature defined in the organization. This is the organization's feature catalog (definitions), not a customer's feature access."""
        return _parse_list(await self._http.get("/features"), Feature)

    async def get(self, code: str) -> ApiResponse[Feature]:
        """Get a single feature definition by code from the organization's feature catalog."""
        return _parse(await self._http.get(f"/features/{code}"), Feature)

    async def create(
        self,
        *,
        name: str,
        code: str,
        type: FeatureType,
        description: str | None = None,
        unit_name: str | None = None,
        idempotency_key: str | None = None,
    ) -> ApiResponse[Feature]:
        """Create a new feature. Code must be lowercase alphanumeric with underscores."""
        body = build_body(
            name=name, code=code, type=type, description=description, unit_name=unit_name
        )
        return _parse(
            await self._http.post("/features/manage", body, idempotency_key=idempotency_key),
            Feature,
        )

    async def update(
        self,
        code: str,
        *,
        name: str | None = None,
        description: str | None = None,
        unit_name: str | None = None,
        idempotency_key: str | None = None,
    ) -> ApiResponse[Feature]:
        """Update a feature's name, description, or unit name. At least one field must be provided."""
        body = build_body(name=name, description=description, unit_name=unit_name)
        return _parse(
            await self._http.put(f"/features/{code}/manage", body, idempotency_key=idempotency_key),
            Feature,
        )

    async def delete(self, code: str) -> ApiResponse[DeletedObject]:
        """Delete a feature. Fails if the feature is attached to active plans or has an active add-on."""
        return _parse(await self._http.delete(f"/features/{code}/manage"), DeletedObject)
