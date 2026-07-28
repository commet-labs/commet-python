# ruff: noqa: E501

from __future__ import annotations

from .._http import CommetHTTPClient
from .._shared import build_body
from ..types import (
    CreditPack,
    CreditPacksListResult,
    DeletedObject,
    _parse_data,
)


class CreditPacksResource:
    def __init__(self, http: CommetHTTPClient) -> None:
        self._http = http

    def update(
        self,
        id: str,
        *,
        name: str | None = None,
        description: str | None = None,
        credits: int | None = None,
        price: int | None = None,
        is_active: bool | None = None,
        idempotency_key: str | None = None,
    ) -> CreditPack:
        """Update a credit pack's name, description, credits, price, or active status."""
        body = build_body(
            name=name, description=description, credits=credits, price=price, is_active=is_active
        )
        return _parse_data(
            self._http.patch(f"/credit-packs/{id}", body, idempotency_key=idempotency_key),
            CreditPack,
        )

    def delete(self, id: str) -> DeletedObject:
        """Soft-delete a credit pack."""
        return _parse_data(self._http.delete(f"/credit-packs/{id}"), DeletedObject)

    def list(self) -> CreditPacksListResult:
        """List all active credit packs."""
        return _parse_data(self._http.get("/credit-packs"), CreditPacksListResult)

    def create(
        self,
        *,
        name: str,
        credits: int,
        price: int,
        description: str | None = None,
        is_active: bool | None = None,
        idempotency_key: str | None = None,
    ) -> CreditPack:
        """Create a new credit pack."""
        body = build_body(
            name=name, description=description, credits=credits, price=price, is_active=is_active
        )
        return _parse_data(
            self._http.post("/credit-packs", body, idempotency_key=idempotency_key), CreditPack
        )
