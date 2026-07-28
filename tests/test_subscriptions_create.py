from __future__ import annotations

import json

import pytest
import respx
from httpx import Response

from commet import Commet
from commet.async_client import AsyncCommet
from commet.types import CreatedSubscription


def _create_response() -> Response:
    return Response(
        200,
        json={
            "success": True,
            "data": {
                "id": "sub_1",
                "customerId": "cus_1",
                "status": "active",
            },
        },
    )


@pytest.fixture
def mock_api() -> respx.MockRouter:
    with respx.mock(base_url="https://commet.co/api/v1") as mock:
        yield mock


class TestCreate:
    def test_create_sends_offer_id_from_contract(self, mock_api: respx.MockRouter) -> None:
        route = mock_api.post("/subscriptions").mock(return_value=_create_response())
        with Commet(api_key="ck_test_123") as client:
            result = client.subscriptions.create(
                customer_id="cus_1",
                plan_code="pro",
                offer_id="offer_1",
            )
            assert isinstance(result, CreatedSubscription)

        sent = json.loads(route.calls.last.request.content)
        assert sent["offerId"] == "offer_1"
        assert "introOffer" not in sent


@pytest.mark.asyncio
class TestAsyncCreate:
    async def test_create_sends_offer_id_from_contract(self, mock_api: respx.MockRouter) -> None:
        route = mock_api.post("/subscriptions").mock(return_value=_create_response())
        async with AsyncCommet(api_key="ck_test_123") as client:
            result = await client.subscriptions.create(
                customer_id="cus_1",
                plan_code="pro",
                offer_id="offer_1",
            )
            assert isinstance(result, CreatedSubscription)

        sent = json.loads(route.calls.last.request.content)
        assert sent["offerId"] == "offer_1"
        assert "introOffer" not in sent
