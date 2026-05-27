from __future__ import annotations

from typing import Any

from .._http import ApiResponse, CommetHTTPClient
from .._shared import build_body


class PlanGroupsResource:
    def __init__(self, http: CommetHTTPClient) -> None:
        self._http = http

    def list(
        self,
        *,
        limit: int | None = None,
        cursor: str | None = None,
    ) -> ApiResponse[Any]:
        return self._http.get("/plan-groups", build_body(limit=limit, cursor=cursor))

    def get(self, plan_group_id: str) -> ApiResponse[Any]:
        return self._http.get(f"/plan-groups/{plan_group_id}")

    def create(
        self,
        *,
        name: str,
        description: str | None = None,
        is_public: bool | None = None,
        idempotency_key: str | None = None,
    ) -> ApiResponse[Any]:
        return self._http.post(
            "/plan-groups",
            build_body(name=name, description=description, is_public=is_public),
            idempotency_key=idempotency_key,
        )

    def update(
        self,
        plan_group_id: str,
        *,
        name: str | None = None,
        description: str | None = None,
        is_public: bool | None = None,
        idempotency_key: str | None = None,
    ) -> ApiResponse[Any]:
        return self._http.put(
            f"/plan-groups/{plan_group_id}",
            build_body(name=name, description=description, is_public=is_public),
            idempotency_key=idempotency_key,
        )

    def delete(
        self,
        plan_group_id: str,
        *,
        idempotency_key: str | None = None,
    ) -> ApiResponse[Any]:
        return self._http.delete(
            f"/plan-groups/{plan_group_id}", idempotency_key=idempotency_key,
        )

    def add_plan(
        self,
        plan_group_id: str,
        *,
        plan_id: str,
        sort_order: int | None = None,
        idempotency_key: str | None = None,
    ) -> ApiResponse[Any]:
        return self._http.post(
            f"/plan-groups/{plan_group_id}/plans",
            build_body(plan_id=plan_id, sort_order=sort_order),
            idempotency_key=idempotency_key,
        )

    def remove_plan(
        self,
        plan_group_id: str,
        *,
        plan_id: str,
        idempotency_key: str | None = None,
    ) -> ApiResponse[Any]:
        return self._http.delete(
            f"/plan-groups/{plan_group_id}/plans/{plan_id}",
            idempotency_key=idempotency_key,
        )

    def reorder_plans(
        self,
        plan_group_id: str,
        *,
        plan_ids: list[str],
        idempotency_key: str | None = None,
    ) -> ApiResponse[Any]:
        return self._http.put(
            f"/plan-groups/{plan_group_id}/plans/reorder",
            build_body(plan_ids=plan_ids),
            idempotency_key=idempotency_key,
        )
