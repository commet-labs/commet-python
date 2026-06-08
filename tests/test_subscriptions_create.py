from __future__ import annotations

import json

import pytest
import respx
from httpx import Response

from commet import Commet
from commet.async_client import AsyncCommet
from commet.types import Subscription

_INTRO_OFFER = {
    "discount_type": "percentage",
    "discount_value": 1000,
    "duration_cycles": 3,
}


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
    def test_create_sends_custom_intro_offer_as_camel_case(
        self, mock_api: respx.MockRouter
    ) -> None:
        route = mock_api.post("/subscriptions").mock(return_value=_create_response())
        with Commet(api_key="ck_test_123") as client:
            result = client.subscriptions.create(
                customer_id="cus_1",
                plan_code="pro",
                intro_offer=_INTRO_OFFER,
            )
            assert result.success is True
            assert isinstance(result.data, Subscription)

        sent = json.loads(route.calls.last.request.content)
        assert sent["introOffer"] == {
            "discountType": "percentage",
            "discountValue": 1000,
            "durationCycles": 3,
        }
        assert "intro_offer" not in sent
        assert "discount_type" not in sent["introOffer"]
        assert "discount_value" not in sent["introOffer"]
        assert "duration_cycles" not in sent["introOffer"]


@pytest.mark.asyncio
class TestAsyncCreate:
    async def test_create_sends_custom_intro_offer_as_camel_case(
        self, mock_api: respx.MockRouter
    ) -> None:
        route = mock_api.post("/subscriptions").mock(return_value=_create_response())
        async with AsyncCommet(api_key="ck_test_123") as client:
            result = await client.subscriptions.create(
                customer_id="cus_1",
                plan_code="pro",
                intro_offer=_INTRO_OFFER,
            )
            assert result.success is True
            assert isinstance(result.data, Subscription)

        sent = json.loads(route.calls.last.request.content)
        assert sent["introOffer"] == {
            "discountType": "percentage",
            "discountValue": 1000,
            "durationCycles": 3,
        }
        assert "intro_offer" not in sent
        assert "discount_type" not in sent["introOffer"]
        assert "discount_value" not in sent["introOffer"]
        assert "duration_cycles" not in sent["introOffer"]
