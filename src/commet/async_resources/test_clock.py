# ruff: noqa: E501

from __future__ import annotations

from .._async_http import AsyncCommetHTTPClient
from .._http import ApiResponse
from .._shared import build_body
from ..types import (
    TestClock,
    TestClockBilling,
    _parse,
)


class AsyncTestClockResource:
    def __init__(self, http: AsyncCommetHTTPClient) -> None:
        self._http = http

    async def get(self) -> ApiResponse[TestClock]:
        """Returns the organization's current test clock state. Sandbox only."""
        return _parse(await self._http.get("/test-clock"), TestClock)

    async def advance(
        self,
        *,
        advance_days: int | None = None,
        frozen_time: str | None = None,
        idempotency_key: str | None = None,
    ) -> ApiResponse[TestClock]:
        """Moves the test clock forward, by a number of days (advanceDays) or to an absolute instant (frozenTime). The clock can only move forward. Sandbox only."""
        body = build_body(advance_days=advance_days, frozen_time=frozen_time)
        return _parse(
            await self._http.post("/test-clock", body, idempotency_key=idempotency_key), TestClock
        )

    async def process_billing(
        self, *, idempotency_key: str | None = None
    ) -> ApiResponse[TestClockBilling]:
        """Discovers customers due for billing at the org's current (simulated) time and enqueues a billing cycle for each — renewals, expired trials, pending cancellations. Enqueueing is asynchronous. Sandbox only."""
        return _parse(
            await self._http.post("/test-clock/process-billing", idempotency_key=idempotency_key),
            TestClockBilling,
        )
