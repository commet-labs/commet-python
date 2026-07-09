# ruff: noqa: E501

from __future__ import annotations

from .._http import ApiResponse, CommetHTTPClient
from .._shared import build_body
from ..types import (
    PortalAccess,
    _parse,
)


class PortalResource:
    def __init__(self, http: CommetHTTPClient) -> None:
        self._http = http

    def get_url(
        self,
        *,
        email: str | None = None,
        customer_id: str | None = None,
        return_url: str | None = None,
        idempotency_key: str | None = None,
    ) -> ApiResponse[PortalAccess]:
        """Generate a customer portal URL. Exactly one identifier (email or customerId) is required."""
        body = build_body(email=email, customer_id=customer_id, return_url=return_url)
        return _parse(
            self._http.post("/portal/request-access", body, idempotency_key=idempotency_key),
            PortalAccess,
        )
