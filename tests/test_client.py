from __future__ import annotations

import pytest

from commet import Commet
from commet.async_client import AsyncCommet


class TestClientInitialization:
    def test_valid_key(self) -> None:
        with Commet(api_key="ck_test_123") as client:
            assert client is not None

    def test_rejects_invalid_api_keys(self) -> None:
        with pytest.raises(ValueError, match="API key is required"):
            Commet(api_key="")
        with pytest.raises(ValueError, match="Invalid API key format"):
            Commet(api_key="sk_invalid_prefix")

    def test_async_client_initializes(self) -> None:
        client = AsyncCommet(api_key="ck_test_123")
        assert client is not None
