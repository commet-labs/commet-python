from __future__ import annotations

import pytest
import respx
from httpx import Response

from commet import Commet
from commet.types import TestClock as TestClockModel


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

        assert isinstance(result, TestClockModel)
        assert result.simulated_time is None
        assert result.is_active is False
        assert result.now == "2026-06-01T00:00:00Z"
