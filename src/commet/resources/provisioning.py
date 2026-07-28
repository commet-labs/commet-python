# ruff: noqa: E501

from __future__ import annotations

from .._http import CommetHTTPClient
from ..types import (
    ClaimLink,
    _parse_data,
)


class ProvisioningResource:
    def __init__(self, http: CommetHTTPClient) -> None:
        self._http = http

    def create_claim_link(self, *, idempotency_key: str | None = None) -> ClaimLink:
        """Issue a fresh claim link for an organization that was provisioned headlessly and has not been claimed yet. Any previously issued link stops working."""
        return _parse_data(
            self._http.post("/claim-link", idempotency_key=idempotency_key), ClaimLink
        )
