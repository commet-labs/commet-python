from __future__ import annotations

from .._async_http import AsyncCommetHTTPClient
from .._http import ApiResponse
from .._resource_mixins import parse_feature_access, parse_feature_access_list, parse_feature_check
from ..types import FeatureAccess


class AsyncFeaturesResource:
    def __init__(self, http: AsyncCommetHTTPClient) -> None:
        self._http = http

    async def get(
        self,
        *,
        code: str,
        customer_id: str,
    ) -> ApiResponse[FeatureAccess]:
        return parse_feature_access(
            await self._http.get(f"/features/{code}", {"customer_id": customer_id})
        )

    async def check(
        self,
        *,
        code: str,
        customer_id: str,
    ) -> ApiResponse[dict[str, bool]]:
        return parse_feature_check(
            await self._http.get(f"/features/{code}", {"customer_id": customer_id})
        )

    async def can_use(
        self,
        *,
        code: str,
        customer_id: str,
    ) -> ApiResponse[dict[str, bool | str | None]]:
        return await self._http.get(
            f"/features/{code}", {"customer_id": customer_id, "action": "canUse"}
        )

    async def list(self, customer_id: str) -> ApiResponse[list[FeatureAccess]]:
        return parse_feature_access_list(
            await self._http.get("/features", {"customer_id": customer_id})
        )
