from __future__ import annotations

import json

import pytest
import respx
from httpx import Response

from commet import Commet
from commet.async_client import AsyncCommet
from commet.types import (
    BillingInterval,
    ConsumptionModel,
    DiscountType,
    FeatureType,
    Plan,
    PlanPrice,
    PlanRegionalPricing,
    PlanRegionalPricingResult,
)


@pytest.fixture
def mock_api() -> respx.MockRouter:
    with respx.mock(base_url="https://commet.co/api/v1") as mock:
        yield mock


class TestGet:
    def test_get_parses_nested_prices_features_and_enums(
        self, mock_api: respx.MockRouter
    ) -> None:
        mock_api.get("/plans/pro").mock(
            return_value=Response(
                200,
                json={
                    "success": True,
                    "data": {
                        "id": "plan_1",
                        "name": "Pro",
                        "code": "pro",
                        "consumptionModel": "metered",
                        "isPublic": True,
                        "prices": [
                            {
                                "billingInterval": "yearly",
                                "price": 120000,
                                "isDefault": True,
                                "trialDays": 30,
                                "includedCredits": 1000,
                                "introOffer": {
                                    "enabled": True,
                                    "discountType": "amount",
                                    "discountValue": 5000,
                                    "durationCycles": 2,
                                },
                                "regionalPrices": [
                                    {"currency": "brl", "price": 60000, "autoSynced": True},
                                ],
                            }
                        ],
                        "features": [
                            {
                                "code": "seats",
                                "name": "Seats",
                                "type": "seats",
                                "enabled": True,
                                "includedAmount": 5,
                                "overage": {
                                    "enabled": True,
                                    "model": "per_unit",
                                    "unitPrice": 1000,
                                },
                            }
                        ],
                        "object": "plan",
                    },
                },
            )
        )
        with Commet(api_key="ck_test_123") as client:
            result = client.plans.get("pro")

        plan = result.data
        assert isinstance(plan, Plan)
        assert plan.consumption_model is ConsumptionModel.METERED

        price = plan.prices[0]
        assert price.billing_interval is BillingInterval.YEARLY
        assert price.intro_offer.discount_type is DiscountType.AMOUNT
        assert price.intro_offer.discount_value == 5000
        assert price.regional_prices[0].currency == "brl"
        assert price.regional_prices[0].auto_synced is True

        feature = plan.features[0]
        assert feature.type is FeatureType.SEATS
        assert feature.overage.unit_price == 1000


class TestListIncludePrivate:
    def test_list_passes_include_private_query(self, mock_api: respx.MockRouter) -> None:
        route = mock_api.get("/plans").mock(
            return_value=Response(200, json={"success": True, "data": []})
        )
        with Commet(api_key="ck_test_123") as client:
            client.plans.list(include_private="true")

        assert route.calls.last.request.url.params["includePrivate"] == "true"


class TestAddPrice:
    def test_add_price_sends_enum_and_nested_intro_offer(
        self, mock_api: respx.MockRouter
    ) -> None:
        route = mock_api.post("/plans/plan_1/prices").mock(
            return_value=Response(
                200,
                json={
                    "success": True,
                    "data": {
                        "id": "price_1",
                        "planId": "plan_1",
                        "billingInterval": "monthly",
                        "price": 10000,
                        "isDefault": False,
                        "trialDays": 7,
                        "introOffer": {
                            "enabled": True,
                            "discountType": "percentage",
                            "discountValue": 1500,
                            "durationCycles": 3,
                        },
                    },
                },
            )
        )
        with Commet(api_key="ck_test_123") as client:
            result = client.plans.add_price(
                "plan_1",
                billing_interval=BillingInterval.MONTHLY,
                price=10000,
                trial_days=7,
                intro_offer={
                    "enabled": True,
                    "discount_type": "percentage",
                    "discount_value": 1500,
                    "duration_cycles": 3,
                },
            )

        assert isinstance(result.data, PlanPrice)
        assert result.data.billing_interval is BillingInterval.MONTHLY
        assert result.data.intro_offer.discount_type is DiscountType.PERCENTAGE

        sent = json.loads(route.calls.last.request.content)
        # Enum value serializes to its wire string, never the member repr.
        assert sent["billingInterval"] == "monthly"
        assert sent["price"] == 10000
        assert sent["trialDays"] == 7
        assert sent["introOffer"] == {
            "enabled": True,
            "discountType": "percentage",
            "discountValue": 1500,
            "durationCycles": 3,
        }


class TestSetRegionalPrices:
    def test_sends_list_of_overrides_camel_cased(self, mock_api: respx.MockRouter) -> None:
        route = mock_api.put("/plans/plan_1/prices/price_1/regional").mock(
            return_value=Response(
                200,
                json={
                    "success": True,
                    "data": {
                        "priceId": "price_1",
                        "overrides": [
                            {"currency": "brl", "price": 50000, "includedBalance": 100},
                            {"currency": "eur", "price": 9000},
                        ],
                        "object": "plan",
                    },
                },
            )
        )
        with Commet(api_key="ck_test_123") as client:
            result = client.plans.set_regional_prices(
                "plan_1",
                "price_1",
                overrides=[
                    {"currency": "brl", "price": 50000, "included_balance": 100},
                    {"currency": "eur", "price": 9000},
                ],
            )

        assert isinstance(result.data, PlanRegionalPricing)
        assert result.data.overrides[0].currency == "brl"
        assert result.data.overrides[0].included_balance == 100

        sent = json.loads(route.calls.last.request.content)
        # Each item in the list body must be recursively key-converted.
        assert sent["overrides"] == [
            {"currency": "brl", "price": 50000, "includedBalance": 100},
            {"currency": "eur", "price": 9000},
        ]


class TestSetRegionalPricing:
    def test_derives_all_values_from_currency_and_rate(self, mock_api: respx.MockRouter) -> None:
        route = mock_api.put("/plans/plan_1/regional").mock(
            return_value=Response(
                200,
                json={
                    "success": True,
                    "data": {
                        "planId": "plan_1",
                        "currency": "brl",
                        "exchangeRate": 5.12,
                        "pricesConfigured": 2,
                        "featuresConfigured": 3,
                        "object": "plan",
                    },
                },
            )
        )
        with Commet(api_key="ck_test_123") as client:
            result = client.plans.set_regional_pricing(
                "plan_1", currency="brl", exchange_rate=5.12
            )

        assert isinstance(result.data, PlanRegionalPricingResult)
        assert result.data.currency == "brl"
        assert result.data.exchange_rate == 5.12
        assert result.data.prices_configured == 2
        assert result.data.features_configured == 3

        sent = json.loads(route.calls.last.request.content)
        assert sent == {"currency": "brl", "exchangeRate": 5.12}


@pytest.mark.asyncio
class TestAsyncPlans:
    async def test_get_parses_nested_intro_offer(self, mock_api: respx.MockRouter) -> None:
        mock_api.get("/plans/plan_1").mock(
            return_value=Response(
                200,
                json={
                    "success": True,
                    "data": {
                        "id": "plan_1",
                        "name": "Pro",
                        "code": "pro",
                        "consumptionModel": "credits",
                        "prices": [
                            {
                                "billingInterval": "monthly",
                                "price": 10000,
                                "introOffer": {
                                    "enabled": True,
                                    "discountType": "percentage",
                                    "discountValue": 1000,
                                },
                            }
                        ],
                    },
                },
            )
        )
        async with AsyncCommet(api_key="ck_test_123") as client:
            result = await client.plans.get("plan_1")

        assert result.data.consumption_model is ConsumptionModel.CREDITS
        assert result.data.prices[0].intro_offer.discount_type is DiscountType.PERCENTAGE
