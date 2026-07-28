from __future__ import annotations

import logging

from ._async_http import AsyncCommetHTTPClient
from ._generated_async_resources import GeneratedAsyncResources
from ._shared import API_VERSION
from .async_resources.webhooks import AsyncWebhooks

logger = logging.getLogger("commet")


class AsyncCommet(GeneratedAsyncResources):
    def __init__(
        self,
        api_key: str,
        *,
        api_version: str = API_VERSION,
        timeout: float = 30.0,
        retries: int = 3,
        telemetry: bool = True,
    ) -> None:
        if not api_key:
            raise ValueError("Commet SDK: API key is required")

        if not api_key.startswith("ck_"):
            raise ValueError("Commet SDK: Invalid API key format. Expected format: ck_xxx...")

        self._http = AsyncCommetHTTPClient(
            api_key, api_version=api_version, timeout=timeout, retries=retries, telemetry=telemetry
        )

        self._init_resources(self._http)

        self.webhooks = AsyncWebhooks(self._http)

        logger.debug("AsyncCommet client initialized")

    async def close(self) -> None:
        await self._http.close()

    async def __aenter__(self) -> AsyncCommet:
        return self

    async def __aexit__(self, *args: object) -> None:
        await self.close()
