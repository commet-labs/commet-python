from __future__ import annotations

from .._async_http import AsyncCommetHTTPClient
from .._http import ApiResponse
from .._resource_mixins import (
    parse_plan_group,
    parse_plan_group_detail,
    parse_plan_group_list,
)
from .._shared import build_body
from ..types import PlanGroup, PlanGroupDetail


class AsyncPlanGroupsResource:
    def __init__(self, http: AsyncCommetHTTPClient) -> None:
        self._http = http

    async def list(
        self,
        *,
        limit: int | None = None,
        cursor: str | None = None,
    ) -> ApiResponse[list[PlanGroup]]:
        return parse_plan_group_list(
            await self._http.get("/plan-groups", build_body(limit=limit, cursor=cursor))
        )

    async def get(self, plan_group_id: str) -> ApiResponse[PlanGroupDetail]:
        return parse_plan_group_detail(await self._http.get(f"/plan-groups/{plan_group_id}"))

    async def create(
        self,
        *,
        name: str,
        description: str | None = None,
        is_public: bool | None = None,
        idempotency_key: str | None = None,
    ) -> ApiResponse[PlanGroup]:
        return parse_plan_group(await self._http.post(
            "/plan-groups",
            build_body(name=name, description=description, is_public=is_public),
            idempotency_key=idempotency_key,
        ))

    async def update(
        self,
        plan_group_id: str,
        *,
        name: str | None = None,
        description: str | None = None,
        is_public: bool | None = None,
        idempotency_key: str | None = None,
    ) -> ApiResponse[PlanGroup]:
        return parse_plan_group(await self._http.put(
            f"/plan-groups/{plan_group_id}",
            build_body(name=name, description=description, is_public=is_public),
            idempotency_key=idempotency_key,
        ))

    async def delete(
        self,
        plan_group_id: str,
        *,
        idempotency_key: str | None = None,
    ) -> ApiResponse[None]:
        return await self._http.delete(
            f"/plan-groups/{plan_group_id}", idempotency_key=idempotency_key,
        )

    async def add_plan(
        self,
        plan_group_id: str,
        *,
        plan_id: str,
        sort_order: int | None = None,
        idempotency_key: str | None = None,
    ) -> ApiResponse[PlanGroupDetail]:
        return parse_plan_group_detail(await self._http.post(
            f"/plan-groups/{plan_group_id}/plans",
            build_body(plan_id=plan_id, sort_order=sort_order),
            idempotency_key=idempotency_key,
        ))

    async def remove_plan(
        self,
        plan_group_id: str,
        *,
        plan_id: str,
        idempotency_key: str | None = None,
    ) -> ApiResponse[None]:
        return await self._http.delete(
            f"/plan-groups/{plan_group_id}/plans/{plan_id}",
            idempotency_key=idempotency_key,
        )

    async def reorder_plans(
        self,
        plan_group_id: str,
        *,
        plan_ids: list[str],
        idempotency_key: str | None = None,
    ) -> ApiResponse[PlanGroupDetail]:
        return parse_plan_group_detail(await self._http.put(
            f"/plan-groups/{plan_group_id}/plans/reorder",
            build_body(plan_ids=plan_ids),
            idempotency_key=idempotency_key,
        ))
