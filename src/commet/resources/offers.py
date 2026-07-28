# ruff: noqa: E501

from __future__ import annotations

import builtins
from typing import Any, Literal

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
        """Retrieve a canonical offer by its public ID."""
        return _parse_data(self._http.get(f"/offers/{id}"), Offer)

    def update(
        self,
        id: str,
        *,
        name: str,
        purpose: Literal["introductory", "promotional"],
        plan_price_ids: builtins.list[str],
        phases: builtins.list[UpdateOfferParamsPhasesItem],
        metadata: dict[str, Any] | None = None,
        starts_at: str | None = None,
        ends_at: str | None = None,
        active: bool | None = None,
        idempotency_key: str | None = None,
    ) -> Offer:
        """Replace an offer's catalog definition. Existing offer applications keep their immutable accepted terms."""
        body = build_body(
            name=name,
            purpose=purpose,
            plan_price_ids=plan_price_ids,
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
        """Soft-delete an offer. Existing applications and their accepted terms remain available for billing and audit."""
        return _parse_data(self._http.delete(f"/offers/{id}"), DeletedOffer)

    def list(
        self,
        *,
        cursor: str | None = None,
        limit: int | None = None,
        plan_price_id: str | None = None,
        purpose: Literal["introductory", "promotional"] | None = None,
        active: bool | None = None,
    ) -> OffersListResult:
        """List the organization's canonical introductory and promotional offers."""
        query = build_body(
            cursor=cursor, limit=limit, plan_price_id=plan_price_id, purpose=purpose, active=active
        )
        return _parse_data(self._http.get("/offers", query), OffersListResult)

    def create(
        self,
        *,
        name: str,
        purpose: Literal["introductory", "promotional"],
        plan_price_ids: builtins.list[str],
        phases: builtins.list[CreateOfferParamsPhasesItem],
        metadata: dict[str, Any] | None = None,
        starts_at: str | None = None,
        ends_at: str | None = None,
        active: bool | None = None,
        idempotency_key: str | None = None,
    ) -> Offer:
        """Create a canonical offer scoped to one or more plan prices. Currency-specific phases require an explicit USD value and never fall back across currencies."""
        body = build_body(
            name=name,
            purpose=purpose,
            plan_price_ids=plan_price_ids,
            phases=phases,
            metadata=metadata,
            starts_at=starts_at,
            ends_at=ends_at,
            active=active,
        )
        return _parse_data(self._http.post("/offers", body, idempotency_key=idempotency_key), Offer)
