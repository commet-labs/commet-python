from __future__ import annotations

from .._async_http import AsyncCommetHTTPClient
from .._http import ApiResponse
from .._resource_mixins import (
    parse_can_use_result,
    parse_delete_result,
    parse_feature_access,
    parse_feature_access_list,
    parse_feature_manage,
)
from .._shared import build_body
from ..types import CanUseResult, DeleteResult, FeatureAccess, FeatureManage


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

    async def can_use(
        self,
        *,
        code: str,
        customer_id: str,
    ) -> ApiResponse[CanUseResult]:
        return parse_can_use_result(await self._http.get(
            f"/features/{code}", {"customer_id": customer_id, "action": "canUse"}
        ))

    async def list(self, customer_id: str) -> ApiResponse[list[FeatureAccess]]:
        return parse_feature_access_list(
            await self._http.get("/features", {"customer_id": customer_id})
        )

    async def create(
        self,
        *,
        code: str,
        name: str,
        type: str,
        description: str | None = None,
        unit_name: str | None = None,
        idempotency_key: str | None = None,
    ) -> ApiResponse[FeatureManage]:
        return parse_feature_manage(await self._http.post(
            "/features/manage",
            build_body(code=code, name=name, type=type, description=description, unit_name=unit_name),
            idempotency_key=idempotency_key,
        ))

    async def update(
        self,
        code: str,
        *,
        name: str | None = None,
        description: str | None = None,
        unit_name: str | None = None,
        idempotency_key: str | None = None,
    ) -> ApiResponse[FeatureManage]:
        return parse_feature_manage(await self._http.put(
            f"/features/{code}/manage",
            build_body(name=name, description=description, unit_name=unit_name),
            idempotency_key=idempotency_key,
        ))

    async def delete(
        self,
        code: str,
        *,
        idempotency_key: str | None = None,
    ) -> ApiResponse[DeleteResult]:
        return parse_delete_result(await self._http.delete(
            f"/features/{code}/manage", idempotency_key=idempotency_key,
        ))
