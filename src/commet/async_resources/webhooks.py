from __future__ import annotations

from typing import Any

from .._async_http import AsyncCommetHTTPClient
from ..resources.webhooks import verify_and_parse_payload, verify_signature
from .generated_webhooks import AsyncGeneratedWebhooksResource


class AsyncWebhooks(AsyncGeneratedWebhooksResource):
    def __init__(self, http: AsyncCommetHTTPClient | None = None) -> None:
        if http is not None:
            super().__init__(http)

    def verify(self, *, payload: str, signature: str | None, secret: str) -> bool:
        return verify_signature(payload=payload, signature=signature, secret=secret)

    def verify_and_parse(
        self, *, raw_body: str, signature: str | None, secret: str
    ) -> dict[str, Any] | None:
        return verify_and_parse_payload(raw_body=raw_body, signature=signature, secret=secret)
