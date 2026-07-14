# ruff: noqa: E501

from __future__ import annotations

from .._async_http import AsyncCommetHTTPClient
from .._http import ApiResponse
from .._shared import build_body
from ..types import (
    Payment,
    _parse,
    _parse_list,
)


class AsyncPaymentsResource:
    def __init__(self, http: AsyncCommetHTTPClient) -> None:
        self._http = http

    async def list(
        self, *, customer_id: str | None = None, cursor: str | None = None, limit: int | None = None
    ) -> ApiResponse[list[Payment]]:
        """List payments with cursor-based pagination. Filter by customer."""
        query = build_body(customer_id=customer_id, cursor=cursor, limit=limit)
        return _parse_list(await self._http.get("/payments", query), Payment)

    async def create(
        self,
        *,
        amount: int,
        currency: str,
        description: str,
        customer_id: str | None = None,
        success_url: str | None = None,
        metadata: dict[str, str] | None = None,
        idempotency_key: str | None = None,
    ) -> ApiResponse[Payment]:
        """Create a hosted payment link. Returns a url the customer opens to pay with any card. Calculates tax, generates an invoice, and vaults the payment method on confirmation. No subscription or plan required."""
        body = build_body(
            amount=amount,
            currency=currency,
            customer_id=customer_id,
            description=description,
            success_url=success_url,
            metadata=metadata,
        )
        return _parse(
            await self._http.post("/payments", body, idempotency_key=idempotency_key), Payment
        )

    async def charge(
        self,
        *,
        customer_id: str,
        amount: int,
        currency: str,
        description: str,
        metadata: dict[str, str] | None = None,
        idempotency_key: str | None = None,
    ) -> ApiResponse[Payment]:
        """Charge a customer's vaulted payment method off-session. Calculates tax, generates an invoice, and sends a receipt. Requires the customer to have a subscription in active, trialing, or past_due state."""
        body = build_body(
            customer_id=customer_id,
            amount=amount,
            currency=currency,
            description=description,
            metadata=metadata,
        )
        return _parse(
            await self._http.post("/payments/charge", body, idempotency_key=idempotency_key),
            Payment,
        )

    async def get(self, id: str) -> ApiResponse[Payment]:
        """Retrieve a payment by its public ID."""
        return _parse(await self._http.get(f"/payments/{id}"), Payment)

    async def cancel(self, id: str, *, idempotency_key: str | None = None) -> ApiResponse[Payment]:
        """Cancel a pending payment link so it can no longer be paid. Only a link that has not been paid or started processing can be canceled; canceling an already canceled link is a no-op. Charges cannot be canceled."""
        return _parse(
            await self._http.post(f"/payments/{id}/cancel", idempotency_key=idempotency_key),
            Payment,
        )
