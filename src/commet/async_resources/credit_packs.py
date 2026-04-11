from __future__ import annotations

from .._async_http import AsyncCommetHTTPClient
from .._http import ApiResponse
from .._resource_mixins import parse_credit_pack_list
from ..types import CreditPack


class AsyncCreditPacksResource:
    def __init__(self, http: AsyncCommetHTTPClient) -> None:
        self._http = http

    async def list(self) -> ApiResponse[list[CreditPack]]:
        return parse_credit_pack_list(await self._http.get("/credit-packs"))
