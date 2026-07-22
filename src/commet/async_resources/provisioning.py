# ruff: noqa: E501

from __future__ import annotations

from .._async_http import AsyncCommetHTTPClient
from .._http import ApiResponse
from ..types import (
    ClaimLink,
    _parse,
)


class AsyncProvisioningResource:
    def __init__(self, http: AsyncCommetHTTPClient) -> None:
        self._http = http

    async def create_claim_link(
        self, *, idempotency_key: str | None = None
    ) -> ApiResponse[ClaimLink]:
        """Issue a fresh claim link for an organization that was provisioned headlessly and has not been claimed yet. Any previously issued link stops working."""
        return _parse(
            await self._http.post("/claim-link", idempotency_key=idempotency_key), ClaimLink
        )
