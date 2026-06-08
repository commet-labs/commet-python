from __future__ import annotations

import json

import pytest
import respx
from httpx import Response

from commet import Commet
from commet.async_client import AsyncCommet
from commet.types import (
    CreatedInvoice,
    Invoice,
    InvoiceLineItemsItem,
    InvoiceStatus,
    InvoiceType,
)


@pytest.fixture
def mock_api() -> respx.MockRouter:
    with respx.mock(base_url="https://commet.co/api/v1") as mock:
        yield mock


class TestGet:
    def test_get_parses_line_items_and_invoice_type_enum(
        self, mock_api: respx.MockRouter
    ) -> None:
        mock_api.get("/invoices/inv_1").mock(
            return_value=Response(
                200,
                json={
                    "success": True,
                    "data": {
                        "id": "inv_1",
                        "customerId": "cus_1",
                        "invoiceNumber": "INV-001",
                        "status": "paid",
                        "invoiceType": "recurring",
                        "currency": "usd",
                        "subtotal": 10000,
                        "taxAmount": 800,
                        "total": 10800,
                        "lineItems": [
                            {
                                "lineType": "plan_base",
                                "description": "Pro plan",
                                "quantity": 1,
                                "unitAmount": 10000,
                                "amount": 10000,
                                "chargeType": "standard",
                            },
                            {
                                "lineType": "feature_overage",
                                "featureName": "API Calls",
                                "description": "Overage",
                                "quantity": 50,
                                "unitAmount": 16,
                                "amount": 800,
                                "overageAmount": 800,
                            },
                        ],
                        "metadata": {"po": "123"},
                        "object": "invoice",
                    },
                },
            )
        )
        with Commet(api_key="ck_test_123") as client:
            result = client.invoices.get("inv_1")

        invoice = result.data
        assert isinstance(invoice, Invoice)
        assert invoice.invoice_type is InvoiceType.RECURRING
        assert invoice.total == 10800
        assert invoice.metadata == {"po": "123"}

        assert isinstance(invoice.line_items[0], InvoiceLineItemsItem)
        assert invoice.line_items[0].line_type == "plan_base"
        assert invoice.line_items[0].charge_type == "standard"
        assert invoice.line_items[1].feature_name == "API Calls"
        assert invoice.line_items[1].overage_amount == 800


class TestList:
    def test_list_filters_passed_as_camel_case_query(self, mock_api: respx.MockRouter) -> None:
        route = mock_api.get("/invoices").mock(
            return_value=Response(200, json={"success": True, "data": [], "hasMore": False})
        )
        with Commet(api_key="ck_test_123") as client:
            result = client.invoices.list(customer_id="cus_1", status="outstanding", limit=10)

        assert result.has_more is False
        params = route.calls.last.request.url.params
        assert params["customerId"] == "cus_1"
        assert params["status"] == "outstanding"
        assert params["limit"] == "10"
        assert "subscriptionId" not in params


class TestCreateAdjustment:
    def test_negative_amount_credit_is_sent_through(self, mock_api: respx.MockRouter) -> None:
        route = mock_api.post("/invoices").mock(
            return_value=Response(
                200,
                json={
                    "success": True,
                    "data": {
                        "id": "inv_adj",
                        "customerId": "cus_1",
                        "invoiceNumber": "INV-ADJ",
                        "invoiceType": "adjustment",
                        "currency": "usd",
                        "subtotal": -2500,
                        "taxAmount": 0,
                        "total": -2500,
                    },
                },
            )
        )
        with Commet(api_key="ck_test_123") as client:
            result = client.invoices.create_adjustment(
                customer_id="cus_1", amount=-2500, description="Goodwill credit"
            )

        assert isinstance(result.data, CreatedInvoice)
        assert result.data.invoice_type is InvoiceType.ADJUSTMENT
        assert result.data.total == -2500

        sent = json.loads(route.calls.last.request.content)
        assert sent == {
            "customerId": "cus_1",
            "amount": -2500,
            "description": "Goodwill credit",
        }


class TestUpdateStatus:
    def test_sends_status_body(self, mock_api: respx.MockRouter) -> None:
        route = mock_api.put("/invoices/inv_1/status").mock(
            return_value=Response(
                200,
                json={
                    "success": True,
                    "data": {
                        "id": "inv_1",
                        "status": "void",
                        "updatedAt": "2026-06-01T00:00:00Z",
                    },
                },
            )
        )
        with Commet(api_key="ck_test_123") as client:
            result = client.invoices.update_status("inv_1", status="void")

        assert isinstance(result.data, InvoiceStatus)
        assert result.data.status == "void"
        sent = json.loads(route.calls.last.request.content)
        assert sent == {"status": "void"}


@pytest.mark.asyncio
class TestAsyncInvoices:
    async def test_get_parses_line_items(self, mock_api: respx.MockRouter) -> None:
        mock_api.get("/invoices/inv_1").mock(
            return_value=Response(
                200,
                json={
                    "success": True,
                    "data": {
                        "id": "inv_1",
                        "customerId": "cus_1",
                        "invoiceNumber": "INV-001",
                        "invoiceType": "credit_purchase",
                        "currency": "usd",
                        "total": 5000,
                        "lineItems": [
                            {
                                "lineType": "credit",
                                "description": "Credit pack",
                                "quantity": 1,
                                "unitAmount": 5000,
                                "amount": 5000,
                            }
                        ],
                    },
                },
            )
        )
        async with AsyncCommet(api_key="ck_test_123") as client:
            result = await client.invoices.get("inv_1")

        assert result.data.invoice_type is InvoiceType.CREDIT_PURCHASE
        assert result.data.line_items[0].line_type == "credit"
