from __future__ import annotations

from .._async_http import AsyncCommetHTTPClient
from .._http import ApiResponse
from .._resource_mixins import parse_portal_session
from .._shared import build_body
from ..types import PortalSession


class AsyncPortalResource:
    def __init__(self, http: AsyncCommetHTTPClient) -> None:
        self._http = http

    async def get_url(
        self,
        *,
        customer_id: str | None = None,
        email: str | None = None,
        idempotency_key: str | None = None,
    ) -> ApiResponse[PortalSession]:
        return parse_portal_session(await self._http.post(
            "/portal/request-access",
            build_body(customer_id=customer_id, email=email),
            idempotency_key=idempotency_key,
        ))
