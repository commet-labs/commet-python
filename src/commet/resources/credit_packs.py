# ruff: noqa: E501

from __future__ import annotations

from .._http import ApiResponse, CommetHTTPClient
from .._shared import build_body
from ..types import (
    CreditPack,
    DeletedObject,
    _parse,
    _parse_list,
)


class CreditPacksResource:
    def __init__(self, http: CommetHTTPClient) -> None:
        self._http = http

    def list(self) -> ApiResponse[list[CreditPack]]:
        """List all active credit packs."""
        return _parse_list(self._http.get("/credit-packs"), CreditPack)

    def create(
        self,
        *,
        name: str,
        credits: int,
        price: int,
        description: str | None = None,
        is_active: bool | None = None,
        idempotency_key: str | None = None,
    ) -> ApiResponse[CreditPack]:
        """Create a new credit pack."""
        body = build_body(
            name=name, description=description, credits=credits, price=price, is_active=is_active
        )
        return _parse(
            self._http.post("/credit-packs/manage", body, idempotency_key=idempotency_key),
            CreditPack,
        )

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
    ) -> ApiResponse[CreditPack]:
        """Update a credit pack's name, description, credits, price, or active status."""
        body = build_body(
            name=name, description=description, credits=credits, price=price, is_active=is_active
        )
        return _parse(
            self._http.put(f"/credit-packs/{id}", body, idempotency_key=idempotency_key), CreditPack
        )

    def delete(self, id: str) -> ApiResponse[DeletedObject]:
        """Soft-delete a credit pack."""
        return _parse(self._http.delete(f"/credit-packs/{id}"), DeletedObject)
