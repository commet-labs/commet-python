from __future__ import annotations

import logging
from typing import Literal

from ._customer import CustomerContext
from ._http import CommetHTTPClient, _BASE_URLS
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

Environment = Literal["sandbox", "production"]


class Commet:
    """Commet SDK client.

    Usage::

        from commet import Commet

        commet = Commet(api_key="ck_xxx")

        # Direct resource access
        commet.customers.create(email="user@example.com")
        commet.usage.track(feature="api_calls", external_id="user_123")

        # Customer-scoped context
        customer = commet.customer("user_123")
        customer.usage.track("api_calls")

        # Context manager
        with Commet(api_key="ck_xxx") as commet:
            commet.usage.track(feature="api_calls", external_id="user_123")
    """

    def __init__(
        self,
        api_key: str,
        *,
        environment: Environment = "sandbox",
        timeout: float = 30.0,
        retries: int = 3,
    ) -> None:
        if not api_key:
            raise ValueError("Commet SDK: API key is required")

        if not api_key.startswith("ck_"):
            raise ValueError("Commet SDK: Invalid API key format. Expected format: ck_xxx...")

        if environment not in _BASE_URLS:
            raise ValueError(
                f"Commet SDK: Invalid environment '{environment}'. Must be 'sandbox' or 'production'"
            )

        self._environment = environment
        self._http = CommetHTTPClient(
            api_key, environment, timeout=timeout, retries=retries
        )

        self.customers = CustomersResource(self._http)
        self.credit_packs = CreditPacksResource(self._http)
        self.plans = PlansResource(self._http)
        self.usage = UsageResource(self._http)
        self.seats = SeatsResource(self._http)
        self.subscriptions = SubscriptionsResource(self._http)
        self.portal = PortalResource(self._http)
        self.features = FeaturesResource(self._http)
        self.webhooks = Webhooks()

        logger.debug("Initialized in %s mode", environment)

    def close(self) -> None:
        self._http.close()

    def __enter__(self) -> Commet:
        return self

    def __exit__(self, *args: object) -> None:
        self.close()

    def customer(self, external_id: str) -> CustomerContext:
        """Create a customer-scoped context for cleaner API usage."""
        return CustomerContext(
            external_id,
            features=self.features,
            seats=self.seats,
            usage=self.usage,
            subscriptions=self.subscriptions,
            portal=self.portal,
        )

    @property
    def environment(self) -> str:
        return self._environment

    def is_sandbox(self) -> bool:
        return self._environment == "sandbox"

    def is_production(self) -> bool:
        return self._environment == "production"
