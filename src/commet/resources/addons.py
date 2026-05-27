from __future__ import annotations

from typing import Any

from .._http import ApiResponse, CommetHTTPClient
from .._shared import build_body


class AddonsResource:
    def __init__(self, http: CommetHTTPClient) -> None:
        self._http = http

    def get_active(self, customer_id: str) -> ApiResponse[list[dict[str, Any]]]:
        return self._http.get("/addons/active", {"customer_id": customer_id})

    def list(
        self,
        *,
        limit: int | None = None,
        cursor: str | None = None,
    ) -> ApiResponse[Any]:
        return self._http.get("/addons", build_body(limit=limit, cursor=cursor))

    def get(self, addon_id: str) -> ApiResponse[Any]:
        return self._http.get(f"/addons/{addon_id}")

    def create(
        self,
        *,
        name: str,
        base_price: int,
        feature_id: str,
        consumption_model: str,
        description: str | None = None,
        included_units: int | None = None,
        overage_rate: int | None = None,
        credit_cost: int | None = None,
        idempotency_key: str | None = None,
    ) -> ApiResponse[Any]:
        return self._http.post(
            "/addons",
            build_body(
                name=name, base_price=base_price, feature_id=feature_id,
                consumption_model=consumption_model, description=description,
                included_units=included_units, overage_rate=overage_rate,
                credit_cost=credit_cost,
            ),
            idempotency_key=idempotency_key,
        )

    def update(
        self,
        addon_id: str,
        *,
        name: str | None = None,
        description: str | None = None,
        base_price: int | None = None,
        included_units: int | None = None,
        overage_rate: int | None = None,
        idempotency_key: str | None = None,
    ) -> ApiResponse[Any]:
        return self._http.put(
            f"/addons/{addon_id}",
            build_body(
                name=name, description=description, base_price=base_price,
                included_units=included_units, overage_rate=overage_rate,
            ),
            idempotency_key=idempotency_key,
        )

    def delete(
        self,
        addon_id: str,
        *,
        idempotency_key: str | None = None,
    ) -> ApiResponse[Any]:
        return self._http.delete(f"/addons/{addon_id}", idempotency_key=idempotency_key)
