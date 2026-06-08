from __future__ import annotations

import json

import pytest
import respx
from httpx import Response

from commet import Commet
from commet.async_client import AsyncCommet
from commet.types import TestClock as TestClockModel
from commet.types import TestClockBilling as TestClockBillingModel


@pytest.fixture
def mock_api() -> respx.MockRouter:
    with respx.mock(base_url="https://commet.co/api/v1") as mock:
        yield mock


class TestGet:
    def test_get_parses_clock_state_with_nullable_simulated_time(
        self, mock_api: respx.MockRouter
    ) -> None:
        mock_api.get("/test-clock").mock(
            return_value=Response(
                200,
                json={
                    "success": True,
                    "data": {
                        "simulatedTime": None,
                        "isActive": False,
                        "now": "2026-06-01T00:00:00Z",
                        "object": "test_clock",
                    },
                },
            )
        )
        with Commet(api_key="ck_test_123") as client:
            result = client.test_clock.get()

        assert isinstance(result.data, TestClockModel)
        assert result.data.simulated_time is None
        assert result.data.is_active is False
        assert result.data.now == "2026-06-01T00:00:00Z"


class TestAdvance:
    def test_advance_by_days_sends_only_provided_field(self, mock_api: respx.MockRouter) -> None:
        route = mock_api.post("/test-clock").mock(
            return_value=Response(
                200,
                json={
                    "success": True,
                    "data": {
                        "simulatedTime": "2026-06-15T00:00:00Z",
                        "isActive": True,
                        "now": "2026-06-15T00:00:00Z",
                    },
                },
            )
        )
        with Commet(api_key="ck_test_123") as client:
            result = client.test_clock.advance(advance_days=14)

        assert isinstance(result.data, TestClockModel)
        assert result.data.is_active is True

        sent = json.loads(route.calls.last.request.content)
        assert sent == {"advanceDays": 14}
        assert "frozenTime" not in sent

    def test_advance_to_frozen_time(self, mock_api: respx.MockRouter) -> None:
        route = mock_api.post("/test-clock").mock(
            return_value=Response(
                200,
                json={
                    "success": True,
                    "data": {
                        "simulatedTime": "2027-01-01T00:00:00Z",
                        "isActive": True,
                        "now": "2027-01-01T00:00:00Z",
                    },
                },
            )
        )
        with Commet(api_key="ck_test_123") as client:
            client.test_clock.advance(frozen_time="2027-01-01T00:00:00Z")

        sent = json.loads(route.calls.last.request.content)
        assert sent == {"frozenTime": "2027-01-01T00:00:00Z"}
        assert "advanceDays" not in sent


class TestProcessBilling:
    def test_no_param_post_sends_no_json_body(self, mock_api: respx.MockRouter) -> None:
        route = mock_api.post("/test-clock/process-billing").mock(
            return_value=Response(
                200,
                json={
                    "success": True,
                    "data": {
                        "customersFound": 3,
                        "enqueued": 3,
                        "failed": 0,
                        "object": "test_clock",
                    },
                },
            )
        )
        with Commet(api_key="ck_test_123") as client:
            result = client.test_clock.process_billing()

        assert isinstance(result.data, TestClockBillingModel)
        assert result.data.customers_found == 3
        assert result.data.enqueued == 3
        assert result.data.failed == 0

        # A no-param POST must not serialize an empty/literal-null JSON body.
        assert route.calls.last.request.content in (b"", b"null")


@pytest.mark.asyncio
class TestAsyncTestClock:
    async def test_advance_parses_and_sends_camel_case(self, mock_api: respx.MockRouter) -> None:
        route = mock_api.post("/test-clock").mock(
            return_value=Response(
                200,
                json={
                    "success": True,
                    "data": {
                        "simulatedTime": "2026-07-01T00:00:00Z",
                        "isActive": True,
                        "now": "2026-07-01T00:00:00Z",
                    },
                },
            )
        )
        async with AsyncCommet(api_key="ck_test_123") as client:
            result = await client.test_clock.advance(advance_days=30)

        assert isinstance(result.data, TestClockModel)
        assert result.data.is_active is True
        sent = json.loads(route.calls.last.request.content)
        assert sent == {"advanceDays": 30}

    async def test_process_billing_parses_counts(self, mock_api: respx.MockRouter) -> None:
        mock_api.post("/test-clock/process-billing").mock(
            return_value=Response(
                200,
                json={
                    "success": True,
                    "data": {"customersFound": 1, "enqueued": 0, "failed": 1},
                },
            )
        )
        async with AsyncCommet(api_key="ck_test_123") as client:
            result = await client.test_clock.process_billing()

        assert isinstance(result.data, TestClockBillingModel)
        assert result.data.customers_found == 1
        assert result.data.failed == 1
