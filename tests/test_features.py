from __future__ import annotations

import pytest
import respx
from httpx import Response

from commet import Commet
from commet.async_client import AsyncCommet
from commet.types import (
    Feature,
    FeatureAccessVariant2,
)


@pytest.fixture
def mock_api() -> respx.MockRouter:
    with respx.mock(base_url="https://commet.co/api/v1") as mock:
        yield mock


class TestFeaturesCatalog:
    def test_list_parses_feature_catalog(self, mock_api: respx.MockRouter) -> None:
        route = mock_api.get("/features").mock(
            return_value=Response(
                200,
                json={
                    "object": "list",
                    "data": [
                        {
                            "id": "feat_1",
                            "name": "API Calls",
                            "code": "api_calls",
                            "type": "usage",
                            "createdAt": "2026-06-01T00:00:00Z",
                            "updatedAt": "2026-06-01T00:00:00Z",
                        }
                    ],
                    "hasMore": False,
                },
            )
        )
        with Commet(api_key="ck_test_123") as client:
            result = client.features.list()

        assert isinstance(result.data[0], Feature)
        assert result.data[0].code == "api_calls"
        assert dict(route.calls.last.request.url.params) == {}

    def test_get_parses_feature_definition(self, mock_api: respx.MockRouter) -> None:
        route = mock_api.get("/features/api_calls").mock(
            return_value=Response(
                200,
                json={
                    "id": "feat_1",
                    "name": "API Calls",
                    "code": "api_calls",
                    "type": "usage",
                    "createdAt": "2026-06-01T00:00:00Z",
                    "updatedAt": "2026-06-01T00:00:00Z",
                },
            )
        )
        with Commet(api_key="ck_test_123") as client:
            result = client.features.get("api_calls")

        assert isinstance(result, Feature)
        assert result.code == "api_calls"
        assert dict(route.calls.last.request.url.params) == {}


class TestFeatureAccess:
    def test_get_parses_feature_lookup(self, mock_api: respx.MockRouter) -> None:
        route = mock_api.get("/feature-access/api_calls").mock(
            return_value=Response(
                200,
                json={
                    "code": "api_calls",
                    "name": "API Calls",
                    "type": "usage",
                    "allowed": True,
                    "consumption": {
                        "model": "metered",
                        "period": {
                            "start": "2026-07-01T00:00:00Z",
                            "end": "2026-08-01T00:00:00Z",
                        },
                        "unitsUsed": 50,
                        "includedUnits": 1000,
                        "remainingUnits": 950,
                        "overage": {
                            "enabled": False,
                            "units": 0,
                            "unitPrice": {"amount": 0, "currency": "usd", "scale": 10000},
                        },
                    },
                },
            )
        )
        with Commet(api_key="ck_test_123") as client:
            result = client.feature_access.get("api_calls", customer_id="cus_1")

        assert isinstance(result, FeatureAccessVariant2)
        assert result.code == "api_calls"
        assert result.allowed is True
        assert dict(route.calls.last.request.url.params) == {"customerId": "cus_1"}

    def test_list_parses_feature_access(self, mock_api: respx.MockRouter) -> None:
        route = mock_api.get("/feature-access").mock(
            return_value=Response(
                200,
                json={
                    "object": "list",
                    "data": [
                        {
                            "code": "api_calls",
                            "name": "API Calls",
                            "type": "usage",
                            "allowed": True,
                        }
                    ],
                    "hasMore": False,
                },
            )
        )
        with Commet(api_key="ck_test_123") as client:
            result = client.feature_access.list(customer_id="cus_1")

        assert isinstance(result.data[0], FeatureAccessVariant2)
        assert result.data[0].code == "api_calls"
        assert result.data[0].allowed is True
        assert dict(route.calls.last.request.url.params) == {"customerId": "cus_1"}


@pytest.mark.asyncio
async def test_async_feature_access_get(mock_api: respx.MockRouter) -> None:
    mock_api.get("/feature-access/api_calls").mock(
        return_value=Response(
            200,
            json={
                "code": "api_calls",
                "name": "API Calls",
                "type": "boolean",
                "allowed": True,
                "enabled": True,
            },
        )
    )
    async with AsyncCommet(api_key="ck_test_123") as client:
        result = await client.feature_access.get("api_calls", customer_id="cus_1")

    assert result.allowed is True
