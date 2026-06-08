from __future__ import annotations

import builtins
import hashlib
import hmac
import json
from typing import Any

from .._http import ApiResponse, CommetHTTPClient
from .._preserved_types import (
    DeleteResult,
    WebhookEndpoint,
    WebhookEndpointCreated,
    WebhookTestResult,
    _parse,
    _parse_list,
)
from .._shared import build_body


def sign_payload(payload: str, secret: str) -> str:
    return hmac.new(secret.encode(), payload.encode(), hashlib.sha256).hexdigest()


def verify_signature(*, payload: str, signature: str | None, secret: str) -> bool:
    if not signature or not secret or not payload:
        return False
    return hmac.compare_digest(signature, sign_payload(payload, secret))


def verify_and_parse_payload(
    *, raw_body: str, signature: str | None, secret: str
) -> dict[str, Any] | None:
    if not verify_signature(payload=raw_body, signature=signature, secret=secret):
        return None
    try:
        parsed = json.loads(raw_body)
    except (json.JSONDecodeError, TypeError):
        return None
    if not isinstance(parsed, dict):
        return None
    return parsed


class Webhooks:
    def __init__(self, http: CommetHTTPClient | None = None) -> None:
        self._http = http

    def verify(self, *, payload: str, signature: str | None, secret: str) -> bool:
        return verify_signature(payload=payload, signature=signature, secret=secret)

    def verify_and_parse(
        self, *, raw_body: str, signature: str | None, secret: str
    ) -> dict[str, Any] | None:
        return verify_and_parse_payload(raw_body=raw_body, signature=signature, secret=secret)

    def list(
        self,
        *,
        limit: int | None = None,
        cursor: str | None = None,
    ) -> ApiResponse[list[WebhookEndpoint]]:
        assert self._http is not None
        return _parse_list(
            self._http.get("/webhooks", build_body(limit=limit, cursor=cursor)), WebhookEndpoint
        )

    def create(
        self,
        *,
        url: str,
        events: builtins.list[str],
        description: str | None = None,
        api_version: str | None = None,
        idempotency_key: str | None = None,
    ) -> ApiResponse[WebhookEndpointCreated]:
        assert self._http is not None
        return _parse(
            self._http.post(
                "/webhooks",
                build_body(
                    url=url, events=events, description=description, api_version=api_version
                ),
                idempotency_key=idempotency_key,
            ),
            WebhookEndpointCreated,
        )

    def get(self, webhook_id: str) -> ApiResponse[WebhookEndpoint]:
        assert self._http is not None
        return _parse(self._http.get(f"/webhooks/{webhook_id}"), WebhookEndpoint)

    def update(
        self,
        webhook_id: str,
        *,
        url: str | None = None,
        events: builtins.list[str] | None = None,
        description: str | None = None,
        is_active: bool | None = None,
        api_version: str | None = None,
        idempotency_key: str | None = None,
    ) -> ApiResponse[WebhookEndpoint]:
        assert self._http is not None
        return _parse(
            self._http.put(
                f"/webhooks/{webhook_id}",
                build_body(
                    url=url,
                    events=events,
                    description=description,
                    is_active=is_active,
                    api_version=api_version,
                ),
                idempotency_key=idempotency_key,
            ),
            WebhookEndpoint,
        )

    def delete(
        self,
        webhook_id: str,
        *,
        idempotency_key: str | None = None,
    ) -> ApiResponse[DeleteResult]:
        assert self._http is not None
        return _parse(
            self._http.delete(f"/webhooks/{webhook_id}", idempotency_key=idempotency_key),
            DeleteResult,
        )

    def test(
        self,
        webhook_id: str,
        *,
        idempotency_key: str | None = None,
    ) -> ApiResponse[WebhookTestResult]:
        assert self._http is not None
        return _parse(
            self._http.post(f"/webhooks/{webhook_id}/test", idempotency_key=idempotency_key),
            WebhookTestResult,
        )
