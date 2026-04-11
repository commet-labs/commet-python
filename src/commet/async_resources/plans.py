from __future__ import annotations

from .._async_http import AsyncCommetHTTPClient
from .._http import ApiResponse
from .._resource_mixins import parse_plan, parse_plan_list
from .._shared import build_body
from ..types import Plan


class AsyncPlansResource:
    def __init__(self, http: AsyncCommetHTTPClient) -> None:
        self._http = http

    async def list(
        self,
        *,
        include_private: bool | None = None,
        limit: int | None = None,
        cursor: str | None = None,
    ) -> ApiResponse[list[Plan]]:
        return parse_plan_list(await self._http.get("/plans", build_body(
            include_private=include_private, limit=limit, cursor=cursor
        )))

    async def get(self, plan_code: str) -> ApiResponse[Plan]:
        return parse_plan(await self._http.get(f"/plans/{plan_code}"))
