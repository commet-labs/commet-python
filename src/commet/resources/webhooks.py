from __future__ import annotations

import hashlib
import hmac
import json
from typing import Any

from .._http import ApiResponse, CommetHTTPClient
from .._shared import build_body


class Webhooks:
    def __init__(self, http: CommetHTTPClient | None = None) -> None:
        self._http = http

    def verify(self, *, payload: str, signature: str | None, secret: str) -> bool:
        if not signature or not secret or not payload:
            return False

        expected = self._sign(payload, secret)
        return hmac.compare_digest(signature, expected)

    def verify_and_parse(
        self, *, raw_body: str, signature: str | None, secret: str
    ) -> dict[str, Any] | None:
        if not self.verify(payload=raw_body, signature=signature, secret=secret):
            return None

        try:
            return json.loads(raw_body)
        except (json.JSONDecodeError, TypeError):
            return None

    def _sign(self, payload: str, secret: str) -> str:
        return hmac.new(secret.encode(), payload.encode(), hashlib.sha256).hexdigest()

    def list(
        self,
        *,
        limit: int | None = None,
        cursor: str | None = None,
    ) -> ApiResponse[Any]:
        return self._http.get("/webhooks", build_body(limit=limit, cursor=cursor))

    def create(
        self,
        *,
        url: str,
        events: list[str],
        description: str | None = None,
        idempotency_key: str | None = None,
    ) -> ApiResponse[Any]:
        return self._http.post(
            "/webhooks",
            build_body(url=url, events=events, description=description),
            idempotency_key=idempotency_key,
        )

    def delete(
        self,
        webhook_id: str,
        *,
        idempotency_key: str | None = None,
    ) -> ApiResponse[Any]:
        return self._http.delete(f"/webhooks/{webhook_id}", idempotency_key=idempotency_key)

    def test(
        self,
        webhook_id: str,
        *,
        idempotency_key: str | None = None,
    ) -> ApiResponse[Any]:
        return self._http.post(
            f"/webhooks/{webhook_id}/test", idempotency_key=idempotency_key,
        )
