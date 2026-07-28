# ruff: noqa: E501

from __future__ import annotations

from .._http import CommetHTTPClient
from .._shared import build_body
from ..types import (
    QuotaGetAllResult,
    UsageQuota,
    UsageQuotaEvent,
    _parse_data,
)


class QuotaResource:
    def __init__(self, http: CommetHTTPClient) -> None:
        self._http = http

    def get_all(self, *, customer_id: str) -> QuotaGetAllResult:
        """Get all quota allowances for a customer across every quota feature in their plan."""
        query = build_body(customer_id=customer_id)
        return _parse_data(self._http.get("/usage/quota/all", query), QuotaGetAllResult)

    def remove(
        self,
        *,
        feature_code: str,
        count: int | None = None,
        customer_id: str | None = None,
        external_id: str | None = None,
        idempotency_key: str | None = None,
    ) -> UsageQuotaEvent:
        """Remove from a customer's quota allowance for a feature. Defaults to 1 if count is omitted. Returns 400 insufficient_balance if the balance would go negative."""
        body = build_body(
            feature_code=feature_code, count=count, customer_id=customer_id, external_id=external_id
        )
        return _parse_data(
            self._http.post("/usage/quota/remove", body, idempotency_key=idempotency_key),
            UsageQuotaEvent,
        )

    def get(self, *, customer_id: str, feature_code: str) -> UsageQuota:
        """Get the current quota allowance (used vs included) for a specific feature."""
        query = build_body(customer_id=customer_id, feature_code=feature_code)
        return _parse_data(self._http.get("/usage/quota", query), UsageQuota)

    def add(
        self,
        *,
        feature_code: str,
        count: int | None = None,
        customer_id: str | None = None,
        external_id: str | None = None,
        idempotency_key: str | None = None,
    ) -> UsageQuotaEvent:
        """Add to a customer's quota allowance for a feature. Defaults to 1 if count is omitted."""
        body = build_body(
            feature_code=feature_code, count=count, customer_id=customer_id, external_id=external_id
        )
        return _parse_data(
            self._http.post("/usage/quota", body, idempotency_key=idempotency_key), UsageQuotaEvent
        )

    def set(
        self,
        *,
        feature_code: str,
        count: int,
        customer_id: str | None = None,
        external_id: str | None = None,
        idempotency_key: str | None = None,
    ) -> UsageQuotaEvent:
        """Set a customer's quota allowance for a feature to an exact value."""
        body = build_body(
            feature_code=feature_code, count=count, customer_id=customer_id, external_id=external_id
        )
        return _parse_data(
            self._http.put("/usage/quota", body, idempotency_key=idempotency_key), UsageQuotaEvent
        )
