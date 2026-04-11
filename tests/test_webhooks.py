from __future__ import annotations

import hashlib
import hmac
import json

from commet.resources.webhooks import Webhooks


def _sign(payload: str, secret: str) -> str:
    return hmac.new(secret.encode(), payload.encode(), hashlib.sha256).hexdigest()


class TestWebhookVerification:
    def setup_method(self) -> None:
        self.webhooks = Webhooks()
        self.secret = "whsec_test_secret_key"
        self.payload = json.dumps({"event": "subscription.created", "data": {"id": "sub_123"}})
        self.valid_signature = _sign(self.payload, self.secret)

    def test_valid_signature_passes(self) -> None:
        assert self.webhooks.verify(
            payload=self.payload,
            signature=self.valid_signature,
            secret=self.secret,
        ) is True

    def test_invalid_signature_fails(self) -> None:
        assert self.webhooks.verify(
            payload=self.payload,
            signature="invalid_signature_value",
            secret=self.secret,
        ) is False

    def test_tampered_payload_fails(self) -> None:
        tampered = json.dumps({"event": "subscription.created", "data": {"id": "sub_999"}})
        assert self.webhooks.verify(
            payload=tampered,
            signature=self.valid_signature,
            secret=self.secret,
        ) is False

    def test_empty_signature_fails(self) -> None:
        assert self.webhooks.verify(
            payload=self.payload,
            signature=None,
            secret=self.secret,
        ) is False

    def test_empty_secret_fails(self) -> None:
        assert self.webhooks.verify(
            payload=self.payload,
            signature=self.valid_signature,
            secret="",
        ) is False

    def test_empty_payload_fails(self) -> None:
        assert self.webhooks.verify(
            payload="",
            signature=self.valid_signature,
            secret=self.secret,
        ) is False

    def test_verify_and_parse_valid(self) -> None:
        result = self.webhooks.verify_and_parse(
            raw_body=self.payload,
            signature=self.valid_signature,
            secret=self.secret,
        )
        assert result is not None
        assert result["event"] == "subscription.created"
        assert result["data"]["id"] == "sub_123"

    def test_verify_and_parse_invalid_signature(self) -> None:
        result = self.webhooks.verify_and_parse(
            raw_body=self.payload,
            signature="bad_sig",
            secret=self.secret,
        )
        assert result is None
