from __future__ import annotations

from .._http import ApiResponse, CommetHTTPClient
from .._resource_mixins import (
    parse_active_addon_list,
    parse_addon,
    parse_addon_list,
    parse_delete_result,
)
from .._shared import build_body
from ..types import ActiveAddon, Addon, AddonConsumptionModel, DeleteResult


class AddonsResource:
    def __init__(self, http: CommetHTTPClient) -> None:
        self._http = http

    def list_active(self, customer_id: str) -> ApiResponse[list[ActiveAddon]]:
        return parse_active_addon_list(
            self._http.get("/addons/active", {"customer_id": customer_id})
        )

    def get_active(self, customer_id: str) -> ApiResponse[list[ActiveAddon]]:
        """.. deprecated:: use :meth:`list_active` instead."""
        return self.list_active(customer_id)

    def list(
        self,
        *,
        limit: int | None = None,
        cursor: str | None = None,
    ) -> ApiResponse[list[Addon]]:
        return parse_addon_list(
            self._http.get("/addons", build_body(limit=limit, cursor=cursor))
        )

    def get(self, addon_id: str) -> ApiResponse[Addon]:
        return parse_addon(self._http.get(f"/addons/{addon_id}"))

    def create(
        self,
        *,
        name: str,
        base_price: int,
        feature_id: str,
        consumption_model: AddonConsumptionModel,
        description: str | None = None,
        included_units: int | None = None,
        overage_rate: int | None = None,
        credit_cost: int | None = None,
        idempotency_key: str | None = None,
    ) -> ApiResponse[Addon]:
        return parse_addon(self._http.post(
            "/addons",
            build_body(
                name=name, base_price=base_price, feature_id=feature_id,
                consumption_model=consumption_model, description=description,
                included_units=included_units, overage_rate=overage_rate,
                credit_cost=credit_cost,
            ),
            idempotency_key=idempotency_key,
        ))

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
    ) -> ApiResponse[Addon]:
        return parse_addon(self._http.put(
            f"/addons/{addon_id}",
            build_body(
                name=name, description=description, base_price=base_price,
                included_units=included_units, overage_rate=overage_rate,
            ),
            idempotency_key=idempotency_key,
        ))

    def delete(
        self,
        addon_id: str,
        *,
        idempotency_key: str | None = None,
    ) -> ApiResponse[DeleteResult]:
        return parse_delete_result(
            self._http.delete(f"/addons/{addon_id}", idempotency_key=idempotency_key)
        )
