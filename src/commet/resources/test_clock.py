# ruff: noqa: E501

from __future__ import annotations

from .._http import CommetHTTPClient
from .._shared import build_body
from ..types import (
    TestClock,
    TestClockRun,
    _data,
    _parse_data,
)


class TestClockResource:
    def __init__(self, http: CommetHTTPClient) -> None:
        self._http = http

    def process_billing(self, *, idempotency_key: str | None = None) -> None:
        """
        Deprecated. POST /test-clock now advances time and processes every due billing deadline in one durable run.
        Deprecated.
        """
        return _data(
            self._http.post("/test-clock/process-billing", idempotency_key=idempotency_key)
        )

    def get(self) -> TestClock:
        """Returns the organization's current test clock state and latest durable run. Sandbox only."""
        return _parse_data(self._http.get("/test-clock"), TestClock)

    def advance(
        self,
        *,
        advance_days: int | None = None,
        frozen_time: str | None = None,
        idempotency_key: str | None = None,
    ) -> TestClockRun:
        """Starts a durable run that moves the test clock forward and processes every billing deadline due before the target time. Poll GET /test-clock for progress and terminal results. Sandbox only."""
        body = build_body(advance_days=advance_days, frozen_time=frozen_time)
        return _parse_data(
            self._http.post("/test-clock", body, idempotency_key=idempotency_key), TestClockRun
        )
