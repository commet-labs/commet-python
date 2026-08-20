from __future__ import annotations

import json

import pytest
import respx
from httpx import Response

from commet import Commet
from commet.async_client import AsyncCommet
from commet.types import TestClock as TestClockModel
from commet.types import TestClockRun


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
                        "latestRun": None,
                        "object": "test_clock",
                        "livemode": False,
                    },
                },
            )
        )
        with Commet(api_key="ck_test_123") as client:
            result = client.test_clock.get()

        assert isinstance(result, TestClockModel)
        assert result.simulated_time is None
        assert result.is_active is False
        assert result.now == "2026-06-01T00:00:00Z"


class TestAdvance:
    def test_advance_by_days_sends_only_provided_field(self, mock_api: respx.MockRouter) -> None:
        route = mock_api.post("/test-clock").mock(
            return_value=Response(
                200,
                json={
                    "success": True,
                    "data": {
                        "id": "tcr_1",
                        "status": "pending",
                        "startedAtTime": "2026-06-01T00:00:00Z",
                        "targetTime": "2026-06-15T00:00:00Z",
                        "estimatedDeadlineCount": 0,
                        "completedDeadlineCount": 0,
                        "failedDeadlineCount": 0,
                        "error": None,
                        "items": [],
                        "object": "test_clock_run",
                        "livemode": False,
                    },
                },
            )
        )
        with Commet(api_key="ck_test_123") as client:
            result = client.test_clock.advance(advance_days=14)

        assert isinstance(result, TestClockRun)
        assert result.status == "pending"

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
                        "id": "tcr_2",
                        "status": "pending",
                        "startedAtTime": "2026-06-01T00:00:00Z",
                        "targetTime": "2027-01-01T00:00:00Z",
                        "estimatedDeadlineCount": 0,
                        "completedDeadlineCount": 0,
                        "failedDeadlineCount": 0,
                        "error": None,
                        "items": [],
                        "object": "test_clock_run",
                        "livemode": False,
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
                    "data": None,
                },
            )
        )
        with Commet(api_key="ck_test_123") as client:
            result = client.test_clock.process_billing()

        assert result is None

        assert route.calls.last.request.content == b""


@pytest.mark.asyncio
class TestAsyncTestClock:
    async def test_advance_parses_and_sends_camel_case(self, mock_api: respx.MockRouter) -> None:
        route = mock_api.post("/test-clock").mock(
            return_value=Response(
                200,
                json={
                    "success": True,
                    "data": {
                        "id": "tcr_3",
                        "status": "pending",
                        "startedAtTime": "2026-06-01T00:00:00Z",
                        "targetTime": "2026-07-01T00:00:00Z",
                        "estimatedDeadlineCount": 0,
                        "completedDeadlineCount": 0,
                        "failedDeadlineCount": 0,
                        "error": None,
                        "items": [],
                        "object": "test_clock_run",
                        "livemode": False,
                    },
                },
            )
        )
        async with AsyncCommet(api_key="ck_test_123") as client:
            result = await client.test_clock.advance(advance_days=30)

        assert isinstance(result, TestClockRun)
        assert result.status == "pending"
        sent = json.loads(route.calls.last.request.content)
        assert sent == {"advanceDays": 30}

    async def test_process_billing_returns_no_result(self, mock_api: respx.MockRouter) -> None:
        mock_api.post("/test-clock/process-billing").mock(
            return_value=Response(
                200,
                json={
                    "success": True,
                    "data": None,
                },
            )
        )
        async with AsyncCommet(api_key="ck_test_123") as client:
            result = await client.test_clock.process_billing()

        assert result is None
