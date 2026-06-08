from __future__ import annotations

import pytest
import respx
from httpx import Response

from commet.async_client import AsyncCommet
from commet.types import Customer


@pytest.fixture
def mock_api() -> respx.MockRouter:
    with respx.mock(base_url="https://commet.co/api/v1") as mock:
        yield mock


@pytest.mark.asyncio
async def test_async_context_manager(mock_api: respx.MockRouter) -> None:
    async with AsyncCommet(api_key="ck_test_123") as client:
        assert client is not None


@pytest.mark.asyncio
async def test_async_customer_create(mock_api: respx.MockRouter) -> None:
    mock_api.post("/customers").mock(
        return_value=Response(
            200,
            json={
                "success": True,
                "data": {
                    "id": "cus_123",
                    "externalId": "org_1",
                    "email": "user@example.com",
                    "createdAt": "2024-01-01T00:00:00Z",
                    "updatedAt": "2024-01-01T00:00:00Z",
                },
            },
        )
    )

    async with AsyncCommet(api_key="ck_test_123") as client:
        result = await client.customers.create(email="user@example.com")
        assert result.success is True
        assert isinstance(result.data, Customer)
        assert result.data.id == "cus_123"
        assert result.data.email == "user@example.com"


@pytest.mark.asyncio
async def test_async_customer_list(mock_api: respx.MockRouter) -> None:
    mock_api.get("/customers").mock(
        return_value=Response(
            200,
            json={
                "success": True,
                "data": [
                    {
                        "id": "cus_1",
                        "email": "a@example.com",
                        "createdAt": "2024-01-01T00:00:00Z",
                        "updatedAt": "2024-01-01T00:00:00Z",
                    },
                    {
                        "id": "cus_2",
                        "email": "b@example.com",
                        "createdAt": "2024-01-01T00:00:00Z",
                        "updatedAt": "2024-01-01T00:00:00Z",
                    },
                ],
                "hasMore": False,
            },
        )
    )

    async with AsyncCommet(api_key="ck_test_123") as client:
        result = await client.customers.list()
        assert result.success is True
        assert len(result.data) == 2
        assert all(isinstance(c, Customer) for c in result.data)
        assert result.has_more is False


@pytest.mark.asyncio
async def test_async_usage_track(mock_api: respx.MockRouter) -> None:
    mock_api.post("/usage/events").mock(
        return_value=Response(
            200,
            json={
                "success": True,
                "data": {
                    "id": "evt_123",
                    "organizationId": "org_1",
                    "customerId": "cus_1",
                    "feature": "api_calls",
                    "ts": "2024-01-01T00:00:00Z",
                    "createdAt": "2024-01-01T00:00:00Z",
                },
            },
        )
    )

    async with AsyncCommet(api_key="ck_test_123") as client:
        result = await client.usage.track(feature="api_calls", customer_id="cus_1", value=1)
        assert result.success is True
        assert result.data.feature == "api_calls"


@pytest.mark.asyncio
async def test_async_plans_list(mock_api: respx.MockRouter) -> None:
    mock_api.get("/plans").mock(
        return_value=Response(
            200,
            json={
                "success": True,
                "data": [
                    {
                        "id": "plan_1",
                        "code": "pro",
                        "name": "Pro",
                        "isPublic": True,
                        "isFree": False,
                        "isDefault": False,
                        "sortOrder": 1,
                        "prices": [],
                        "features": [],
                        "createdAt": "2024-01-01T00:00:00Z",
                    }
                ],
            },
        )
    )

    async with AsyncCommet(api_key="ck_test_123") as client:
        result = await client.plans.list()
        assert result.success is True
        assert len(result.data) == 1
        assert result.data[0].code == "pro"
