# ruff: noqa: E501

from __future__ import annotations

from .._http import CommetHTTPClient
from .._shared import build_body
from ..types import (
    FeatureAccess,
    FeatureAccessListResult,
    _parse_data,
    _parse_union_data,
)


class FeatureAccessResource:
    def __init__(self, http: CommetHTTPClient) -> None:
        self._http = http

    def get(self, code: str, *, customer_id: str) -> FeatureAccess:
        """Get one feature's access and current usage for a customer. To evaluate a prospective consumption, use POST /usage/check."""
        query = build_body(customer_id=customer_id)
        return _parse_union_data(self._http.get(f"/feature-access/{code}", query), "FeatureAccess")

    def list(self, *, customer_id: str) -> FeatureAccessListResult:
        """List a customer's feature access and current usage."""
        query = build_body(customer_id=customer_id)
        return _parse_data(self._http.get("/feature-access", query), FeatureAccessListResult)
