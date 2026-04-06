from __future__ import annotations

import hashlib
import hmac
import json
from typing import Any


class Webhooks:
    """Webhook signature verification.

    Usage::

        from commet import Webhooks

        webhooks = Webhooks()

        is_valid = webhooks.verify(
            payload=raw_body,
            signature=request.headers["x-commet-signature"],
            secret=WEBHOOK_SECRET,
        )
    """

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
