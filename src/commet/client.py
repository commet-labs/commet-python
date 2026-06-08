from __future__ import annotations

import logging

from ._generated_resources import GeneratedSyncResources
from ._http import CommetHTTPClient
from ._shared import API_VERSION
from .resources.usage import UsageResource
from .resources.webhooks import Webhooks

logger = logging.getLogger("commet")


class Commet(GeneratedSyncResources):
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

        self._http = CommetHTTPClient(
            api_key, api_version=api_version, timeout=timeout, retries=retries, telemetry=telemetry
        )

        self._init_resources(self._http)

        self.usage = UsageResource(self._http)
        self.webhooks = Webhooks(self._http)

        logger.debug("Commet client initialized")

    def close(self) -> None:
        self._http.close()

    def __enter__(self) -> Commet:
        return self

    def __exit__(self, *args: object) -> None:
        self.close()
