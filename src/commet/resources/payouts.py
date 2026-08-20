# ruff: noqa: E501

from __future__ import annotations

from typing import Literal

from .._http import CommetHTTPClient
from .._shared import build_body
from ..types import (
    Payout,
    PayoutBankAccount,
    _data,
    _parse_data,
)


class PayoutsResource:
    def __init__(self, http: CommetHTTPClient) -> None:
        self._http = http

    def add_bank_account(
        self,
        *,
        account_number: str,
        account_holder_name: str,
        routing_number: str | None = None,
        account_type: Literal["checking", "savings"] | None = None,
        set_default: bool | None = None,
        idempotency_key: str | None = None,
    ) -> PayoutBankAccount:
        """Add an additional destination bank account to the organization's existing payout account. Country and currency are resolved from the organization. The full account number is never returned — only `last4`."""
        body = build_body(
            account_number=account_number,
            account_holder_name=account_holder_name,
            routing_number=routing_number,
            account_type=account_type,
            set_default=set_default,
        )
        return _parse_data(
            self._http.post("/payouts/bank-accounts", body, idempotency_key=idempotency_key),
            PayoutBankAccount,
        )

    def request(
        self, *, amount: int, description: str | None = None, idempotency_key: str | None = None
    ) -> Payout:
        """Withdraw available balance to the organization's verified payout account. `amount` is in cents (USD, minimum 1000 = $10). The payout is created in `pending` and settles to `paid` asynchronously as provider webhooks arrive."""
        body = build_body(amount=amount, description=description)
        return _parse_data(
            self._http.post("/payouts", body, idempotency_key=idempotency_key), Payout
        )

    def complete_verification(self, *, idempotency_key: str | None = None) -> None:
        """
        Deprecated. Complete business and identity verification in the Commet dashboard. This endpoint no longer accepts or processes KYC data.
        Deprecated.
        """
        return _data(self._http.post("/payouts/verification", idempotency_key=idempotency_key))
