from __future__ import annotations

import json

import pytest
import respx
from httpx import Response

from commet import Commet
from commet.async_client import AsyncCommet
from commet.types import QuotaAllowance, QuotaEvent


@pytest.fixture
def mock_api() -> respx.MockRouter:
    with respx.mock(base_url="https://commet.co/api/v1") as mock:
        yield mock


class TestQuotaAdd:
    def test_add_defaults_count_to_one(self, mock_api: respx.MockRouter) -> None:
        route = mock_api.post("/usage/quota").mock(
            return_value=Response(200, json={
                "success": True,
                "data": {
                    "id": "qe_1",
                    "customerId": "cus_1",
                    "featureCode": "storage",
                    "previousBalance": 0,
                    "newBalance": 1,
                    "ts": "2026-06-01T00:00:00Z",
                    "createdAt": "2026-06-01T00:00:00Z",
                },
            })
        )
        with Commet(api_key="ck_test_123") as client:
            result = client.quota.add(feature_code="storage", customer_id="cus_1")
            assert result.success is True
            assert isinstance(result.data, QuotaEvent)
            assert result.data.id == "qe_1"
            assert result.data.new_balance == 1

        sent = json.loads(route.calls.last.request.content)
        assert sent == {"featureCode": "storage", "count": 1, "customerId": "cus_1"}


class TestQuotaSet:
    def test_set_sends_required_count(self, mock_api: respx.MockRouter) -> None:
        route = mock_api.put("/usage/quota").mock(
            return_value=Response(200, json={
                "success": True,
                "data": {
                    "id": "qe_2",
                    "customerId": "cus_1",
                    "featureCode": "storage",
                    "previousBalance": 1,
                    "newBalance": 5,
                    "ts": "2026-06-01T00:00:00Z",
                    "createdAt": "2026-06-01T00:00:00Z",
                },
            })
        )
        with Commet(api_key="ck_test_123") as client:
            result = client.quota.set(feature_code="storage", count=5, customer_id="cus_1")
            assert result.success is True
            assert isinstance(result.data, QuotaEvent)
            assert result.data.previous_balance == 1
            assert result.data.new_balance == 5

        sent = json.loads(route.calls.last.request.content)
        assert sent == {"featureCode": "storage", "count": 5, "customerId": "cus_1"}


class TestQuotaRemove:
    def test_remove_defaults_count_to_one(self, mock_api: respx.MockRouter) -> None:
        route = mock_api.delete("/usage/quota").mock(
            return_value=Response(200, json={
                "success": True,
                "data": {
                    "id": "qe_3",
                    "customerId": "cus_1",
                    "featureCode": "storage",
                    "previousBalance": 5,
                    "newBalance": 4,
                    "ts": "2026-06-01T00:00:00Z",
                    "createdAt": "2026-06-01T00:00:00Z",
                },
            })
        )
        with Commet(api_key="ck_test_123") as client:
            result = client.quota.remove(feature_code="storage", customer_id="cus_1")
            assert result.success is True
            assert isinstance(result.data, QuotaEvent)
            assert result.data.new_balance == 4

        sent = json.loads(route.calls.last.request.content)
        assert sent == {"featureCode": "storage", "count": 1, "customerId": "cus_1"}


class TestQuotaGet:
    def test_get_parses_allowance(self, mock_api: respx.MockRouter) -> None:
        route = mock_api.get("/usage/quota").mock(
            return_value=Response(200, json={
                "success": True,
                "data": {
                    "featureCode": "storage",
                    "current": 4,
                    "included": 10,
                    "remaining": 6,
                    "billedQuantity": 12,
                    "unlimited": False,
                    "overageEnabled": True,
                    "asOf": "2026-06-01T00:00:00Z",
                },
            })
        )
        with Commet(api_key="ck_test_123") as client:
            result = client.quota.get(feature_code="storage", customer_id="cus_1")
            assert result.success is True
            assert isinstance(result.data, QuotaAllowance)
            assert result.data.feature_code == "storage"
            assert result.data.current == 4
            assert result.data.included == 10
            assert result.data.remaining == 6
            assert result.data.billed_quantity == 12
            assert result.data.unlimited is False
            assert result.data.overage_enabled is True

        assert route.calls.last.request.url.params["featureCode"] == "storage"
        assert route.calls.last.request.url.params["customerId"] == "cus_1"


class TestQuotaGetAll:
    def test_get_all_parses_list(self, mock_api: respx.MockRouter) -> None:
        route = mock_api.get("/usage/quota/all").mock(
            return_value=Response(200, json={
                "success": True,
                "data": [
                    {
                        "featureCode": "storage",
                        "current": 4,
                        "included": 10,
                        "remaining": 6,
                        "unlimited": False,
                        "overageEnabled": False,
                        "asOf": "2026-06-01T00:00:00Z",
                    },
                    {
                        "featureCode": "seats",
                        "current": 2,
                        "included": 0,
                        "remaining": None,
                        "unlimited": True,
                        "overageEnabled": False,
                        "asOf": None,
                    },
                ],
            })
        )
        with Commet(api_key="ck_test_123") as client:
            result = client.quota.get_all(customer_id="cus_1")
            assert result.success is True
            assert isinstance(result.data, list)
            assert len(result.data) == 2
            assert all(isinstance(item, QuotaAllowance) for item in result.data)
            assert result.data[0].feature_code == "storage"
            assert result.data[0].remaining == 6
            assert result.data[1].unlimited is True
            assert result.data[1].remaining is None

        assert route.calls.last.request.url.params["customerId"] == "cus_1"


@pytest.mark.asyncio
class TestAsyncQuota:
    async def test_add_returns_event(self, mock_api: respx.MockRouter) -> None:
        mock_api.post("/usage/quota").mock(
            return_value=Response(200, json={
                "success": True,
                "data": {
                    "id": "qe_1",
                    "customerId": "cus_1",
                    "featureCode": "storage",
                    "previousBalance": 0,
                    "newBalance": 1,
                    "ts": "2026-06-01T00:00:00Z",
                    "createdAt": "2026-06-01T00:00:00Z",
                },
            })
        )
        async with AsyncCommet(api_key="ck_test_123") as client:
            result = await client.quota.add(feature_code="storage", customer_id="cus_1")
            assert result.success is True
            assert isinstance(result.data, QuotaEvent)
            assert result.data.new_balance == 1

    async def test_get_all_returns_list(self, mock_api: respx.MockRouter) -> None:
        mock_api.get("/usage/quota/all").mock(
            return_value=Response(200, json={
                "success": True,
                "data": [
                    {
                        "featureCode": "storage",
                        "current": 4,
                        "included": 10,
                        "remaining": 6,
                        "unlimited": False,
                        "overageEnabled": False,
                        "asOf": "2026-06-01T00:00:00Z",
                    },
                ],
            })
        )
        async with AsyncCommet(api_key="ck_test_123") as client:
            result = await client.quota.get_all(customer_id="cus_1")
            assert result.success is True
            assert isinstance(result.data, list)
            assert result.data[0].feature_code == "storage"
