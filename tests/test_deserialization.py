from __future__ import annotations

from commet.types import (
    BillingInterval,
    ConsumptionModel,
    FeatureType,
    InvoiceType,
    Plan,
    PlanFeaturesItem,
    PlanFeaturesItemOverage,
    PlanFeaturesItemRegionalPricesItem,
    PlanPricesItem,
    PlanPricesItemRegionalPricesItem,
    Transaction,
    TransactionStatus,
    _from_dict,
    _from_list,
)


class TestEnumCoercion:
    def test_wire_string_becomes_enum_member(self) -> None:
        tx = _from_dict(
            Transaction,
            {"id": "txn_1", "status": "succeeded", "gross_amount": 5000, "currency": "usd"},
        )
        assert isinstance(tx.status, TransactionStatus)
        assert tx.status is TransactionStatus.SUCCEEDED
        assert tx.status == "succeeded"

    def test_unknown_enum_value_falls_back_to_raw_string(self) -> None:
        # An enum value the SDK does not know about must NOT crash deserialization;
        # the raw wire string is preserved so forward-compatible servers don't break clients.
        tx = _from_dict(Transaction, {"id": "txn_1", "status": "frozen"})
        assert tx.status == "frozen"
        assert not isinstance(tx.status, TransactionStatus)


class TestNullability:
    def test_wire_null_maps_to_none(self) -> None:
        tx = _from_dict(
            Transaction,
            {"id": "txn_1", "invoice_id": None, "paid_at": None, "status": "pending"},
        )
        assert tx.invoice_id is None
        assert tx.paid_at is None

    def test_omitted_optional_uses_dataclass_default(self) -> None:
        tx = _from_dict(Transaction, {"id": "txn_1"})
        assert tx.invoice_id is None
        assert tx.gross_amount is None
        assert tx.status is None
        assert tx.livemode is False

    def test_unknown_wire_field_is_ignored(self) -> None:
        # Wire fields not present on the dataclass must be dropped, not passed to __init__.
        tx = _from_dict(
            Transaction,
            {"id": "txn_1", "somethingTheServerAddedLater": "boom"},
        )
        assert tx.id == "txn_1"
        assert not hasattr(tx, "something_the_server_added_later")


class TestNestedDataclassCoercion:
    # NOTE: _from_dict runs AFTER the HTTP layer has already converted wire keys to
    # snake_case via convert_keys(to_snake). So the dicts fed here are snake_case,
    # exactly as the deserializer receives them in production.
    def test_nested_object_and_list_of_objects_and_enums(self) -> None:
        already_snaked = {
            "id": "plan_1",
            "code": "pro",
            "name": "Pro",
            "consumption_model": "credits",
            "is_public": True,
            "prices": [
                {
                    "billing_interval": "monthly",
                    "price": 10000,
                    "is_default": True,
                    "trial_days": 14,
                    "id": "price_1",
                    "offer_id": "offer_1",
                    "regional_prices": [
                        {"currency": "brl", "price": 5000, "auto_synced": True},
                    ],
                }
            ],
            "features": [
                {
                    "code": "api_calls",
                    "name": "API Calls",
                    "type": "usage",
                    "enabled": True,
                    "included_amount": 1000,
                    "overage": {"enabled": True, "model": "per_unit", "unit_price": 5},
                    "regional_prices": [
                        {"currency": "eur", "overage_unit_price": 4, "auto_synced": False},
                    ],
                }
            ],
        }

        plan = _from_dict(Plan, already_snaked)

        assert isinstance(plan, Plan)
        assert plan.consumption_model is ConsumptionModel.CREDITS

        assert isinstance(plan.prices, list)
        price = plan.prices[0]
        assert isinstance(price, PlanPricesItem)
        assert price.billing_interval is BillingInterval.MONTHLY
        assert price.price == 10000
        assert price.trial_days == 14

        assert price.offer_id == "offer_1"

        assert isinstance(price.regional_prices[0], PlanPricesItemRegionalPricesItem)
        assert price.regional_prices[0].currency == "brl"
        assert price.regional_prices[0].auto_synced is True

        feature = plan.features[0]
        assert isinstance(feature, PlanFeaturesItem)
        assert feature.type is FeatureType.USAGE
        assert isinstance(feature.overage, PlanFeaturesItemOverage)
        assert feature.overage.unit_price == 5
        assert isinstance(feature.regional_prices[0], PlanFeaturesItemRegionalPricesItem)
        assert feature.regional_prices[0].overage_unit_price == 4
        assert feature.regional_prices[0].auto_synced is False

    def test_nested_optional_object_stays_none_when_absent(self) -> None:
        plan = _from_dict(
            Plan,
            {
                "id": "plan_1",
                "code": "free",
                "name": "Free",
                "prices": [{"billingInterval": "monthly", "price": 0}],
            },
        )
        assert plan.prices[0].offer_id is None
        assert plan.prices[0].regional_prices == []
        assert plan.features == []


class TestFromList:
    def test_from_list_coerces_each_item_and_its_enums(self) -> None:
        rows = _from_list(
            Transaction,
            [
                {"id": "txn_1", "status": "succeeded", "invoice_id": "inv_1"},
                {"id": "txn_2", "status": "refunded"},
            ],
        )
        assert len(rows) == 2
        assert all(isinstance(r, Transaction) for r in rows)
        assert rows[0].status is TransactionStatus.SUCCEEDED
        assert rows[1].status is TransactionStatus.REFUNDED


class TestPreservedTypeRegistration:
    def test_invoice_type_enum_resolves_through_registry(self) -> None:
        # InvoiceType is referenced by name from generated annotations; the registry
        # must resolve it so the member (not a raw string) is produced.
        assert InvoiceType("balance_topup") is InvoiceType.BALANCE_TOPUP
