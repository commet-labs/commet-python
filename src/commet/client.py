from __future__ import annotations

import logging

from ._http import CommetHTTPClient
from ._shared import API_VERSION
from .resources.addons import AddonsResource
from .resources.api_keys import ApiKeysResource
from .resources.credit_packs import CreditPacksResource
from .resources.customers import CustomersResource
from .resources.features import FeaturesResource
from .resources.invoices import InvoicesResource
from .resources.plan_groups import PlanGroupsResource
from .resources.plans import PlansResource
from .resources.portal import PortalResource
from .resources.promo_codes import PromoCodesResource
from .resources.quota import QuotaResource
from .resources.seats import SeatsResource
from .resources.subscriptions import SubscriptionsResource
from .resources.transactions import TransactionsResource
from .resources.usage import UsageResource
from .resources.webhooks import Webhooks

logger = logging.getLogger("commet")


class Commet:
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

        self.addons = AddonsResource(self._http)
        self.api_keys = ApiKeysResource(self._http)
        self.customers = CustomersResource(self._http)
        self.credit_packs = CreditPacksResource(self._http)
        self.features = FeaturesResource(self._http)
        self.invoices = InvoicesResource(self._http)
        self.plan_groups = PlanGroupsResource(self._http)
        self.plans = PlansResource(self._http)
        self.portal = PortalResource(self._http)
        self.promo_codes = PromoCodesResource(self._http)
        self.quota = QuotaResource(self._http)
        self.seats = SeatsResource(self._http)
        self.subscriptions = SubscriptionsResource(self._http)
        self.transactions = TransactionsResource(self._http)
        self.usage = UsageResource(self._http)
        self.webhooks = Webhooks(self._http)

        logger.debug("Commet client initialized")

    def close(self) -> None:
        self._http.close()

    def __enter__(self) -> Commet:
        return self

    def __exit__(self, *args: object) -> None:
        self.close()
