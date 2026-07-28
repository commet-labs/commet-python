from __future__ import annotations

import json

import pytest
import respx
from httpx import Response

from commet import Commet
from commet.async_client import AsyncCommet
from commet.types import Invoice, InvoiceLineItemsItem, InvoiceType


@pytest.fixture
def mock_api() -> respx.MockRouter:
    with respx.mock(base_url="https://commet.co/api/v1") as mock:
        yield mock


def invoice_payload(invoice_type: str = "recurring") -> dict[str, object]:
    return {
        "id": "inv_1",
        "customerId": "cus_1",
        "invoiceNumber": "INV-001",
        "status": "paid",
        "invoiceType": invoice_type,
        "currency": "usd",
        "subtotal": 10000,
        "discountAmount": 0,
        "taxAmount": 800,
        "total": 10800,
        "periodStart": "2026-07-01",
        "periodEnd": "2026-08-01",
        "issueDate": "2026-07-01",
        "dueDate": "2026-07-01",
        "metadata": {"po": "123"},
        "createdAt": "2026-07-01",
        "updatedAt": "2026-07-01",
        "lineItems": [
            {
                "lineType": "plan_base",
                "description": "Pro plan",
                "quantity": 1,
                "unitAmount": 10000,
                "amount": 10000,
                "chargeType": "standard",
            }
        ],
    }


def test_get_parses_direct_invoice(mock_api: respx.MockRouter) -> None:
    mock_api.get("/invoices/inv_1").mock(return_value=Response(200, json=invoice_payload()))
    with Commet(api_key="ck_test_123") as client:
        invoice = client.invoices.get("inv_1")

    assert isinstance(invoice, Invoice)
    assert invoice.invoice_type is InvoiceType.RECURRING
    assert isinstance(invoice.line_items[0], InvoiceLineItemsItem)
    assert invoice.metadata == {"po": "123"}


def test_list_uses_explicit_list_envelope(mock_api: respx.MockRouter) -> None:
    route = mock_api.get("/invoices").mock(
        return_value=Response(
            200,
            json={"object": "list", "data": [], "hasMore": False},
        )
    )
    with Commet(api_key="ck_test_123") as client:
        result = client.invoices.list(customer_id="cus_1", status="outstanding", limit=10)

    assert result.has_more is False
    assert route.calls.last.request.url.params["customerId"] == "cus_1"


def test_create_adjustment_returns_invoice(mock_api: respx.MockRouter) -> None:
    route = mock_api.post("/invoices").mock(
        return_value=Response(200, json=invoice_payload("adjustment"))
    )
    with Commet(api_key="ck_test_123") as client:
        invoice = client.invoices.create_adjustment(
            customer_id="cus_1",
            amount=-2500,
            description="Goodwill credit",
        )

    assert isinstance(invoice, Invoice)
    assert invoice.invoice_type is InvoiceType.ADJUSTMENT
    assert json.loads(route.calls.last.request.content) == {
        "customerId": "cus_1",
        "amount": -2500,
        "description": "Goodwill credit",
    }


def test_update_status_uses_patch(mock_api: respx.MockRouter) -> None:
    route = mock_api.patch("/invoices/inv_1/status").mock(
        return_value=Response(200, json=invoice_payload())
    )
    with Commet(api_key="ck_test_123") as client:
        invoice = client.invoices.update_status("inv_1", status="paid")

    assert invoice.status == "paid"
    assert json.loads(route.calls.last.request.content) == {"status": "paid"}


@pytest.mark.asyncio
async def test_async_get_returns_direct_invoice(mock_api: respx.MockRouter) -> None:
    mock_api.get("/invoices/inv_1").mock(
        return_value=Response(200, json=invoice_payload("credit_purchase"))
    )
    async with AsyncCommet(api_key="ck_test_123") as client:
        invoice = await client.invoices.get("inv_1")

    assert invoice.invoice_type is InvoiceType.CREDIT_PURCHASE
