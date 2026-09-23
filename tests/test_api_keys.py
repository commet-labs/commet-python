from __future__ import annotations

import json

import pytest
import respx
from httpx import Response

from commet import Commet
from commet.async_client import AsyncCommet


@pytest.mark.parametrize(
    ("permissions", "expected"),
    [
        (None, None),
        ({}, {}),
        ({"plan_group": ["read"]}, {"plan_group": ["read"]}),
    ],
)
def test_create_api_key_permissions_wire(
    permissions: dict[str, list[str]] | None, expected: dict[str, list[str]] | None
) -> None:
    with respx.mock(base_url="https://commet.co/api/v1") as mock:
        route = mock.post("/api-keys").mock(return_value=Response(201, json={}))
        with Commet(api_key="ck_test_123") as client:
            client.api_keys.create(name="Example", permissions=permissions)

        body = json.loads(route.calls.last.request.content)
        assert ("permissions" in body) == (expected is not None)
        if expected is not None:
            assert body["permissions"] == expected


@pytest.mark.asyncio
async def test_async_create_api_key_preserves_permission_resource_ids() -> None:
    with respx.mock(base_url="https://commet.co/api/v1") as mock:
        route = mock.post("/api-keys").mock(return_value=Response(201, json={}))
        async with AsyncCommet(api_key="ck_test_123") as client:
            await client.api_keys.create(name="Example", permissions={"credit_pack": ["read"]})

        body = json.loads(route.calls.last.request.content)
        assert body["permissions"] == {"credit_pack": ["read"]}
