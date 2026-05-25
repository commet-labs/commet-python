from __future__ import annotations

from typing import Any

from .._async_http import AsyncCommetHTTPClient
from .._http import ApiResponse


class AsyncAddonsResource:
    def __init__(self, http: AsyncCommetHTTPClient) -> None:
        self._http = http

    async def get_active(self, customer_id: str) -> ApiResponse[list[dict[str, Any]]]:
        return await self._http.get("/addons/active", {"customer_id": customer_id})
