from __future__ import annotations

import hashlib
import hmac
import json
from typing import Any

from .._http import CommetHTTPClient
from .generated_webhooks import GeneratedWebhooksResource


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


class Webhooks(GeneratedWebhooksResource):
    def __init__(self, http: CommetHTTPClient | None = None) -> None:
        self._http = http

    def verify(self, *, payload: str, signature: str | None, secret: str) -> bool:
        return verify_signature(payload=payload, signature=signature, secret=secret)

    def verify_and_parse(
        self, *, raw_body: str, signature: str | None, secret: str
    ) -> dict[str, Any] | None:
        return verify_and_parse_payload(raw_body=raw_body, signature=signature, secret=secret)
