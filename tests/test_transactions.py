from __future__ import annotations

import pytest
import respx
from httpx import Response

from commet import Commet
from commet.async_client import AsyncCommet
from commet.types import (
    Transaction,
    TransactionRefund,
    TransactionRetry,
    TransactionStatus,
)


@pytest.fixture
def mock_api() -> respx.MockRouter:
    with respx.mock(base_url="https://commet.co/api/v1") as mock:
        yield mock


class TestList:
    def test_enum_status_filter_serializes_to_wire_string(
        self, mock_api: respx.MockRouter
    ) -> None:
        route = mock_api.get("/transactions").mock(
            return_value=Response(
                200,
                json={
                    "success": True,
                    "data": [
                        {
                            "id": "txn_1",
                            "invoiceId": "inv_1",
                            "grossAmount": 10800,
                            "subtotal": 10000,
                            "taxAmount": 800,
                            "currency": "usd",
                            "status": "succeeded",
                            "customerEmail": "a@example.com",
                            "paidAt": "2026-06-01T00:00:00Z",
                            "createdAt": "2026-06-01T00:00:00Z",
                            "availableAt": None,
                        }
                    ],
                    "hasMore": True,
                    "nextCursor": "cur_2",
                },
            )
        )
        with Commet(api_key="ck_test_123") as client:
            result = client.transactions.list(
                status=TransactionStatus.SUCCEEDED, customer_email="a@example.com"
            )

        assert result.has_more is True
        assert result.next_cursor == "cur_2"
        txn = result.data[0]
        assert isinstance(txn, Transaction)
        assert txn.status is TransactionStatus.SUCCEEDED
        assert txn.gross_amount == 10800
        assert txn.available_at is None

        params = route.calls.last.request.url.params
        # The Enum member must reach the wire as its string value (".value"),
        # not the member repr "TransactionStatus.SUCCEEDED".
        assert params["status"] == "succeeded"
        assert params["customerEmail"] == "a@example.com"


class TestGet:
    def test_get_parses_status_enum(self, mock_api: respx.MockRouter) -> None:
        mock_api.get("/transactions/txn_1").mock(
            return_value=Response(
                200,
                json={
                    "success": True,
                    "data": {
                        "id": "txn_1",
                        "grossAmount": 5000,
                        "currency": "usd",
                        "status": "disputed",
                    },
                },
            )
        )
        with Commet(api_key="ck_test_123") as client:
            result = client.transactions.get("txn_1")

        assert result.data.status is TransactionStatus.DISPUTED


class TestRefundRetry:
    def test_refund_no_body_post_parses_refunded_status(
        self, mock_api: respx.MockRouter
    ) -> None:
        route = mock_api.post("/transactions/txn_1/refund").mock(
            return_value=Response(
                200,
                json={
                    "success": True,
                    "data": {"id": "txn_1", "status": "refunded", "object": "transaction"},
                },
            )
        )
        with Commet(api_key="ck_test_123") as client:
            result = client.transactions.refund("txn_1")

        assert isinstance(result.data, TransactionRefund)
        assert result.data.status == "refunded"
        assert route.calls.last.request.content in (b"", b"null")

    def test_retry_parses_new_invoice_number(self, mock_api: respx.MockRouter) -> None:
        mock_api.post("/transactions/txn_1/retry").mock(
            return_value=Response(
                200,
                json={
                    "success": True,
                    "data": {
                        "id": "txn_1",
                        "status": "processing",
                        "retryInvoiceNumber": "INV-RETRY-001",
                    },
                },
            )
        )
        with Commet(api_key="ck_test_123") as client:
            result = client.transactions.retry("txn_1")

        assert isinstance(result.data, TransactionRetry)
        assert result.data.status == "processing"
        assert result.data.retry_invoice_number == "INV-RETRY-001"


@pytest.mark.asyncio
class TestAsyncTransactions:
    async def test_list_parses_enums(self, mock_api: respx.MockRouter) -> None:
        mock_api.get("/transactions").mock(
            return_value=Response(
                200,
                json={
                    "success": True,
                    "data": [{"id": "txn_a", "status": "failed", "currency": "usd"}],
                },
            )
        )
        async with AsyncCommet(api_key="ck_test_123") as client:
            result = await client.transactions.list()

        assert result.data[0].status is TransactionStatus.FAILED
