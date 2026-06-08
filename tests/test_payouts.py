from __future__ import annotations

import json

import pytest
import respx
from httpx import Response

from commet import Commet
from commet.async_client import AsyncCommet
from commet.types import Payout, PayoutBankAccount, PayoutVerification


@pytest.fixture
def mock_api() -> respx.MockRouter:
    with respx.mock(base_url="https://commet.co/api/v1") as mock:
        yield mock


class TestAddBankAccount:
    def test_sends_camel_case_body_and_parses_last4_response(
        self, mock_api: respx.MockRouter
    ) -> None:
        route = mock_api.post("/payouts/bank-accounts").mock(
            return_value=Response(
                200,
                json={
                    "success": True,
                    "data": {
                        "id": "pba_1",
                        "providerExternalAccountId": "ba_ext_1",
                        "holderName": "Acme Inc",
                        "last4": "6789",
                        "bankName": "Big Bank",
                        "country": "US",
                        "currency": "usd",
                        "accountType": "checking",
                        "isDefault": True,
                        "status": "active",
                        "createdAt": "2026-06-01T00:00:00Z",
                        "object": "payout_bank_account",
                    },
                },
            )
        )
        with Commet(api_key="ck_test_123") as client:
            result = client.payouts.add_bank_account(
                account_number="000123456789",
                account_holder_name="Acme Inc",
                routing_number="110000000",
                account_type="checking",
                set_default=True,
            )

        assert result.success is True
        assert isinstance(result.data, PayoutBankAccount)
        assert result.data.last4 == "6789"
        assert result.data.account_type == "checking"
        assert result.data.is_default is True
        # Full account number must never appear in the parsed response.
        assert not hasattr(result.data, "account_number")

        sent = json.loads(route.calls.last.request.content)
        assert sent == {
            "accountNumber": "000123456789",
            "accountHolderName": "Acme Inc",
            "routingNumber": "110000000",
            "accountType": "checking",
            "setDefault": True,
        }

    def test_omitted_optionals_are_not_sent(self, mock_api: respx.MockRouter) -> None:
        route = mock_api.post("/payouts/bank-accounts").mock(
            return_value=Response(
                200,
                json={
                    "success": True,
                    "data": {
                        "id": "pba_2",
                        "holderName": "Solo Dev",
                        "last4": "0000",
                        "country": "US",
                        "currency": "usd",
                        "isDefault": False,
                    },
                },
            )
        )
        with Commet(api_key="ck_test_123") as client:
            client.payouts.add_bank_account(
                account_number="999",
                account_holder_name="Solo Dev",
            )

        sent = json.loads(route.calls.last.request.content)
        assert sent == {"accountNumber": "999", "accountHolderName": "Solo Dev"}
        assert "routingNumber" not in sent
        assert "accountType" not in sent
        assert "setDefault" not in sent


class TestRequestPayout:
    def test_sends_amount_and_parses_net_and_status(self, mock_api: respx.MockRouter) -> None:
        route = mock_api.post("/payouts").mock(
            return_value=Response(
                200,
                json={
                    "success": True,
                    "data": {
                        "id": "po_1",
                        "status": "pending",
                        "amount": 100000,
                        "fee": 250,
                        "netAmount": 99750,
                        "currency": "usd",
                        "description": "Weekly withdrawal",
                        "providerTransferId": "tr_1",
                        "createdAt": "2026-06-01T00:00:00Z",
                        "object": "payout",
                    },
                },
            )
        )
        with Commet(api_key="ck_test_123") as client:
            result = client.payouts.request(amount=100000, description="Weekly withdrawal")

        assert isinstance(result.data, Payout)
        assert result.data.status == "pending"
        assert result.data.net_amount == 99750
        assert result.data.provider_transfer_id == "tr_1"

        sent = json.loads(route.calls.last.request.content)
        assert sent == {"amount": 100000, "description": "Weekly withdrawal"}


class TestCompleteVerification:
    def test_sends_deeply_nested_kyc_body_as_camel_case(
        self, mock_api: respx.MockRouter
    ) -> None:
        route = mock_api.post("/payouts/verification").mock(
            return_value=Response(
                200,
                json={
                    "success": True,
                    "data": {
                        "providerAccountId": "acct_1",
                        "status": "pending_verification",
                        "transfersEnabled": False,
                        "alreadyExists": False,
                        "businessType": "individual",
                        "country": "US",
                        "object": "payout_account",
                    },
                },
            )
        )

        bank = {
            "account_number": "000123456789",
            "account_holder_name": "Jane Doe",
            "routing_number": "110000000",
            "account_type": "checking",
        }
        individual = {
            "first_name": "Jane",
            "last_name": "Doe",
            "phone": "+15555550123",
            "date_of_birth": "1990-01-01",
            "ssn_last4": "4321",
            "address": {
                "line1": "1 Main St",
                "city": "NYC",
                "state": "NY",
                "postal_code": "10001",
                "country": "US",
            },
        }

        with Commet(api_key="ck_test_123") as client:
            result = client.payouts.complete_verification(
                email="jane@example.com",
                business_type="individual",
                business_url="https://acme.test",
                document_url="https://files.test/id.png",
                bank=bank,
                individual=individual,
            )

        assert isinstance(result.data, PayoutVerification)
        assert result.data.status == "pending_verification"
        assert result.data.transfers_enabled is False
        assert result.data.business_type == "individual"

        sent = json.loads(route.calls.last.request.content)
        assert sent["email"] == "jane@example.com"
        assert sent["businessType"] == "individual"
        assert sent["businessUrl"] == "https://acme.test"
        assert sent["documentUrl"] == "https://files.test/id.png"
        assert sent["bank"] == {
            "accountNumber": "000123456789",
            "accountHolderName": "Jane Doe",
            "routingNumber": "110000000",
            "accountType": "checking",
        }
        # Deep recursion through convert_keys: nested address keys are camelCased too.
        assert sent["individual"]["dateOfBirth"] == "1990-01-01"
        assert sent["individual"]["ssnLast4"] == "4321"
        assert sent["individual"]["address"]["postalCode"] == "10001"
        # Omitted optional top-level object must not be sent.
        assert "company" not in sent


@pytest.mark.asyncio
class TestAsyncPayouts:
    async def test_request_payout_parses_response(self, mock_api: respx.MockRouter) -> None:
        mock_api.post("/payouts").mock(
            return_value=Response(
                200,
                json={
                    "success": True,
                    "data": {
                        "id": "po_async",
                        "status": "in_transit",
                        "amount": 50000,
                        "fee": 0,
                        "netAmount": 50000,
                        "currency": "usd",
                        "providerTransferId": "tr_async",
                        "createdAt": "2026-06-01T00:00:00Z",
                    },
                },
            )
        )
        async with AsyncCommet(api_key="ck_test_123") as client:
            result = await client.payouts.request(amount=50000)

        assert isinstance(result.data, Payout)
        assert result.data.status == "in_transit"
        assert result.data.net_amount == 50000

    async def test_add_bank_account_sends_camel_case(self, mock_api: respx.MockRouter) -> None:
        route = mock_api.post("/payouts/bank-accounts").mock(
            return_value=Response(
                200,
                json={
                    "success": True,
                    "data": {
                        "id": "pba_async",
                        "holderName": "Async Co",
                        "last4": "1111",
                        "country": "US",
                        "currency": "usd",
                        "isDefault": False,
                    },
                },
            )
        )
        async with AsyncCommet(api_key="ck_test_123") as client:
            result = await client.payouts.add_bank_account(
                account_number="111", account_holder_name="Async Co", set_default=False
            )

        assert isinstance(result.data, PayoutBankAccount)
        assert result.data.last4 == "1111"
        sent = json.loads(route.calls.last.request.content)
        assert sent == {
            "accountNumber": "111",
            "accountHolderName": "Async Co",
            "setDefault": False,
        }
