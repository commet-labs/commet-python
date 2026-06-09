# ruff: noqa: E501

from __future__ import annotations

import builtins

from .._http import ApiResponse, CommetHTTPClient
from .._shared import build_body
from ..types import (
    AddedPlanToGroup,
    DeletedObject,
    PlanGroup,
    RemovedPlanFromGroup,
    ReorderedPlans,
    _parse,
    _parse_list,
)


class PlanGroupsResource:
    def __init__(self, http: CommetHTTPClient) -> None:
        self._http = http

    def list(
        self, *, limit: int | None = None, cursor: str | None = None
    ) -> ApiResponse[list[PlanGroup]]:
        """List plan groups with cursor-based pagination."""
        query = build_body(limit=limit, cursor=cursor)
        return _parse_list(self._http.get("/plan-groups", query), PlanGroup)

    def get(self, id: str) -> ApiResponse[PlanGroup]:
        """Retrieve a plan group by ID, including its plans ordered by sortOrder."""
        return _parse(self._http.get(f"/plan-groups/{id}"), PlanGroup)

    def create(
        self,
        *,
        name: str,
        description: str | None = None,
        is_public: bool | None = None,
        idempotency_key: str | None = None,
    ) -> ApiResponse[PlanGroup]:
        """Create a new plan group for organizing plans."""
        body = build_body(name=name, description=description, is_public=is_public)
        return _parse(
            self._http.post("/plan-groups", body, idempotency_key=idempotency_key), PlanGroup
        )

    def update(
        self,
        id: str,
        *,
        name: str | None = None,
        description: str | None = None,
        is_public: bool | None = None,
        idempotency_key: str | None = None,
    ) -> ApiResponse[PlanGroup]:
        """Update a plan group's name, description, or visibility."""
        body = build_body(name=name, description=description, is_public=is_public)
        return _parse(
            self._http.put(f"/plan-groups/{id}", body, idempotency_key=idempotency_key), PlanGroup
        )

    def delete(self, id: str) -> ApiResponse[DeletedObject]:
        """Delete a plan group. Plans in the group are unlinked, not deleted."""
        return _parse(self._http.delete(f"/plan-groups/{id}"), DeletedObject)

    def add_plan(
        self,
        id: str,
        *,
        plan_id: str,
        sort_order: int | None = None,
        idempotency_key: str | None = None,
    ) -> ApiResponse[AddedPlanToGroup]:
        """Add an existing plan to a plan group with optional sort order."""
        body = build_body(plan_id=plan_id, sort_order=sort_order)
        return _parse(
            self._http.post(f"/plan-groups/{id}/plans", body, idempotency_key=idempotency_key),
            AddedPlanToGroup,
        )

    def remove_plan(self, id: str, plan_id: str) -> ApiResponse[RemovedPlanFromGroup]:
        """Remove a plan from a plan group."""
        return _parse(self._http.delete(f"/plan-groups/{id}/plans/{plan_id}"), RemovedPlanFromGroup)

    def reorder_plans(
        self, id: str, *, plan_ids: builtins.list[str], idempotency_key: str | None = None
    ) -> ApiResponse[ReorderedPlans]:
        """Set the display order of plans within a group. All plan IDs in the group must be provided."""
        body = build_body(plan_ids=plan_ids)
        return _parse(
            self._http.put(
                f"/plan-groups/{id}/plans/reorder", body, idempotency_key=idempotency_key
            ),
            ReorderedPlans,
        )
