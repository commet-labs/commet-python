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


def plan_payload() -> dict[str, object]:
    return {
        "id": "plan_1",
        "name": "Pro",
        "code": "pro",
        "consumptionModel": "metered",
        "isPublic": True,
        "prices": [
            {
                "id": "price_1",
                "billingInterval": "yearly",
                "price": 120000,
                "isDefault": True,
                "trialDays": 30,
                "offerId": "offer_1",
                "regionalPrices": [{"currency": "brl", "price": 60000, "autoSynced": True}],
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
    }


def test_get_parses_direct_plan(mock_api: respx.MockRouter) -> None:
    mock_api.get("/plans/pro").mock(return_value=Response(200, json=plan_payload()))
    with Commet(api_key="ck_test_123") as client:
        plan = client.plans.get("pro")

    assert isinstance(plan, Plan)
    assert plan.consumption_model is ConsumptionModel.METERED
    assert plan.prices[0].billing_interval is BillingInterval.YEARLY
    assert plan.prices[0].offer_id == "offer_1"
    assert plan.features[0].type is FeatureType.SEATS


def test_list_passes_boolean_include_private(mock_api: respx.MockRouter) -> None:
    route = mock_api.get("/plans").mock(
        return_value=Response(
            200,
            json={"object": "list", "data": [], "hasMore": False},
        )
    )
    with Commet(api_key="ck_test_123") as client:
        client.plans.list(include_private=True)

    assert route.calls.last.request.url.params["includePrivate"] == "true"


def test_add_price_has_no_manual_offer_shape(mock_api: respx.MockRouter) -> None:
    route = mock_api.post("/plans/plan_1/prices").mock(
        return_value=Response(
            200,
            json={
                "id": "price_1",
                "planId": "plan_1",
                "billingInterval": "monthly",
                "price": 10000,
                "isDefault": False,
                "trialDays": 7,
                "offerId": "offer_1",
            },
        )
    )
    with Commet(api_key="ck_test_123") as client:
        price = client.plans.add_price(
            "plan_1",
            billing_interval="monthly",
            price=10000,
            trial_days=7,
        )

    assert isinstance(price, PlanPrice)
    assert price.billing_interval is BillingInterval.MONTHLY
    assert price.offer_id == "offer_1"
    assert json.loads(route.calls.last.request.content) == {
        "billingInterval": "monthly",
        "price": 10000,
        "trialDays": 7,
    }


def test_set_regional_prices_returns_direct_resource(
    mock_api: respx.MockRouter,
) -> None:
    route = mock_api.put("/plans/plan_1/prices/price_1/regional").mock(
        return_value=Response(
            200,
            json={
                "priceId": "price_1",
                "overrides": [{"currency": "brl", "price": 50000, "includedBalance": 100}],
            },
        )
    )
    with Commet(api_key="ck_test_123") as client:
        result = client.plans.set_regional_prices(
            "plan_1",
            "price_1",
            overrides=[{"currency": "brl", "price": 50000, "included_balance": 100}],
        )

    assert isinstance(result, PlanRegionalPricing)
    assert result.overrides[0].included_balance == 100
    assert json.loads(route.calls.last.request.content)["overrides"][0]["includedBalance"] == 100


def test_set_regional_pricing_returns_direct_resource(
    mock_api: respx.MockRouter,
) -> None:
    mock_api.put("/plans/plan_1/regional").mock(
        return_value=Response(
            200,
            json={
                "planId": "plan_1",
                "currency": "brl",
                "exchangeRate": 5.12,
                "pricesConfigured": 2,
                "featuresConfigured": 3,
            },
        )
    )
    with Commet(api_key="ck_test_123") as client:
        result = client.plans.set_regional_pricing("plan_1", currency="brl", exchange_rate=5.12)

    assert isinstance(result, PlanRegionalPricingResult)
    assert result.exchange_rate == 5.12


@pytest.mark.asyncio
async def test_async_get_returns_direct_plan(mock_api: respx.MockRouter) -> None:
    mock_api.get("/plans/plan_1").mock(return_value=Response(200, json=plan_payload()))
    async with AsyncCommet(api_key="ck_test_123") as client:
        plan = await client.plans.get("plan_1")

    assert plan.prices[0].offer_id == "offer_1"
