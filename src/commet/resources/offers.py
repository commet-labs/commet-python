# ruff: noqa: E501

from __future__ import annotations

import builtins
from typing import Any

from .._http import CommetHTTPClient
from .._shared import build_body
from ..types import (
    CreateOfferParamsPhasesItem,
    DeletedOffer,
    Offer,
    OffersListResult,
    UpdateOfferParamsPhasesItem,
    _parse_data,
)


class OffersResource:
    def __init__(self, http: CommetHTTPClient) -> None:
        self._http = http

    def get(self, id: str) -> Offer:
        """Retrieve reusable offer terms by public ID."""
        return _parse_data(self._http.get(f"/offers/{id}"), Offer)

    def update(
        self,
        id: str,
        *,
        name: str,
        phases: builtins.list[UpdateOfferParamsPhasesItem],
        metadata: dict[str, Any] | None = None,
        starts_at: str | None = None,
        ends_at: str | None = None,
        active: bool | None = None,
        idempotency_key: str | None = None,
    ) -> Offer:
        """Replace reusable offer terms. Existing applications keep their immutable accepted terms."""
        body = build_body(
            name=name,
            phases=phases,
            metadata=metadata,
            starts_at=starts_at,
            ends_at=ends_at,
            active=active,
        )
        return _parse_data(
            self._http.patch(f"/offers/{id}", body, idempotency_key=idempotency_key), Offer
        )

    def delete(self, id: str) -> DeletedOffer:
        """Soft-delete an Offer. Existing applications and their accepted terms remain available for billing and audit."""
        return _parse_data(self._http.delete(f"/offers/{id}"), DeletedOffer)

    def list(
        self, *, cursor: str | None = None, limit: int | None = None, active: bool | None = None
    ) -> OffersListResult:
        """List reusable offer terms. Offers are independent from plans, prices, eligibility, and distribution channels."""
        query = build_body(cursor=cursor, limit=limit, active=active)
        return _parse_data(self._http.get("/offers", query), OffersListResult)

    def create(
        self,
        *,
        name: str,
        phases: builtins.list[CreateOfferParamsPhasesItem],
        metadata: dict[str, Any] | None = None,
        starts_at: str | None = None,
        ends_at: str | None = None,
        active: bool | None = None,
        idempotency_key: str | None = None,
    ) -> Offer:
        """Create reusable offer terms without assigning a plan, price, eligibility rule, or distribution channel."""
        body = build_body(
            name=name,
            phases=phases,
            metadata=metadata,
            starts_at=starts_at,
            ends_at=ends_at,
            active=active,
        )
        return _parse_data(self._http.post("/offers", body, idempotency_key=idempotency_key), Offer)
