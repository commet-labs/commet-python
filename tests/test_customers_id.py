from __future__ import annotations

import json

import pytest
import respx
from httpx import Response

from commet.client import Commet

CUSTOMER_OK = {
    "success": True,
    "data": {
        "id": "cus_123",
        "organizationId": "org_1",
        "billingEmail": "user@example.com",
        "createdAt": "2024-01-01T00:00:00Z",
        "updatedAt": "2024-01-01T00:00:00Z",
    },
}


@pytest.fixture
def mock_api() -> respx.MockRouter:
    with respx.mock(base_url="https://commet.co/api/v1") as mock:
        yield mock


def _last_body(mock_api: respx.MockRouter) -> dict:
    return json.loads(mock_api.calls.last.request.content)


def test_create_sends_id(mock_api: respx.MockRouter) -> None:
    mock_api.post("/customers").mock(return_value=Response(200, json=CUSTOMER_OK))

    client = Commet(api_key="ck_test_123")
    client.customers.create(email="user@example.com", id="ext_123")

    body = _last_body(mock_api)
    assert body["id"] == "ext_123"
    assert body["email"] == "user@example.com"


def test_create_without_id_omits_it(mock_api: respx.MockRouter) -> None:
    mock_api.post("/customers").mock(return_value=Response(200, json=CUSTOMER_OK))

    client = Commet(api_key="ck_test_123")
    client.customers.create(email="user@example.com")

    assert "id" not in _last_body(mock_api)


def test_create_batch_sends_id(mock_api: respx.MockRouter) -> None:
    mock_api.post("/customers/batch").mock(
        return_value=Response(200, json={"success": True, "data": {"successful": [], "failed": []}})
    )

    client = Commet(api_key="ck_test_123")
    client.customers.create_batch(
        customers=[
            {"email": "a@example.com", "id": "ext_a"},
            {"email": "b@example.com"},
        ]
    )

    body = _last_body(mock_api)
    assert body["customers"][0]["id"] == "ext_a"
    assert "id" not in body["customers"][1]


def test_addons_list_active(mock_api: respx.MockRouter) -> None:
    route = mock_api.get("/addons/active").mock(
        return_value=Response(200, json={"success": True, "data": []})
    )

    client = Commet(api_key="ck_test_123")
    client.addons.list_active(customer_id="cus_1")

    assert route.called
    assert mock_api.calls.last.request.url.params["customerId"] == "cus_1"
