from __future__ import annotations

import pytest
import respx
from httpx import Response

from commet import Commet
from commet.async_client import AsyncCommet
from commet.types import FeatureAccess


@pytest.fixture
def mock_api() -> respx.MockRouter:
    with respx.mock(base_url="https://commet.co/api") as mock:
        yield mock


class TestFeaturesCheck:
    def test_check_returns_allowed_true_on_success(self, mock_api: respx.MockRouter) -> None:
        mock_api.get("/features/api_calls").mock(
            return_value=Response(200, json={
                "success": True,
                "data": {"code": "api_calls", "allowed": True, "current": 5, "included": 100},
            })
        )
        with Commet(api_key="ck_test_123") as client:
            result = client.features.check(code="api_calls", customer_id="cus_1")
            assert result.success is True
            assert result.data == {"allowed": True}

    def test_check_returns_allowed_false_on_success(self, mock_api: respx.MockRouter) -> None:
        mock_api.get("/features/api_calls").mock(
            return_value=Response(200, json={
                "success": True,
                "data": {"code": "api_calls", "allowed": False, "current": 100, "included": 100},
            })
        )
        with Commet(api_key="ck_test_123") as client:
            result = client.features.check(code="api_calls", customer_id="cus_1")
            assert result.success is True
            assert result.data == {"allowed": False}

    def test_check_propagates_api_error(self, mock_api: respx.MockRouter) -> None:
        mock_api.get("/features/api_calls").mock(
            return_value=Response(200, json={
                "success": False,
                "code": "no_subscription",
                "message": "Customer has no active subscription",
            })
        )
        with Commet(api_key="ck_test_123") as client:
            result = client.features.check(code="api_calls", customer_id="cus_1")
            assert result.success is False
            assert result.code == "no_subscription"
            assert result.message == "Customer has no active subscription"

    def test_get_parses_feature_access(self, mock_api: respx.MockRouter) -> None:
        mock_api.get("/features/api_calls").mock(
            return_value=Response(200, json={
                "success": True,
                "data": {
                    "code": "api_calls",
                    "name": "API Calls",
                    "type": "metered",
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
class TestAsyncFeaturesCheck:
    async def test_check_propagates_api_error(self, mock_api: respx.MockRouter) -> None:
        mock_api.get("/features/api_calls").mock(
            return_value=Response(200, json={
                "success": False,
                "code": "no_subscription",
                "message": "Customer has no active subscription",
            })
        )
        async with AsyncCommet(api_key="ck_test_123") as client:
            result = await client.features.check(code="api_calls", customer_id="cus_1")
            assert result.success is False
            assert result.code == "no_subscription"
            assert result.message == "Customer has no active subscription"

    async def test_check_returns_allowed_on_success(self, mock_api: respx.MockRouter) -> None:
        mock_api.get("/features/api_calls").mock(
            return_value=Response(200, json={
                "success": True,
                "data": {"code": "api_calls", "allowed": True},
            })
        )
        async with AsyncCommet(api_key="ck_test_123") as client:
            result = await client.features.check(code="api_calls", customer_id="cus_1")
            assert result.success is True
            assert result.data == {"allowed": True}
