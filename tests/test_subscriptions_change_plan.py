from __future__ import annotations

import json

import pytest
import respx
from httpx import Response

from commet import Commet
from commet.async_client import AsyncCommet
from commet.types import PlanChangeVariant1

_SUCCESS_URL = "https://app.example.com/billing/success"


def _change_plan_response() -> Response:
    return Response(
        200,
        json={
            "outcome": "requires_checkout",
            "requiresCheckout": True,
            "checkoutUrl": "https://checkout.example.com/abc",
        },
    )


@pytest.fixture
def mock_api() -> respx.MockRouter:
    with respx.mock(base_url="https://commet.co/api/v1") as mock:
        yield mock


class TestChangePlan:
    def test_change_plan_sends_success_url_as_camel_case(self, mock_api: respx.MockRouter) -> None:
        route = mock_api.post("/subscriptions/sub_1/change-plan").mock(
            return_value=_change_plan_response()
        )
        with Commet(api_key="ck_test_123") as client:
            result = client.subscriptions.change_plan(
                "sub_1", new_plan_id="plan_2", success_url=_SUCCESS_URL
            )
            assert isinstance(result, PlanChangeVariant1)

        sent = json.loads(route.calls.last.request.content)
        assert sent["successUrl"] == _SUCCESS_URL
        assert sent["newPlanId"] == "plan_2"
        assert "success_url" not in sent
        assert "new_plan_id" not in sent


@pytest.mark.asyncio
class TestAsyncChangePlan:
    async def test_change_plan_sends_success_url_as_camel_case(
        self, mock_api: respx.MockRouter
    ) -> None:
        route = mock_api.post("/subscriptions/sub_1/change-plan").mock(
            return_value=_change_plan_response()
        )
        async with AsyncCommet(api_key="ck_test_123") as client:
            result = await client.subscriptions.change_plan(
                "sub_1", new_plan_id="plan_2", success_url=_SUCCESS_URL
            )
            assert isinstance(result, PlanChangeVariant1)

        sent = json.loads(route.calls.last.request.content)
        assert sent["successUrl"] == _SUCCESS_URL
        assert sent["newPlanId"] == "plan_2"
        assert "success_url" not in sent
        assert "new_plan_id" not in sent
