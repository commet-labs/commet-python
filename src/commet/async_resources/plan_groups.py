# ruff: noqa: E501

from __future__ import annotations

import builtins

from .._async_http import AsyncCommetHTTPClient
from .._shared import build_body
from ..types import (
    AddedPlanToGroup,
    DeletedObject,
    PlanGroup,
    PlanGroupDetail,
    PlanGroupsListResult,
    RemovedPlanFromGroup,
    ReorderedPlans,
    _parse_data,
)


class AsyncPlanGroupsResource:
    def __init__(self, http: AsyncCommetHTTPClient) -> None:
        self._http = http

    async def remove_plan(self, id: str, plan_id: str) -> RemovedPlanFromGroup:
        """Remove a plan from a plan group."""
        return _parse_data(
            await self._http.delete(f"/plan-groups/{id}/plans/{plan_id}"), RemovedPlanFromGroup
        )

    async def reorder_plans(
        self, id: str, *, plan_ids: builtins.list[str], idempotency_key: str | None = None
    ) -> ReorderedPlans:
        """Set the display order of plans within a group. All plan IDs in the group must be provided."""
        body = build_body(plan_ids=plan_ids)
        return _parse_data(
            await self._http.put(
                f"/plan-groups/{id}/plans/reorder", body, idempotency_key=idempotency_key
            ),
            ReorderedPlans,
        )

    async def add_plan(
        self,
        id: str,
        *,
        plan_id: str,
        sort_order: int | None = None,
        idempotency_key: str | None = None,
    ) -> AddedPlanToGroup:
        """Add an existing plan to a plan group with optional sort order."""
        body = build_body(plan_id=plan_id, sort_order=sort_order)
        return _parse_data(
            await self._http.post(
                f"/plan-groups/{id}/plans", body, idempotency_key=idempotency_key
            ),
            AddedPlanToGroup,
        )

    async def get(self, id: str) -> PlanGroupDetail:
        """Retrieve a plan group by ID, including its plans ordered by sortOrder."""
        return _parse_data(await self._http.get(f"/plan-groups/{id}"), PlanGroupDetail)

    async def update(
        self,
        id: str,
        *,
        name: str | None = None,
        description: str | None = None,
        is_public: bool | None = None,
        idempotency_key: str | None = None,
    ) -> PlanGroup:
        """Update a plan group's name, description, or visibility."""
        body = build_body(name=name, description=description, is_public=is_public)
        return _parse_data(
            await self._http.patch(f"/plan-groups/{id}", body, idempotency_key=idempotency_key),
            PlanGroup,
        )

    async def delete(self, id: str) -> DeletedObject:
        """Delete a plan group. Plans in the group are unlinked, not deleted."""
        return _parse_data(await self._http.delete(f"/plan-groups/{id}"), DeletedObject)

    async def list(
        self, *, cursor: str | None = None, limit: int | None = None
    ) -> PlanGroupsListResult:
        """List plan groups with cursor-based pagination."""
        query = build_body(cursor=cursor, limit=limit)
        return _parse_data(await self._http.get("/plan-groups", query), PlanGroupsListResult)

    async def create(
        self,
        *,
        name: str,
        description: str | None = None,
        is_public: bool | None = None,
        idempotency_key: str | None = None,
    ) -> PlanGroup:
        """Create a new plan group for organizing plans."""
        body = build_body(name=name, description=description, is_public=is_public)
        return _parse_data(
            await self._http.post("/plan-groups", body, idempotency_key=idempotency_key), PlanGroup
        )
