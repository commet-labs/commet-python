# ruff: noqa: E501

from __future__ import annotations

from ._http import CommetHTTPClient
from .resources.addons import AddonsResource
from .resources.api_keys import ApiKeysResource
from .resources.credit_packs import CreditPacksResource
from .resources.customers import CustomersResource
from .resources.feature_access import FeatureAccessResource
from .resources.features import FeaturesResource
from .resources.invoices import InvoicesResource
from .resources.markets import MarketsResource
from .resources.offers import OffersResource
from .resources.payments import PaymentsResource
from .resources.payouts import PayoutsResource
from .resources.plan_groups import PlanGroupsResource
from .resources.plans import PlansResource
from .resources.portal import PortalResource
from .resources.promo_codes import PromoCodesResource
from .resources.provisioning import ProvisioningResource
from .resources.quota import QuotaResource
from .resources.seats import SeatsResource
from .resources.subscriptions import SubscriptionsResource
from .resources.test_clock import TestClockResource
from .resources.transactions import TransactionsResource
from .resources.usage import UsageResource


class GeneratedSyncResources:
    def _init_resources(self, http: CommetHTTPClient) -> None:
        self.addons = AddonsResource(http)
        self.api_keys = ApiKeysResource(http)
        self.credit_packs = CreditPacksResource(http)
        self.customers = CustomersResource(http)
        self.feature_access = FeatureAccessResource(http)
        self.features = FeaturesResource(http)
        self.invoices = InvoicesResource(http)
        self.markets = MarketsResource(http)
        self.offers = OffersResource(http)
        self.payments = PaymentsResource(http)
        self.payouts = PayoutsResource(http)
        self.plan_groups = PlanGroupsResource(http)
        self.plans = PlansResource(http)
        self.portal = PortalResource(http)
        self.promo_codes = PromoCodesResource(http)
        self.provisioning = ProvisioningResource(http)
        self.quota = QuotaResource(http)
        self.seats = SeatsResource(http)
        self.subscriptions = SubscriptionsResource(http)
        self.test_clock = TestClockResource(http)
        self.transactions = TransactionsResource(http)
        self.usage = UsageResource(http)
