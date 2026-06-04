from __future__ import annotations

import pytest
import respx
from httpx import Response

from commet import Commet
from commet.async_client import AsyncCommet
from commet.types import CanUseResult, FeatureAccess


@pytest.fixture
def mock_api() -> respx.MockRouter:
    with respx.mock(base_url="https://commet.co/api/v1") as mock:
        yield mock


class TestFeaturesCanUse:
    def test_can_use_returns_allowed_true_on_success(self, mock_api: respx.MockRouter) -> None:
        route = mock_api.get("/features/api_calls").mock(
            return_value=Response(200, json={
                "success": True,
                "data": {"allowed": True},
            })
        )
        with Commet(api_key="ck_test_123") as client:
            result = client.features.can_use(code="api_calls", customer_id="cus_1")
            assert result.success is True
            assert isinstance(result.data, CanUseResult)
            assert result.data.allowed is True
        assert dict(route.calls.last.request.url.params) == {
            "customerId": "cus_1",
            "action": "canUse",
        }

    def test_can_use_returns_allowed_false_on_success(self, mock_api: respx.MockRouter) -> None:
        route = mock_api.get("/features/api_calls").mock(
            return_value=Response(200, json={
                "success": True,
                "data": {"allowed": False},
            })
        )
        with Commet(api_key="ck_test_123") as client:
            result = client.features.can_use(code="api_calls", customer_id="cus_1")
            assert result.success is True
            assert isinstance(result.data, CanUseResult)
            assert result.data.allowed is False
        assert dict(route.calls.last.request.url.params) == {
            "customerId": "cus_1",
            "action": "canUse",
        }

    def test_get_propagates_api_error(self, mock_api: respx.MockRouter) -> None:
        mock_api.get("/features/api_calls").mock(
            return_value=Response(200, json={
                "success": False,
                "code": "no_subscription",
                "message": "Customer has no active subscription",
            })
        )
        with Commet(api_key="ck_test_123") as client:
            result = client.features.get(code="api_calls", customer_id="cus_1")
            assert result.success is False
            assert result.code == "no_subscription"
            assert result.message == "Customer has no active subscription"
            assert result.data is None

    def test_get_parses_feature_access(self, mock_api: respx.MockRouter) -> None:
        mock_api.get("/features/api_calls").mock(
            return_value=Response(200, json={
                "success": True,
                "data": {
                    "code": "api_calls",
                    "name": "API Calls",
                    "type": "usage",
                    "allowed": True,
                    "current": 50,
                    "included": 1000,
                },
            })
        )
        with Commet(api_key="ck_test_123") as client:
            result = client.features.get(code="api_calls", customer_id="cus_1")
            assert result.success is True
            assert isinstance(result.data, FeatureAccess)
            assert result.data.code == "api_calls"
            assert result.data.current == 50


@pytest.mark.asyncio
class TestAsyncFeaturesCanUse:
    async def test_get_propagates_api_error(self, mock_api: respx.MockRouter) -> None:
        mock_api.get("/features/api_calls").mock(
            return_value=Response(200, json={
                "success": False,
                "code": "no_subscription",
                "message": "Customer has no active subscription",
            })
        )
        async with AsyncCommet(api_key="ck_test_123") as client:
            result = await client.features.get(code="api_calls", customer_id="cus_1")
            assert result.success is False
            assert result.code == "no_subscription"
            assert result.message == "Customer has no active subscription"
            assert result.data is None

    async def test_can_use_returns_allowed_on_success(self, mock_api: respx.MockRouter) -> None:
        route = mock_api.get("/features/api_calls").mock(
            return_value=Response(200, json={
                "success": True,
                "data": {"allowed": True},
            })
        )
        async with AsyncCommet(api_key="ck_test_123") as client:
            result = await client.features.can_use(code="api_calls", customer_id="cus_1")
            assert result.success is True
            assert isinstance(result.data, CanUseResult)
            assert result.data.allowed is True
        assert dict(route.calls.last.request.url.params) == {
            "customerId": "cus_1",
            "action": "canUse",
        }
