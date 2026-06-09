# ruff: noqa: E501

from __future__ import annotations

from .._async_http import AsyncCommetHTTPClient
from .._http import ApiResponse
from .._shared import build_body
from ..types import (
    PortalAccess,
    _parse,
)


class AsyncPortalResource:
    def __init__(self, http: AsyncCommetHTTPClient) -> None:
        self._http = http

    async def get_url(
        self,
        *,
        email: str | None = None,
        customer_id: str | None = None,
        idempotency_key: str | None = None,
    ) -> ApiResponse[PortalAccess]:
        """Generate a customer portal URL. Exactly one identifier (email or customerId) is required."""
        body = build_body(email=email, customer_id=customer_id)
        return _parse(
            await self._http.post("/portal/request-access", body, idempotency_key=idempotency_key),
            PortalAccess,
        )
