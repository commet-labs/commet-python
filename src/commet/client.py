from __future__ import annotations

import logging

from ._customer import CustomerContext
from ._http import CommetHTTPClient
from ._shared import API_VERSION
from .resources.addons import AddonsResource
from .resources.credit_packs import CreditPacksResource
from .resources.customers import CustomersResource
from .resources.features import FeaturesResource
from .resources.plans import PlansResource
from .resources.portal import PortalResource
from .resources.seats import SeatsResource
from .resources.subscriptions import SubscriptionsResource
from .resources.usage import UsageResource
from .resources.webhooks import Webhooks

logger = logging.getLogger("commet")


class Commet:
    """Commet SDK client.

    Usage::

        from commet import Commet

        commet = Commet(api_key="ck_xxx")

        # Direct resource access
        commet.customers.create(email="user@example.com")
        commet.usage.track(feature="api_calls", customer_id="user_123")

        # Customer-scoped context
        customer = commet.customer("user_123")
        customer.usage.track("api_calls")

        # Context manager
        with Commet(api_key="ck_xxx") as commet:
            commet.usage.track(feature="api_calls", customer_id="user_123")
    """

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
        self.customers = CustomersResource(self._http)
        self.credit_packs = CreditPacksResource(self._http)
        self.plans = PlansResource(self._http)
        self.usage = UsageResource(self._http)
        self.seats = SeatsResource(self._http)
        self.subscriptions = SubscriptionsResource(self._http)
        self.portal = PortalResource(self._http)
        self.features = FeaturesResource(self._http)
        self.webhooks = Webhooks()

        logger.debug("Commet client initialized")

    def close(self) -> None:
        self._http.close()

    def __enter__(self) -> Commet:
        return self

    def __exit__(self, *args: object) -> None:
        self.close()

    def customer(self, customer_id: str) -> CustomerContext:
        """Create a customer-scoped context for cleaner API usage."""
        return CustomerContext(
            customer_id,
            features=self.features,
            seats=self.seats,
            usage=self.usage,
            subscriptions=self.subscriptions,
            portal=self.portal,
        )
