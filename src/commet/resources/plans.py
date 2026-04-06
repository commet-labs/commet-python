from __future__ import annotations

from .._http import ApiResponse, CommetHTTPClient, build_body


class PlansResource:
    def __init__(self, http: CommetHTTPClient) -> None:
        self._http = http

    def list(
        self,
        *,
        include_private: bool | None = None,
        limit: int | None = None,
        cursor: str | None = None,
    ) -> ApiResponse:
        return self._http.get("/plans", build_body(
            include_private=include_private, limit=limit, cursor=cursor
        ))

    def get(self, plan_code: str) -> ApiResponse:
        return self._http.get(f"/plans/{plan_code}")
