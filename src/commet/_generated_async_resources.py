# ruff: noqa: E501

from __future__ import annotations

from ._async_http import AsyncCommetHTTPClient
from .async_resources.addons import AsyncAddonsResource
from .async_resources.api_keys import AsyncApiKeysResource
from .async_resources.credit_packs import AsyncCreditPacksResource
from .async_resources.customers import AsyncCustomersResource
from .async_resources.feature_access import AsyncFeatureAccessResource
from .async_resources.features import AsyncFeaturesResource
from .async_resources.invoices import AsyncInvoicesResource
from .async_resources.payments import AsyncPaymentsResource
from .async_resources.payouts import AsyncPayoutsResource
from .async_resources.plan_groups import AsyncPlanGroupsResource
from .async_resources.plans import AsyncPlansResource
from .async_resources.portal import AsyncPortalResource
from .async_resources.promo_codes import AsyncPromoCodesResource
from .async_resources.provisioning import AsyncProvisioningResource
from .async_resources.quota import AsyncQuotaResource
from .async_resources.seats import AsyncSeatsResource
from .async_resources.subscriptions import AsyncSubscriptionsResource
from .async_resources.test_clock import AsyncTestClockResource
from .async_resources.transactions import AsyncTransactionsResource


class GeneratedAsyncResources:
    def _init_resources(self, http: AsyncCommetHTTPClient) -> None:
        self.addons = AsyncAddonsResource(http)
        self.api_keys = AsyncApiKeysResource(http)
        self.credit_packs = AsyncCreditPacksResource(http)
        self.customers = AsyncCustomersResource(http)
        self.feature_access = AsyncFeatureAccessResource(http)
        self.features = AsyncFeaturesResource(http)
        self.invoices = AsyncInvoicesResource(http)
        self.payments = AsyncPaymentsResource(http)
        self.payouts = AsyncPayoutsResource(http)
        self.plan_groups = AsyncPlanGroupsResource(http)
        self.plans = AsyncPlansResource(http)
        self.portal = AsyncPortalResource(http)
        self.promo_codes = AsyncPromoCodesResource(http)
        self.provisioning = AsyncProvisioningResource(http)
        self.quota = AsyncQuotaResource(http)
        self.seats = AsyncSeatsResource(http)
        self.subscriptions = AsyncSubscriptionsResource(http)
        self.test_clock = AsyncTestClockResource(http)
        self.transactions = AsyncTransactionsResource(http)
