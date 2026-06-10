from __future__ import annotations

import json

import pytest
import respx
from httpx import Response

from commet import Commet
from commet.async_client import AsyncCommet
from commet.types import (
    ActiveAddon,
    Addon,
    BulkSeatUpdate,
    CreditPack,
    FeatureType,
    SeatBalance,
    SeatEvent,
)


@pytest.fixture
def mock_api() -> respx.MockRouter:
    with respx.mock(base_url="https://commet.co/api/v1") as mock:
        yield mock


class TestSeats:
    def test_add_sends_body_and_parses_event(self, mock_api: respx.MockRouter) -> None:
        route = mock_api.post("/seats").mock(
            return_value=Response(
                200,
                json={
                    "success": True,
                    "data": {
                        "id": "se_1",
                        "customerId": "cus_1",
                        "featureCode": "seats",
                        "previousBalance": 2,
                        "newBalance": 5,
                        "ts": "2026-06-01T00:00:00Z",
                        "createdAt": "2026-06-01T00:00:00Z",
                        "object": "seat",
                    },
                },
            )
        )
        with Commet(api_key="ck_test_123") as client:
            result = client.seats.add(customer_id="cus_1", feature_code="seats", count=3)

        assert isinstance(result.data, SeatEvent)
        assert result.data.previous_balance == 2
        assert result.data.new_balance == 5

        sent = json.loads(route.calls.last.request.content)
        assert sent == {"customerId": "cus_1", "featureCode": "seats", "count": 3}

    def test_remove_uses_delete_with_body(self, mock_api: respx.MockRouter) -> None:
        route = mock_api.delete("/seats").mock(
            return_value=Response(
                200,
                json={
                    "success": True,
                    "data": {
                        "id": "se_2",
                        "customerId": "cus_1",
                        "featureCode": "seats",
                        "previousBalance": 5,
                        "newBalance": 4,
                        "ts": "2026-06-01T00:00:00Z",
                        "createdAt": "2026-06-01T00:00:00Z",
                    },
                },
            )
        )
        with Commet(api_key="ck_test_123") as client:
            result = client.seats.remove(customer_id="cus_1", feature_code="seats", count=1)

        assert isinstance(result.data, SeatEvent)
        assert result.data.new_balance == 4
        sent = json.loads(route.calls.last.request.content)
        assert sent == {"customerId": "cus_1", "featureCode": "seats", "count": 1}

    def test_set_all_sends_map_and_parses_list(self, mock_api: respx.MockRouter) -> None:
        route = mock_api.put("/seats/bulk").mock(
            return_value=Response(
                200,
                json={
                    "success": True,
                    "data": [
                        {
                            "id": "se_a",
                            "featureCode": "editor",
                            "previousBalance": 0,
                            "newBalance": 3,
                            "ts": "2026-06-01T00:00:00Z",
                            "createdAt": "2026-06-01T00:00:00Z",
                        },
                        {
                            "id": "se_b",
                            "featureCode": "viewer",
                            "previousBalance": 1,
                            "newBalance": 10,
                            "ts": "2026-06-01T00:00:00Z",
                            "createdAt": "2026-06-01T00:00:00Z",
                        },
                    ],
                },
            )
        )
        with Commet(api_key="ck_test_123") as client:
            result = client.seats.set_all(customer_id="cus_1", seats={"editor": 3, "viewer": 10})

        assert isinstance(result.data, list)
        assert all(isinstance(item, BulkSeatUpdate) for item in result.data)
        assert result.data[0].feature_code == "editor"
        assert result.data[1].new_balance == 10

        sent = json.loads(route.calls.last.request.content)
        # The seats map values are ints keyed by feature code; keys are not camelCased
        # arbitrarily-meaningful values, but the convert pass still runs over them.
        assert sent["customerId"] == "cus_1"
        assert sent["seats"] == {"editor": 3, "viewer": 10}

    def test_get_balance_query_and_parse(self, mock_api: respx.MockRouter) -> None:
        route = mock_api.get("/seats/balance").mock(
            return_value=Response(
                200,
                json={
                    "success": True,
                    "data": {"current": 7, "asOf": "2026-06-01T00:00:00Z", "object": "seat"},
                },
            )
        )
        with Commet(api_key="ck_test_123") as client:
            result = client.seats.get_balance(customer_id="cus_1", feature_code="editor")

        assert isinstance(result.data, SeatBalance)
        assert result.data.current == 7
        assert result.data.as_of == "2026-06-01T00:00:00Z"
        params = route.calls.last.request.url.params
        assert params["customerId"] == "cus_1"
        assert params["featureCode"] == "editor"


class TestAddons:
    def test_create_sends_camel_case_consumption_model_literal(
        self, mock_api: respx.MockRouter
    ) -> None:
        route = mock_api.post("/addons").mock(
            return_value=Response(
                200,
                json={
                    "success": True,
                    "data": {
                        "id": "addon_1",
                        "name": "Extra Storage",
                        "slug": "extra-storage",
                        "basePrice": 2000,
                        "consumptionModel": "metered",
                        "featureCode": "storage",
                        "featureName": "Storage",
                        "includedUnits": 100,
                        "overageRate": 5,
                        "createdAt": "2026-06-01T00:00:00Z",
                        "updatedAt": "2026-06-01T00:00:00Z",
                        "object": "addon",
                    },
                },
            )
        )
        with Commet(api_key="ck_test_123") as client:
            result = client.addons.create(
                name="Extra Storage",
                base_price=2000,
                feature_id="feat_1",
                consumption_model="metered",
                included_units=100,
                overage_rate=5,
            )

        assert isinstance(result.data, Addon)
        assert result.data.consumption_model == "metered"
        assert result.data.included_units == 100

        sent = json.loads(route.calls.last.request.content)
        assert sent == {
            "name": "Extra Storage",
            "basePrice": 2000,
            "featureId": "feat_1",
            "consumptionModel": "metered",
            "includedUnits": 100,
            "overageRate": 5,
        }

    def test_list_active_parses_feature_type_enum(self, mock_api: respx.MockRouter) -> None:
        mock_api.get("/active-addons").mock(
            return_value=Response(
                200,
                json={
                    "success": True,
                    "data": [
                        {
                            "slug": "extra-storage",
                            "name": "Extra Storage",
                            "basePrice": 2000,
                            "featureCode": "storage",
                            "featureName": "Storage",
                            "featureType": "usage",
                            "consumptionModel": "metered",
                            "activatedAt": "2026-06-01T00:00:00Z",
                            "object": "addon",
                        }
                    ],
                },
            )
        )
        with Commet(api_key="ck_test_123") as client:
            result = client.addons.list_active(customer_id="cus_1")

        assert isinstance(result.data[0], ActiveAddon)
        assert result.data[0].feature_type is FeatureType.USAGE
        assert result.data[0].consumption_model == "metered"


class TestCreditPacks:
    def test_create_sends_body_and_parses(self, mock_api: respx.MockRouter) -> None:
        route = mock_api.post("/credit-packs/manage").mock(
            return_value=Response(
                200,
                json={
                    "success": True,
                    "data": {
                        "id": "cp_1",
                        "name": "1000 Credits",
                        "credits": 1000,
                        "price": 5000,
                        "currency": "usd",
                        "isActive": True,
                        "object": "credit_pack",
                    },
                },
            )
        )
        with Commet(api_key="ck_test_123") as client:
            result = client.credit_packs.create(name="1000 Credits", credits=1000, price=5000)

        assert isinstance(result.data, CreditPack)
        assert result.data.credits == 1000
        assert result.data.is_active is True

        sent = json.loads(route.calls.last.request.content)
        assert sent == {"name": "1000 Credits", "credits": 1000, "price": 5000}

    def test_list_parses_each_pack(self, mock_api: respx.MockRouter) -> None:
        mock_api.get("/credit-packs").mock(
            return_value=Response(
                200,
                json={
                    "success": True,
                    "data": [
                        {"id": "cp_1", "name": "Small", "credits": 100, "price": 500},
                        {"id": "cp_2", "name": "Large", "credits": 1000, "price": 4500},
                    ],
                },
            )
        )
        with Commet(api_key="ck_test_123") as client:
            result = client.credit_packs.list()

        assert all(isinstance(p, CreditPack) for p in result.data)
        assert result.data[1].credits == 1000


@pytest.mark.asyncio
class TestAsyncSeatsAndAddons:
    async def test_async_seat_add(self, mock_api: respx.MockRouter) -> None:
        mock_api.post("/seats").mock(
            return_value=Response(
                200,
                json={
                    "success": True,
                    "data": {
                        "id": "se_async",
                        "customerId": "cus_1",
                        "featureCode": "seats",
                        "previousBalance": 0,
                        "newBalance": 2,
                        "ts": "2026-06-01T00:00:00Z",
                        "createdAt": "2026-06-01T00:00:00Z",
                    },
                },
            )
        )
        async with AsyncCommet(api_key="ck_test_123") as client:
            result = await client.seats.add(customer_id="cus_1", feature_code="seats", count=2)

        assert isinstance(result.data, SeatEvent)
        assert result.data.new_balance == 2

    async def test_async_addon_create_camel_case(self, mock_api: respx.MockRouter) -> None:
        route = mock_api.post("/addons").mock(
            return_value=Response(
                200,
                json={
                    "success": True,
                    "data": {
                        "id": "addon_async",
                        "name": "Async Addon",
                        "slug": "async-addon",
                        "basePrice": 100,
                        "consumptionModel": "boolean",
                        "featureCode": "flag",
                        "featureName": "Flag",
                    },
                },
            )
        )
        async with AsyncCommet(api_key="ck_test_123") as client:
            result = await client.addons.create(
                name="Async Addon",
                base_price=100,
                feature_id="feat_x",
                consumption_model="boolean",
            )

        assert isinstance(result.data, Addon)
        sent = json.loads(route.calls.last.request.content)
        assert sent == {
            "name": "Async Addon",
            "basePrice": 100,
            "featureId": "feat_x",
            "consumptionModel": "boolean",
        }
