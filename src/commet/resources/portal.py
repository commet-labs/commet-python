# ruff: noqa: E501

from __future__ import annotations

from .._http import CommetHTTPClient
from .._shared import build_body
from ..types import (
    PortalAccess,
    _parse_data,
)


class PortalResource:
    def __init__(self, http: CommetHTTPClient) -> None:
        self._http = http

    def get_url(
        self,
        *,
        email: str | None = None,
        return_url: str | None = None,
        customer_id: str | None = None,
        idempotency_key: str | None = None,
    ) -> PortalAccess:
        """Generate a customer portal URL. Exactly one identifier (email or customerId) is required."""
        body = build_body(email=email, return_url=return_url, customer_id=customer_id)
        return _parse_data(
            self._http.post("/portal/sessions", body, idempotency_key=idempotency_key), PortalAccess
        )
