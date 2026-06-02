from __future__ import annotations

import logging

from ._async_http import AsyncCommetHTTPClient
from ._shared import API_VERSION
from .async_resources.addons import AsyncAddonsResource
from .async_resources.api_keys import AsyncApiKeysResource
from .async_resources.credit_packs import AsyncCreditPacksResource
from .async_resources.customers import AsyncCustomersResource
from .async_resources.features import AsyncFeaturesResource
from .async_resources.invoices import AsyncInvoicesResource
from .async_resources.plan_groups import AsyncPlanGroupsResource
from .async_resources.plans import AsyncPlansResource
from .async_resources.portal import AsyncPortalResource
from .async_resources.promo_codes import AsyncPromoCodesResource
from .async_resources.quota import AsyncQuotaResource
from .async_resources.seats import AsyncSeatsResource
from .async_resources.subscriptions import AsyncSubscriptionsResource
from .async_resources.transactions import AsyncTransactionsResource
from .async_resources.usage import AsyncUsageResource
from .resources.webhooks import Webhooks

logger = logging.getLogger("commet")


class AsyncCommet:
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

        self.addons = AsyncAddonsResource(self._http)
        self.api_keys = AsyncApiKeysResource(self._http)
        self.customers = AsyncCustomersResource(self._http)
        self.credit_packs = AsyncCreditPacksResource(self._http)
        self.features = AsyncFeaturesResource(self._http)
        self.invoices = AsyncInvoicesResource(self._http)
        self.plan_groups = AsyncPlanGroupsResource(self._http)
        self.plans = AsyncPlansResource(self._http)
        self.portal = AsyncPortalResource(self._http)
        self.promo_codes = AsyncPromoCodesResource(self._http)
        self.quota = AsyncQuotaResource(self._http)
        self.seats = AsyncSeatsResource(self._http)
        self.subscriptions = AsyncSubscriptionsResource(self._http)
        self.transactions = AsyncTransactionsResource(self._http)
        self.usage = AsyncUsageResource(self._http)
        self.webhooks = Webhooks()

        logger.debug("AsyncCommet client initialized")

    async def close(self) -> None:
        await self._http.close()

    async def __aenter__(self) -> AsyncCommet:
        return self

    async def __aexit__(self, *args: object) -> None:
        await self.close()
