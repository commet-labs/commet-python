from __future__ import annotations

import pytest

from commet import Commet
from commet.async_client import AsyncCommet


class TestClientInitialization:
    @pytest.mark.parametrize(
        "prefix", ["ck_", "ck_live_", "ck_sandbox_", "rk_", "rk_live_", "rk_sandbox_"]
    )
    def test_valid_key(self, prefix: str) -> None:
        with Commet(api_key=f"{prefix}test_123") as client:
            assert client is not None

    def test_rejects_invalid_api_keys(self) -> None:
        with pytest.raises(ValueError, match="API key is required"):
            Commet(api_key="")
        with pytest.raises(ValueError, match="Invalid API key format"):
            Commet(api_key="sk_invalid_prefix")

    @pytest.mark.parametrize(
        "prefix", ["ck_", "ck_live_", "ck_sandbox_", "rk_", "rk_live_", "rk_sandbox_"]
    )
    @pytest.mark.asyncio
    async def test_async_client_initializes(self, prefix: str) -> None:
        async with AsyncCommet(api_key=f"{prefix}test_123") as client:
            assert client is not None
