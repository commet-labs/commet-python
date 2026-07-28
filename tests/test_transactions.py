from __future__ import annotations

import pytest
import respx
from httpx import Response

from commet import Commet
from commet.async_client import AsyncCommet
from commet.types import (
    Refund,
    TransactionListItem,
    TransactionRetry,
    TransactionStatus,
)


@pytest.fixture
def mock_api() -> respx.MockRouter:
    with respx.mock(base_url="https://commet.co/api/v1") as mock:
        yield mock


def test_list_uses_explicit_list_envelope(mock_api: respx.MockRouter) -> None:
    route = mock_api.get("/transactions").mock(
        return_value=Response(
            200,
            json={
                "object": "list",
                "data": [
                    {
                        "id": "txn_1",
                        "grossAmount": 10800,
                        "currency": "usd",
                        "status": "succeeded",
                    }
                ],
                "hasMore": True,
                "nextCursor": "cur_2",
            },
        )
    )
    with Commet(api_key="ck_test_123") as client:
        result = client.transactions.list(
            status=TransactionStatus.SUCCEEDED,
            customer_email="a@example.com",
        )

    assert result.has_more is True
    assert result.next_cursor == "cur_2"
    assert isinstance(result.data[0], TransactionListItem)
    assert result.data[0].status is TransactionStatus.SUCCEEDED
    assert route.calls.last.request.url.params["status"] == "succeeded"


def test_get_returns_direct_transaction(mock_api: respx.MockRouter) -> None:
    mock_api.get("/transactions/txn_1").mock(
        return_value=Response(
            200,
            json={
                "id": "txn_1",
                "grossAmount": 5000,
                "currency": "usd",
                "status": "disputed",
            },
        )
    )
    with Commet(api_key="ck_test_123") as client:
        transaction = client.transactions.get("txn_1")

    assert transaction.status is TransactionStatus.DISPUTED


def test_refund_returns_refund_resource(mock_api: respx.MockRouter) -> None:
    route = mock_api.post("/transactions/txn_1/refund").mock(
        return_value=Response(
            200,
            json={
                "id": "ref_1",
                "transactionId": "txn_1",
                "amount": 5000,
                "currency": "usd",
                "status": "succeeded",
            },
        )
    )
    with Commet(api_key="ck_test_123") as client:
        refund = client.transactions.refund("txn_1")

    assert isinstance(refund, Refund)
    assert refund.transaction_id == "txn_1"
    assert route.calls.last.request.content in (b"", b"null")


def test_retry_returns_retry_result(mock_api: respx.MockRouter) -> None:
    mock_api.post("/transactions/txn_1/retry").mock(
        return_value=Response(
            200,
            json={"id": "txn_2", "status": "processing"},
        )
    )
    with Commet(api_key="ck_test_123") as client:
        retry = client.transactions.retry("txn_1")

    assert isinstance(retry, TransactionRetry)
    assert retry.status == "processing"


@pytest.mark.asyncio
async def test_async_list_parses_enums(mock_api: respx.MockRouter) -> None:
    mock_api.get("/transactions").mock(
        return_value=Response(
            200,
            json={
                "object": "list",
                "data": [{"id": "txn_a", "status": "failed", "currency": "usd"}],
                "hasMore": False,
            },
        )
    )
    async with AsyncCommet(api_key="ck_test_123") as client:
        result = await client.transactions.list()

    assert result.data[0].status is TransactionStatus.FAILED
