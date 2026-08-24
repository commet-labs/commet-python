# ruff: noqa: E501

from __future__ import annotations

import builtins
from typing import Any, Literal

from .._async_http import AsyncCommetHTTPClient
from .._shared import build_body
from ..types import (
    BatchCreateCustomersParamsCustomersItem,
    CreateCustomerParamsAddress,
    Customer,
    CustomerBatch,
    CustomerCredit,
    CustomerCreditRevocation,
    CustomersListCreditsResult,
    CustomersListPlanGrantsResult,
    CustomersListResult,
    PlanGrant,
    Timezone,
    UpdateCustomerParamsAddress,
    _parse_data,
)


class AsyncCustomersResource:
    def __init__(self, http: AsyncCommetHTTPClient) -> None:
        self._http = http

    async def revoke_credit(
        self, id: str, credit_id: str, *, idempotency_key: str | None = None
    ) -> CustomerCreditRevocation:
        """Revoke the unallocated remainder of a customer credit grant. Applied invoice history is unchanged."""
        return _parse_data(
            await self._http.post(
                f"/customers/{id}/credits/{credit_id}/revoke", idempotency_key=idempotency_key
            ),
            CustomerCreditRevocation,
        )

    async def list_credits(self, id: str) -> CustomersListCreditsResult:
        """List currency-specific invoice credit grants and their remaining balances for a customer."""
        return _parse_data(
            await self._http.get(f"/customers/{id}/credits"), CustomersListCreditsResult
        )

    async def create_credit(
        self,
        id: str,
        *,
        amount: int,
        currency: Literal[
            "usd",
            "ars",
            "brl",
            "clp",
            "cop",
            "pen",
            "uyu",
            "pyg",
            "bob",
            "mxn",
            "cad",
            "eur",
            "gbp",
            "jpy",
            "cny",
            "krw",
            "hkd",
            "sgd",
            "twd",
            "inr",
            "thb",
        ],
        reason: str,
        expires_at: str | None = None,
        idempotency_key: str | None = None,
    ) -> CustomerCredit:
        """Grant monetary credit in one currency. Credit is applied FIFO before tax to eligible recurring invoices."""
        body = build_body(amount=amount, currency=currency, reason=reason, expires_at=expires_at)
        return _parse_data(
            await self._http.post(
                f"/customers/{id}/credits", body, idempotency_key=idempotency_key
            ),
            CustomerCredit,
        )

    async def revoke_plan_grant(
        self, id: str, grant_id: str, *, reason: str, idempotency_key: str | None = None
    ) -> PlanGrant:
        """End expanded access immediately and restore the base plan's limits. The subscription, billing cycle, invoices, and payment state remain unchanged."""
        body = build_body(reason=reason)
        return _parse_data(
            await self._http.post(
                f"/customers/{id}/plan-grants/{grant_id}/revoke",
                body,
                idempotency_key=idempotency_key,
            ),
            PlanGrant,
        )

    async def update_plan_grant(
        self,
        id: str,
        grant_id: str,
        *,
        reason: str,
        duration: Literal["cycles", "until_date", "until_revoked"],
        duration_cycles: int | None = None,
        expires_at: str | None = None,
        idempotency_key: str | None = None,
    ) -> PlanGrant:
        """Keep the overlay for a number of the subscription's existing billing cycles, set an exact deadline, or leave it active until revoked. The billing anchor is never reset."""
        body = build_body(
            reason=reason, duration=duration, duration_cycles=duration_cycles, expires_at=expires_at
        )
        return _parse_data(
            await self._http.patch(
                f"/customers/{id}/plan-grants/{grant_id}", body, idempotency_key=idempotency_key
            ),
            PlanGrant,
        )

    async def list_plan_grants(self, id: str) -> CustomersListPlanGrantsResult:
        """List the independent audit timeline for paid-plan access granted without checkout or payment credentials."""
        return _parse_data(
            await self._http.get(f"/customers/{id}/plan-grants"), CustomersListPlanGrantsResult
        )

    async def create_plan_grant(
        self,
        id: str,
        *,
        subscription_id: str,
        plan_id: str,
        reason: str,
        duration: Literal["cycles", "until_date", "until_revoked"],
        duration_cycles: int | None = None,
        expires_at: str | None = None,
        idempotency_key: str | None = None,
    ) -> PlanGrant:
        """Temporarily expand an active subscription's feature access using a higher plan in the same plan group. Billing, prices, periods, invoices, and the base subscription remain unchanged."""
        body = build_body(
            subscription_id=subscription_id,
            plan_id=plan_id,
            reason=reason,
            duration=duration,
            duration_cycles=duration_cycles,
            expires_at=expires_at,
        )
        return _parse_data(
            await self._http.post(
                f"/customers/{id}/plan-grants", body, idempotency_key=idempotency_key
            ),
            PlanGrant,
        )

    async def get(self, id: str) -> Customer:
        """Retrieve a customer by their public ID, including subscription status and metadata."""
        return _parse_data(await self._http.get(f"/customers/{id}"), Customer)

    async def update(
        self,
        id: str,
        *,
        email: str | None = None,
        full_name: str | None = None,
        tax_document: str | None = None,
        external_id: str | None = None,
        timezone: Timezone | None = None,
        metadata: dict[str, Any] | None = None,
        address: UpdateCustomerParamsAddress | None = None,
        idempotency_key: str | None = None,
    ) -> Customer:
        """Update a customer's name, external ID, or metadata."""
        body = build_body(
            email=email,
            full_name=full_name,
            tax_document=tax_document,
            external_id=external_id,
            timezone=timezone,
            metadata=metadata,
            address=address,
        )
        return _parse_data(
            await self._http.patch(f"/customers/{id}", body, idempotency_key=idempotency_key),
            Customer,
        )

    async def create_batch(
        self,
        *,
        customers: builtins.list[BatchCreateCustomersParamsCustomersItem],
        idempotency_key: str | None = None,
    ) -> CustomerBatch:
        """Create up to 100 customers in a single request."""
        body = build_body(customers=customers)
        return _parse_data(
            await self._http.post("/customers/batch", body, idempotency_key=idempotency_key),
            CustomerBatch,
        )

    async def list(
        self, *, cursor: str | None = None, limit: int | None = None, external_id: str | None = None
    ) -> CustomersListResult:
        """List customers with cursor-based pagination."""
        query = build_body(cursor=cursor, limit=limit, external_id=external_id)
        return _parse_data(await self._http.get("/customers", query), CustomersListResult)

    async def create(
        self,
        *,
        email: str,
        id: str | None = None,
        external_id: str | None = None,
        full_name: str | None = None,
        tax_document: str | None = None,
        address: CreateCustomerParamsAddress | None = None,
        address_id: str | None = None,
        timezone: Timezone | None = None,
        metadata: dict[str, Any] | None = None,
        idempotency_key: str | None = None,
    ) -> Customer:
        """Create a new customer. Idempotent when customerId is provided."""
        body = build_body(
            id=id,
            external_id=external_id,
            full_name=full_name,
            tax_document=tax_document,
            address=address,
            address_id=address_id,
            email=email,
            timezone=timezone,
            metadata=metadata,
        )
        return _parse_data(
            await self._http.post("/customers", body, idempotency_key=idempotency_key), Customer
        )
