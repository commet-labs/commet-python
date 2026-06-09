# ruff: noqa: E501

from __future__ import annotations

from typing import Literal

from .._http import ApiResponse, CommetHTTPClient
from .._shared import build_body
from ..types import (
    CompletePayoutVerificationParamsBank,
    CompletePayoutVerificationParamsCompany,
    CompletePayoutVerificationParamsIndividual,
    Payout,
    PayoutBankAccount,
    PayoutVerification,
    _parse,
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
    ) -> ApiResponse[PayoutBankAccount]:
        """Add an additional destination bank account to the organization's existing payout account. Country and currency are resolved from the organization. The full account number is never returned — only `last4`."""
        body = build_body(
            account_number=account_number,
            account_holder_name=account_holder_name,
            routing_number=routing_number,
            account_type=account_type,
            set_default=set_default,
        )
        return _parse(
            self._http.post("/payouts/bank-accounts", body, idempotency_key=idempotency_key),
            PayoutBankAccount,
        )

    def request(
        self, *, amount: int, description: str | None = None, idempotency_key: str | None = None
    ) -> ApiResponse[Payout]:
        """Withdraw available balance to the organization's verified payout account. `amount` is in cents (USD, minimum 1000 = $10). The payout is created in `pending` and settles to `paid` asynchronously as provider webhooks arrive."""
        body = build_body(amount=amount, description=description)
        return _parse(self._http.post("/payouts", body, idempotency_key=idempotency_key), Payout)

    def complete_verification(
        self,
        *,
        email: str,
        business_type: Literal["individual", "company"],
        business_url: str,
        document_url: str,
        bank: CompletePayoutVerificationParamsBank,
        individual: CompletePayoutVerificationParamsIndividual | None = None,
        company: CompletePayoutVerificationParamsCompany | None = None,
        idempotency_key: str | None = None,
    ) -> ApiResponse[PayoutVerification]:
        """Provision the organization's payout account in a single call with the full KYC + bank payload. Uploads the identity document, persists the destination bank, and creates the connected account through the org's payout provider. The account starts `pending_verification` and flips to `verified` via the provider's webhook. Idempotent: returns the existing account if the org already has one."""
        body = build_body(
            email=email,
            business_type=business_type,
            business_url=business_url,
            document_url=document_url,
            bank=bank,
            individual=individual,
            company=company,
        )
        return _parse(
            self._http.post("/payouts/verification", body, idempotency_key=idempotency_key),
            PayoutVerification,
        )
