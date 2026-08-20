# ruff: noqa: E501


from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Literal, TypeVar, Union, cast

from ._http import ApiResponse

T = TypeVar("T")

_ENUM_TYPES: dict[str, type[Enum]] = {}
_DATACLASS_TYPES: dict[str, type[Any]] = {}
_UNION_TYPES: dict[str, tuple[str | None, dict[Any, type[Any]], list[type[Any]]]] = {}


def _from_union(name: str, data: Any) -> Any:
    if not isinstance(data, dict):
        return data
    field, variants, fallbacks = _UNION_TYPES[name]
    if field is not None:
        selected = variants.get(data.get(field))
        if selected is not None:
            return _from_dict(selected, data)
    if fallbacks:
        selected = max(
            fallbacks,
            key=lambda candidate: len(set(candidate.__dataclass_fields__) & set(data)),
        )
        return _from_dict(selected, data)
    return data


def _coerce_field(annotation: str, value: Any) -> Any:
    base = annotation.split(" | ")[0].strip()

    if base in _UNION_TYPES:
        return _from_union(base, value)

    enum_cls = _ENUM_TYPES.get(base)
    if enum_cls is not None:
        try:
            return enum_cls(value)
        except ValueError:
            return value

    if base.startswith("list[") and base.endswith("]"):
        inner = base[len("list[") : -1].strip()
        nested = _DATACLASS_TYPES.get(inner)
        enum_inner = _ENUM_TYPES.get(inner)
        if inner in _UNION_TYPES and isinstance(value, list):
            return [_from_union(inner, item) for item in value]
        if nested is not None and isinstance(value, list):
            return [_from_dict(nested, item) for item in value]
        if enum_inner is not None and isinstance(value, list):
            return [_coerce_field(inner, item) for item in value]
        return value

    if base.startswith("dict[") and base.endswith("]"):
        inner = base[len("dict[") : -1].split(",")[-1].strip()
        nested = _DATACLASS_TYPES.get(inner)
        if nested is not None and isinstance(value, dict):
            return {k: _from_dict(nested, v) for k, v in value.items()}
        return value

    nested = _DATACLASS_TYPES.get(base)
    if nested is not None and isinstance(value, dict):
        return _from_dict(nested, value)

    return value


def _from_dict(cls: type[T], data: Any) -> T:
    if not isinstance(data, dict):
        return cast("T", data)
    fields_map = cls.__dataclass_fields__  # type: ignore[attr-defined]
    result: dict[str, Any] = {}
    for key, value in data.items():
        if key not in fields_map:
            continue
        annotation = fields_map[key].type
        result[key] = (
            _coerce_field(annotation, value)
            if isinstance(annotation, str) and value is not None
            else value
        )
    return cls(**result)


def _from_list(cls: type[T], data: list[Any]) -> list[T]:
    return [_from_dict(cls, item) for item in data]


def _parse(response: ApiResponse[Any], cls: type[T]) -> ApiResponse[T]:
    if isinstance(response.data, dict):
        response.data = _from_dict(cls, response.data)
    return response


def _parse_union(response: ApiResponse[Any], name: str) -> ApiResponse[Any]:
    response.data = _from_union(name, response.data)
    return response


def _parse_list(response: ApiResponse[Any], cls: type[T]) -> ApiResponse[list[T]]:
    if isinstance(response.data, list):
        response.data = _from_list(cls, response.data)
    return response


def _parse_union_list(response: ApiResponse[Any], name: str) -> ApiResponse[list[Any]]:
    if isinstance(response.data, list):
        response.data = [_from_union(name, item) for item in response.data]
    return response


def _parse_map(response: ApiResponse[Any], cls: type[T]) -> ApiResponse[dict[str, T]]:
    if isinstance(response.data, dict):
        response.data = {
            key: _from_dict(cls, value) if isinstance(value, dict) else value
            for key, value in response.data.items()
        }
    return response


def _data(response: ApiResponse[T]) -> T:
    return cast("T", response.data)


def _parse_data(response: ApiResponse[Any], cls: type[T]) -> T:
    return cast("T", _parse(response, cls).data)


def _parse_union_data(response: ApiResponse[Any], name: str) -> Any:
    return _parse_union(response, name).data


def _parse_list_data(response: ApiResponse[Any], cls: type[T]) -> list[T]:
    return cast("list[T]", _parse_list(response, cls).data)


def _parse_union_list_data(response: ApiResponse[Any], name: str) -> list[Any]:
    return cast("list[Any]", _parse_union_list(response, name).data)


def _parse_map_data(response: ApiResponse[Any], cls: type[T]) -> dict[str, T]:
    return cast("dict[str, T]", _parse_map(response, cls).data)


class BillingInterval(str, Enum):
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    YEARLY = "yearly"
    ONE_TIME = "one_time"


class ConsumptionModel(str, Enum):
    METERED = "metered"
    CREDITS = "credits"
    BALANCE = "balance"


class FeatureType(str, Enum):
    BOOLEAN = "boolean"
    USAGE = "usage"
    SEATS = "seats"
    QUOTA = "quota"


class InvoiceType(str, Enum):
    RECURRING = "recurring"
    OVERAGE = "overage"
    PLAN_CHANGE = "plan_change"
    ADJUSTMENT = "adjustment"
    CREDIT_PURCHASE = "credit_purchase"
    BALANCE_TOPUP = "balance_topup"
    ADDON_ACTIVATION = "addon_activation"
    ONE_TIME_PAYMENT = "one_time_payment"
    REACTIVATION = "reactivation"


class PaymentProvider(str, Enum):
    STRIPE = "stripe"
    COMMET = "commet"
    DLOCAL = "dlocal"


class SubscriptionStatus(str, Enum):
    DRAFT = "draft"
    PENDING_PAYMENT = "pending_payment"
    TRIALING = "trialing"
    ACTIVE = "active"
    PAST_DUE = "past_due"
    CANCELED = "canceled"


class Timezone(str, Enum):
    UTC = "UTC"
    AMERICA_NEW_YORK = "America/New_York"
    AMERICA_CHICAGO = "America/Chicago"
    AMERICA_DENVER = "America/Denver"
    AMERICA_LOS_ANGELES = "America/Los_Angeles"
    AMERICA_SAO_PAULO = "America/Sao_Paulo"
    AMERICA_MEXICO_CITY = "America/Mexico_City"
    AMERICA_BUENOS_AIRES = "America/Buenos_Aires"
    AMERICA_SANTIAGO = "America/Santiago"
    AMERICA_BOGOTA = "America/Bogota"
    AMERICA_LIMA = "America/Lima"
    AMERICA_ASUNCION = "America/Asuncion"
    EUROPE_LONDON = "Europe/London"
    EUROPE_PARIS = "Europe/Paris"
    EUROPE_BERLIN = "Europe/Berlin"
    EUROPE_MADRID = "Europe/Madrid"
    ASIA_TOKYO = "Asia/Tokyo"
    ASIA_SHANGHAI = "Asia/Shanghai"
    ASIA_SINGAPORE = "Asia/Singapore"
    ASIA_DUBAI = "Asia/Dubai"
    AUSTRALIA_SYDNEY = "Australia/Sydney"


class TransactionStatus(str, Enum):
    PENDING = "pending"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    REFUNDED = "refunded"
    DISPUTED = "disputed"


@dataclass
class ActiveAddon:
    slug: str = ""
    name: str = ""
    base_price: int = 0
    feature_code: str = ""
    feature_name: str = ""
    feature_type: FeatureType | None = None
    consumption_model: Literal["boolean", "metered", "credits", "balance"] | None = None
    activated_at: str = ""
    object: Literal["subscription_addon"] | None = None
    livemode: bool = False


@dataclass
class AddedPlanToGroup:
    success: bool = False
    object: Literal["plan_group_membership"] | None = None
    livemode: bool = False


@dataclass
class Addon:
    id: str = ""
    name: str = ""
    slug: str = ""
    description: str | None = None
    base_price: int = 0
    feature_code: str = ""
    feature_name: str = ""
    created_at: str = ""
    updated_at: str = ""
    consumption_model: Literal["boolean", "metered", "credits", "balance"] | None = None
    included_units: int | None = None
    overage_rate: int | None = None
    credit_cost: int | None = None
    object: Literal["addon"] | None = None
    livemode: bool = False


@dataclass
class AddonsListActiveResult:
    object: Literal["list"] | None = None
    data: list[ActiveAddon] = field(default_factory=list)
    has_more: bool = False
    next_cursor: str | None = None


@dataclass
class AddonsListResult:
    object: Literal["list"] | None = None
    data: list[Addon] = field(default_factory=list)
    has_more: bool = False
    next_cursor: str | None = None


@dataclass
class AddPlanFeatureParamsOverage:
    enabled: bool | None = None
    unit_price: int | None = None


@dataclass
class AddPlanPriceParamsMarketPricesItem:
    market_group_id: str = ""
    currency: (
        Literal[
            "usd",
            "ars",
            "brl",
            "clp",
            "cop",
            "pen",
            "uyu",
            "pyg",
            "bob",
            "mxn",
            "cad",
            "eur",
            "jpy",
            "cny",
            "krw",
            "hkd",
            "sgd",
            "twd",
            "inr",
            "thb",
        ]
        | None
    ) = None
    price: int = 0


@dataclass
class ApiKey:
    id: str = ""
    name: str = ""
    prefix: str = ""
    expires_at: str | None = None
    last_used_at: str | None = None
    created_at: str = ""
    object: Literal["api_key"] | None = None
    livemode: bool = False


@dataclass
class ApiKeysListResult:
    object: Literal["list"] | None = None
    data: list[ApiKey] = field(default_factory=list)
    has_more: bool = False
    next_cursor: str | None = None


@dataclass
class BalanceAdjustment:
    amount: int = 0
    new_balance: int = 0
    reason: str | None = None
    object: Literal["balance_transaction"] | None = None
    livemode: bool = False


@dataclass
class BalanceTopup:
    amount: int = 0
    object: Literal["balance_topup"] | None = None
    livemode: bool = False


@dataclass
class BatchCreateCustomersParamsCustomersItem:
    email: str = ""
    id: str | None = None
    external_id: str | None = None
    full_name: str | None = None
    tax_document: str | None = None
    timezone: Timezone | None = None
    metadata: dict[str, Any] | None = None
    address: BatchCreateCustomersParamsCustomersItemAddress | None = None


@dataclass
class BatchCreateCustomersParamsCustomersItemAddress:
    line1: str = ""
    line2: str | None = None
    city: str = ""
    state: str | None = None
    postal_code: str = ""
    country: str = ""
    region: str | None = None


@dataclass
class ClaimLink:
    url: str = ""
    expires_at: str = ""
    object: Literal["claim_link"] | None = None
    livemode: bool = False


@dataclass
class CreateCustomerParamsAddress:
    line1: str = ""
    line2: str | None = None
    city: str = ""
    state: str | None = None
    postal_code: str = ""
    country: str = ""
    region: str | None = None


@dataclass
class CreatedApiKey:
    id: str = ""
    name: str = ""
    api_key: str = ""
    prefix: str = ""
    expires_at: str = ""
    created_at: str = ""
    object: Literal["api_key"] | None = None
    livemode: bool = False


@dataclass
class CreatedSubscription:
    id: str = ""
    customer_id: str = ""
    plan: CreatedSubscriptionPlan | None = None
    name: str = ""
    description: str | None = None
    status: SubscriptionStatus | None = None
    billing_interval: BillingInterval | None = None
    trial_ends_at: str | None = None
    current_period: CreatedSubscriptionCurrentPeriod | None = None
    cancellation: CreatedSubscriptionCancellation | None = None
    cancel_at_period_end: bool = False
    scheduled_plan_change: CreatedSubscriptionScheduledPlanChange | None = None
    start_date: str = ""
    end_date: str | None = None
    billing_day_of_month: int | None = None
    next_billing_date: str | None = None
    checkout_url: str | None = None
    created_at: str = ""
    updated_at: str = ""
    offer_applications: list[SubscriptionOfferApplication] = field(default_factory=list)
    checkout_provider: PaymentProvider | None = None
    price_id: str | None = None
    object: Literal["subscription"] | None = None
    livemode: bool = False


@dataclass
class CreatedSubscriptionCancellation:
    scheduled_at: str = ""
    reason: str | None = None
    effective_at: str = ""


@dataclass
class CreatedSubscriptionCurrentPeriod:
    start: str = ""
    end: str = ""
    days_remaining: float = 0.0


@dataclass
class CreatedSubscriptionPlan:
    id: str = ""
    name: str = ""


@dataclass
class CreatedSubscriptionScheduledPlanChange:
    change_type: Literal["plan_downgrade", "interval_change"] | None = None
    new_plan_id: str | None = None
    new_plan_name: str | None = None
    new_billing_interval: str | None = None
    scheduled_for: str = ""


@dataclass
class CreatedWebhook:
    id: str = ""
    url: str = ""
    events: list[str] = field(default_factory=list)
    description: str | None = None
    is_active: bool = False
    api_version: str | None = None
    created_at: str = ""
    secret_key: str = ""
    object: Literal["webhook"] | None = None
    livemode: bool = False


@dataclass
class CreateOfferParamsPhasesItemVariant1:
    type: Literal["free_trial"] | None = None
    duration_days: int = 0


@dataclass
class CreateOfferParamsPhasesItemVariant2:
    type: Literal["percentage"] | None = None
    duration_cycles: int | None = None
    duration_interval: Literal["weekly", "monthly", "quarterly", "yearly"] | None = None
    percentage: int = 0


@dataclass
class CreateOfferParamsPhasesItemVariant3:
    type: Literal["amount_off"] | None = None
    duration_cycles: int | None = None
    duration_interval: Literal["weekly", "monthly", "quarterly", "yearly"] | None = None
    amounts: list[CreateOfferParamsPhasesItemVariant3AmountsItem] = field(default_factory=list)


@dataclass
class CreateOfferParamsPhasesItemVariant3AmountsItem:
    currency: str = ""
    amount: int = 0


@dataclass
class CreateOfferParamsPhasesItemVariant4:
    type: Literal["fixed_price"] | None = None
    duration_cycles: int | None = None
    duration_interval: Literal["weekly", "monthly", "quarterly", "yearly"] | None = None
    prices: list[CreateOfferParamsPhasesItemVariant4PricesItem] = field(default_factory=list)


@dataclass
class CreateOfferParamsPhasesItemVariant4PricesItem:
    currency: str = ""
    amount: int = 0


@dataclass
class CreditGrant:
    credits: int = 0
    object: Literal["credit_grant"] | None = None
    livemode: bool = False


@dataclass
class CreditPack:
    id: str = ""
    name: str = ""
    description: str | None = None
    credits: int = 0
    price: int = 0
    is_active: bool = False
    created_at: str = ""
    updated_at: str = ""
    object: Literal["credit_pack"] | None = None
    livemode: bool = False


@dataclass
class CreditPackListItem:
    id: str = ""
    name: str = ""
    description: str | None = None
    credits: int = 0
    price: int = 0
    currency: str = ""
    object: Literal["credit_pack"] | None = None
    livemode: bool = False


@dataclass
class CreditPacksListResult:
    object: Literal["list"] | None = None
    data: list[CreditPackListItem] = field(default_factory=list)
    has_more: bool = False
    next_cursor: str | None = None


@dataclass
class Customer:
    id: str = ""
    external_id: str | None = None
    full_name: str | None = None
    email: str = ""
    tax_document: str | None = None
    document_type: str | None = None
    timezone: str | None = None
    metadata: dict[str, Any] | None = None
    created_at: str = ""
    updated_at: str = ""
    object: Literal["customer"] | None = None
    livemode: bool = False


@dataclass
class CustomerBatch:
    successful: list[CustomerBatchSuccessfulItem] = field(default_factory=list)
    failed: list[CustomerBatchFailedItem] = field(default_factory=list)
    object: Literal["customer_batch"] | None = None
    livemode: bool = False


@dataclass
class CustomerBatchFailedItem:
    index: int = 0
    error: str = ""
    data: CustomerBatchFailedItemData | None = None


@dataclass
class CustomerBatchFailedItemData:
    id: str | None = None
    external_id: str | None = None
    email: str = ""
    full_name: str | None = None
    tax_document: str | None = None
    timezone: str | None = None
    metadata: dict[str, Any] | None = None
    address: CustomerBatchFailedItemDataAddress | None = None


@dataclass
class CustomerBatchFailedItemDataAddress:
    line1: str = ""
    line2: str | None = None
    city: str = ""
    state: str | None = None
    postal_code: str = ""
    country: str = ""
    region: str | None = None


@dataclass
class CustomerBatchSuccessfulItem:
    id: str = ""
    external_id: str | None = None
    email: str = ""


@dataclass
class CustomerCredit:
    id: str = ""
    amount: int = 0
    applied_amount: int = 0
    reversed_amount: int = 0
    revoked_amount: int = 0
    remaining_amount: int = 0
    currency: str = ""
    reason: str = ""
    source: Literal["dashboard", "api", "plan_change", "migration"] | None = None
    expires_at: str | None = None
    created_at: str = ""
    object: Literal["customer_credit"] | None = None
    livemode: bool = False


@dataclass
class CustomerCreditRevocation:
    id: str = ""
    remaining_amount: int = 0
    revoked_amount: int = 0
    currency: str = ""
    object: Literal["customer_credit"] | None = None
    livemode: bool = False


@dataclass
class CustomersListCreditsResult:
    object: Literal["list"] | None = None
    data: list[CustomerCredit] = field(default_factory=list)
    has_more: bool = False
    next_cursor: str | None = None


@dataclass
class CustomersListPlanGrantsResult:
    object: Literal["list"] | None = None
    data: list[PlanGrant] = field(default_factory=list)
    has_more: bool = False
    next_cursor: str | None = None


@dataclass
class CustomersListResult:
    object: Literal["list"] | None = None
    data: list[Customer] = field(default_factory=list)
    has_more: bool = False
    next_cursor: str | None = None


@dataclass
class DeletedObject:
    id: str = ""
    deleted: Literal[True] | None = None
    object: str = ""
    livemode: bool = False


@dataclass
class DeletedOffer:
    deleted: Literal[True] | None = None
    object: Literal["offer"] | None = None
    livemode: bool = False


@dataclass
class DeletedPlanRegionalPricing:
    deleted: Literal[True] | None = None
    object: Literal["plan_regional_pricing"] | None = None
    livemode: bool = False


@dataclass
class DeletedSubscriptionAddon:
    id: str = ""
    status: Literal["inactive"] | None = None
    deactivated_at: str | None = None
    object: Literal["subscription_addon"] | None = None
    livemode: bool = False


@dataclass
class Feature:
    id: str = ""
    name: str = ""
    code: str = ""
    type: FeatureType | None = None
    description: str | None = None
    unit_name: str | None = None
    created_at: str = ""
    updated_at: str = ""
    object: Literal["feature"] | None = None
    livemode: bool = False


@dataclass
class FeatureAccessListResult:
    object: Literal["list"] | None = None
    data: list[FeatureAccess] = field(default_factory=list)
    has_more: bool = False
    next_cursor: str | None = None


@dataclass
class FeatureAccessVariant1:
    code: str = ""
    name: str = ""
    unit_name: str | None = None
    allowed: bool = False
    type: Literal["boolean"] | None = None
    enabled: bool = False
    base_access: FeatureAccessVariant1BaseAccess | None = None
    object: Literal["feature_access"] | None = None
    livemode: bool = False


@dataclass
class FeatureAccessVariant1BaseAccess:
    enabled: bool = False


@dataclass
class FeatureAccessVariant2:
    code: str = ""
    name: str = ""
    unit_name: str | None = None
    allowed: bool = False
    type: Literal["usage"] | None = None
    consumption: FeatureAccessVariant2Consumption | None = None
    base_access: FeatureAccessVariant2BaseAccess | None = None
    object: Literal["feature_access"] | None = None
    livemode: bool = False


@dataclass
class FeatureAccessVariant2BaseAccess:
    included_units: float = 0.0
    unlimited: bool = False


@dataclass
class FeatureAccessVariant2ConsumptionVariant1:
    model: Literal["metered"] | None = None
    period: FeatureAccessVariant2ConsumptionVariant1Period | None = None
    units_used: float = 0.0
    included_units: float = 0.0
    remaining_units: float | None = None
    unlimited: bool = False
    overage: FeatureAccessVariant2ConsumptionVariant1Overage | None = None


@dataclass
class FeatureAccessVariant2ConsumptionVariant1Overage:
    enabled: bool = False
    units: float = 0.0
    unit_price: FeatureAccessVariant2ConsumptionVariant1OverageUnitPrice | None = None


@dataclass
class FeatureAccessVariant2ConsumptionVariant1OverageUnitPrice:
    amount: int = 0
    currency: str = ""
    scale: Literal[10000] | None = None


@dataclass
class FeatureAccessVariant2ConsumptionVariant1Period:
    start: str = ""
    end: str = ""


@dataclass
class FeatureAccessVariant2ConsumptionVariant2:
    model: Literal["credits"] | None = None
    period: FeatureAccessVariant2ConsumptionVariant2Period | None = None
    units_used: float = 0.0
    credits_per_unit: int = 0
    credits_consumed: float = 0.0
    available_units: int = 0


@dataclass
class FeatureAccessVariant2ConsumptionVariant2Period:
    start: str = ""
    end: str = ""


@dataclass
class FeatureAccessVariant2ConsumptionVariant3:
    model: Literal["balance"] | None = None
    period: FeatureAccessVariant2ConsumptionVariant3Period | None = None
    units_used: float = 0.0
    spent: FeatureAccessVariant2ConsumptionVariant3Spent | None = None
    available_units: int | None = None
    unit_price: FeatureAccessVariant2ConsumptionVariant3UnitPrice | None = None


@dataclass
class FeatureAccessVariant2ConsumptionVariant3Period:
    start: str = ""
    end: str = ""


@dataclass
class FeatureAccessVariant2ConsumptionVariant3Spent:
    amount: int = 0
    currency: str = ""


@dataclass
class FeatureAccessVariant2ConsumptionVariant3UnitPrice:
    amount: int = 0
    currency: str = ""
    scale: Literal[10000] | None = None


@dataclass
class FeatureAccessVariant3:
    code: str = ""
    name: str = ""
    unit_name: str | None = None
    allowed: bool = False
    type: Literal["seats"] | None = None
    usage: FeatureAccessVariant3Usage | None = None
    base_access: FeatureAccessVariant3BaseAccess | None = None
    object: Literal["feature_access"] | None = None
    livemode: bool = False


@dataclass
class FeatureAccessVariant3BaseAccess:
    included_units: float = 0.0
    unlimited: bool = False


@dataclass
class FeatureAccessVariant3Usage:
    period: FeatureAccessVariant3UsagePeriod | None = None
    units_used: float = 0.0
    included_units: float = 0.0
    remaining_units: float | None = None
    unlimited: bool = False
    overage: FeatureAccessVariant3UsageOverage | None = None


@dataclass
class FeatureAccessVariant3UsageOverage:
    enabled: bool = False
    units: float = 0.0
    unit_price: FeatureAccessVariant3UsageOverageUnitPrice | None = None


@dataclass
class FeatureAccessVariant3UsageOverageUnitPrice:
    amount: int = 0
    currency: str = ""
    scale: Literal[10000] | None = None


@dataclass
class FeatureAccessVariant3UsagePeriod:
    start: str = ""
    end: str = ""


@dataclass
class FeatureAccessVariant4:
    code: str = ""
    name: str = ""
    unit_name: str | None = None
    allowed: bool = False
    type: Literal["quota"] | None = None
    usage: FeatureAccessVariant4Usage | None = None
    base_access: FeatureAccessVariant4BaseAccess | None = None
    object: Literal["feature_access"] | None = None
    livemode: bool = False


@dataclass
class FeatureAccessVariant4BaseAccess:
    included_units: float = 0.0
    unlimited: bool = False


@dataclass
class FeatureAccessVariant4Usage:
    period: FeatureAccessVariant4UsagePeriod | None = None
    units_used: float = 0.0
    included_units: float = 0.0
    remaining_units: float | None = None
    unlimited: bool = False
    overage: FeatureAccessVariant4UsageOverage | None = None
    billed_units: float = 0.0


@dataclass
class FeatureAccessVariant4UsageOverage:
    enabled: bool = False
    units: float = 0.0
    unit_price: FeatureAccessVariant4UsageOverageUnitPrice | None = None


@dataclass
class FeatureAccessVariant4UsageOverageUnitPrice:
    amount: int = 0
    currency: str = ""
    scale: Literal[10000] | None = None


@dataclass
class FeatureAccessVariant4UsagePeriod:
    start: str = ""
    end: str = ""


@dataclass
class FeaturesListResult:
    object: Literal["list"] | None = None
    data: list[Feature] = field(default_factory=list)
    has_more: bool = False
    next_cursor: str | None = None


@dataclass
class Invoice:
    id: str = ""
    customer_id: str = ""
    subscription_id: str | None = None
    invoice_number: str = ""
    status: Literal["draft", "outstanding", "paid", "void", "uncollectible"] | None = None
    invoice_type: InvoiceType | None = None
    currency: str = ""
    subtotal: int = 0
    discount_amount: int = 0
    tax_amount: int = 0
    total: int = 0
    period_start: str = ""
    period_end: str = ""
    issue_date: str = ""
    due_date: str = ""
    memo: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: str = ""
    updated_at: str = ""
    credit_applied: int = 0
    plan_name: str | None = None
    po_number: str | None = None
    reference: str | None = None
    line_items: list[InvoiceLineItemsItem] = field(default_factory=list)
    object: Literal["invoice"] | None = None
    livemode: bool = False


@dataclass
class InvoiceDownload:
    url: str = ""
    expires_at: str = ""
    object: Literal["invoice_download_link"] | None = None
    livemode: bool = False


@dataclass
class InvoiceLineItemsItem:
    line_type: (
        Literal[
            "plan_base",
            "feature_overage",
            "feature_seats",
            "feature_quota",
            "discount",
            "promo_code_discount",
            "credit",
            "balance_overage",
            "addon_base",
            "one_time",
        ]
        | None
    ) = None
    feature_name: str | None = None
    description: str = ""
    quantity: int = 0
    unit_amount: int = 0
    amount: int = 0
    included_amount: int | None = None
    used_amount: int | None = None
    overage_amount: int | None = None
    discount_type: str | None = None
    discount_value: int | None = None
    discount_name: str | None = None
    charge_type: Literal["standard", "advance", "true_up"] | None = None


@dataclass
class InvoiceListItem:
    id: str = ""
    customer_id: str = ""
    subscription_id: str | None = None
    invoice_number: str = ""
    status: Literal["draft", "outstanding", "paid", "void", "uncollectible"] | None = None
    invoice_type: InvoiceType | None = None
    currency: str = ""
    subtotal: int = 0
    discount_amount: int = 0
    tax_amount: int = 0
    total: int = 0
    period_start: str = ""
    period_end: str = ""
    issue_date: str = ""
    due_date: str = ""
    memo: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: str = ""
    updated_at: str = ""
    object: Literal["invoice"] | None = None
    livemode: bool = False


@dataclass
class InvoicesListResult:
    object: Literal["list"] | None = None
    data: list[InvoiceListItem] = field(default_factory=list)
    has_more: bool = False
    next_cursor: str | None = None


@dataclass
class Market:
    id: str = ""
    name: str = ""
    country_codes: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: str = ""
    updated_at: str = ""
    object: Literal["market"] | None = None
    livemode: bool = False


@dataclass
class MarketsListResult:
    object: Literal["list"] | None = None
    data: list[Market] = field(default_factory=list)
    has_more: bool = False
    next_cursor: str | None = None


@dataclass
class Offer:
    id: str = ""
    name: str = ""
    phases: list[OfferPhasesItem] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    starts_at: str | None = None
    ends_at: str | None = None
    active: bool = False
    created_at: str = ""
    updated_at: str = ""
    object: Literal["offer"] | None = None
    livemode: bool = False


@dataclass
class OfferPhasesItemVariant1:
    type: Literal["free_trial"] | None = None
    duration_days: int = 0


@dataclass
class OfferPhasesItemVariant2:
    type: Literal["percentage"] | None = None
    duration_cycles: int | None = None
    duration_interval: Literal["weekly", "monthly", "quarterly", "yearly"] | None = None
    percentage: int = 0


@dataclass
class OfferPhasesItemVariant3:
    type: Literal["amount_off"] | None = None
    duration_cycles: int | None = None
    duration_interval: Literal["weekly", "monthly", "quarterly", "yearly"] | None = None
    amounts: list[OfferPhasesItemVariant3AmountsItem] = field(default_factory=list)


@dataclass
class OfferPhasesItemVariant3AmountsItem:
    currency: str = ""
    amount: int = 0


@dataclass
class OfferPhasesItemVariant4:
    type: Literal["fixed_price"] | None = None
    duration_cycles: int | None = None
    duration_interval: Literal["weekly", "monthly", "quarterly", "yearly"] | None = None
    prices: list[OfferPhasesItemVariant4PricesItem] = field(default_factory=list)


@dataclass
class OfferPhasesItemVariant4PricesItem:
    currency: str = ""
    amount: int = 0


@dataclass
class OffersListResult:
    object: Literal["list"] | None = None
    data: list[Offer] = field(default_factory=list)
    has_more: bool = False
    next_cursor: str | None = None


@dataclass
class Payment:
    id: str = ""
    customer_id: str | None = None
    kind: Literal["link", "charge"] | None = None
    status: (
        Literal["pending", "processing", "succeeded", "requires_action", "failed", "canceled"]
        | None
    ) = None
    provider: Literal["stripe", "commet", "dlocal"] | None = None
    amount_subtotal: int = 0
    tax_amount: int = 0
    amount_total: int = 0
    currency: str = ""
    description: str = ""
    metadata: dict[str, Any] | None = None
    url: str | None = None
    expires_at: str | None = None
    created_at: str = ""
    updated_at: str = ""
    object: Literal["payment"] | None = None
    livemode: bool = False


@dataclass
class PaymentMethodUpdateCheckout:
    checkout_url: str = ""
    object: Literal["checkout_session"] | None = None
    livemode: bool = False


@dataclass
class PaymentsListResult:
    object: Literal["list"] | None = None
    data: list[Payment] = field(default_factory=list)
    has_more: bool = False
    next_cursor: str | None = None


@dataclass
class Payout:
    id: str = ""
    status: Literal["pending", "in_transit", "paid", "failed", "canceled"] | None = None
    amount: int = 0
    fee: int = 0
    net_amount: int = 0
    currency: str = ""
    description: str | None = None
    provider_transfer_id: str = ""
    created_at: str = ""
    object: Literal["payout"] | None = None
    livemode: bool = False


@dataclass
class PayoutBankAccount:
    id: str = ""
    provider_external_account_id: str | None = None
    holder_name: str = ""
    last4: str = ""
    bank_name: str | None = None
    country: str = ""
    currency: str = ""
    account_type: Literal["checking", "savings"] | None = None
    is_default: bool = False
    status: Literal["active", "errored"] | None = None
    created_at: str = ""
    object: Literal["payout_bank_account"] | None = None
    livemode: bool = False


@dataclass
class Plan:
    id: str = ""
    name: str = ""
    code: str = ""
    description: str | None = None
    consumption_model: ConsumptionModel | None = None
    is_public: bool = False
    is_default: bool = False
    is_free: bool = False
    block_on_exhaustion: bool | None = None
    sort_order: int = 0
    plan_group_id: str | None = None
    metadata: dict[str, Any] | None = None
    created_at: str = ""
    updated_at: str = ""
    features: list[PlanFeaturesItem] = field(default_factory=list)
    prices: list[PlanPricesItem] = field(default_factory=list)
    exchange_rates: list[PlanExchangeRatesItem] = field(default_factory=list)
    object: Literal["plan"] | None = None
    livemode: bool = False


@dataclass
class PlanChangeVariant1:
    outcome: Literal["requires_checkout"] | None = None
    requires_checkout: Literal[True] | None = None
    checkout_url: str = ""
    offer_application: PlanChangeVariant1OfferApplication | None = None
    object: Literal["plan_change"] | None = None
    livemode: bool = False


@dataclass
class PlanChangeVariant1OfferApplication:
    id: str = ""
    offer_id: str = ""
    name: str = ""
    currency: str = ""
    subtotal: int = 0
    discount_amount: int = 0
    total: int = 0
    phases: list[PlanChangeVariant1OfferApplicationPhasesItem] = field(default_factory=list)
    applies_to: PlanChangeVariant1OfferApplicationAppliesTo | None = None


@dataclass
class PlanChangeVariant1OfferApplicationAppliesToVariant1:
    type: Literal["plan_price"] | None = None
    id: str = ""


@dataclass
class PlanChangeVariant1OfferApplicationAppliesToVariant2:
    type: Literal["addon"] | None = None
    id: str = ""


@dataclass
class PlanChangeVariant1OfferApplicationAppliesToVariant3:
    type: Literal["credit_pack"] | None = None
    id: str = ""


@dataclass
class PlanChangeVariant1OfferApplicationPhasesItemVariant1:
    type: Literal["free_trial"] | None = None
    duration_days: int = 0
    starts_at: str | None = None
    ends_at: str | None = None


@dataclass
class PlanChangeVariant1OfferApplicationPhasesItemVariant2:
    type: Literal["percentage"] | None = None
    duration_cycles: int | None = None
    duration_interval: Literal["weekly", "monthly", "quarterly", "yearly"] | None = None
    starts_at: str | None = None
    ends_at: str | None = None
    percentage: int = 0


@dataclass
class PlanChangeVariant1OfferApplicationPhasesItemVariant3:
    type: Literal["amount_off"] | None = None
    duration_cycles: int | None = None
    duration_interval: Literal["weekly", "monthly", "quarterly", "yearly"] | None = None
    starts_at: str | None = None
    ends_at: str | None = None
    amount: int = 0


@dataclass
class PlanChangeVariant1OfferApplicationPhasesItemVariant4:
    type: Literal["fixed_price"] | None = None
    duration_cycles: int | None = None
    duration_interval: Literal["weekly", "monthly", "quarterly", "yearly"] | None = None
    starts_at: str | None = None
    ends_at: str | None = None
    price: int = 0


@dataclass
class PlanChangeVariant2:
    outcome: Literal["scheduled"] | None = None
    id: str = ""
    scheduled: Literal[True] | None = None
    scheduled_for: str = ""
    change_type: (
        Literal[
            "subscription.plan_downgrade", "subscription.interval_change", "subscription.cancel"
        ]
        | None
    ) = None
    customer_id: str = ""
    new_plan_id: str | None = None
    new_plan_name: str | None = None
    new_billing_interval: str | None = None
    seat_limit_warning: PlanChangeVariant2SeatLimitWarning | None = None
    object: Literal["plan_change"] | None = None
    livemode: bool = False


@dataclass
class PlanChangeVariant2SeatLimitWarning:
    feature_code: str = ""
    feature_name: str = ""
    current_seats: int = 0
    included: int = 0
    new_plan_name: str = ""
    effective_date: str = ""


@dataclass
class PlanChangeVariant3:
    outcome: Literal["completed"] | None = None
    id: str = ""
    scheduled: Literal[False] | None = None
    customer_id: str = ""
    previous_plan: PlanChangeVariant3PreviousPlan | None = None
    current_plan: PlanChangeVariant3CurrentPlan | None = None
    billing_interval: str = ""
    billing: PlanChangeVariant3Billing | None = None
    invoice_id: str | None = None
    offer_application: PlanChangeVariant3OfferApplication | None = None
    object: Literal["plan_change"] | None = None
    livemode: bool = False


@dataclass
class PlanChangeVariant3Billing:
    credit: int = 0
    credits_applied: int = 0
    charge: int = 0
    tax_amount: int = 0
    net_amount: int = 0
    total_charged: int = 0
    remaining_credit_balance: int = 0


@dataclass
class PlanChangeVariant3CurrentPlan:
    id: str = ""
    name: str = ""
    price: int = 0


@dataclass
class PlanChangeVariant3OfferApplication:
    id: str = ""
    offer_id: str = ""
    name: str = ""
    currency: str = ""
    subtotal: int = 0
    discount_amount: int = 0
    total: int = 0
    phases: list[PlanChangeVariant3OfferApplicationPhasesItem] = field(default_factory=list)
    applies_to: PlanChangeVariant3OfferApplicationAppliesTo | None = None


@dataclass
class PlanChangeVariant3OfferApplicationAppliesToVariant1:
    type: Literal["plan_price"] | None = None
    id: str = ""


@dataclass
class PlanChangeVariant3OfferApplicationAppliesToVariant2:
    type: Literal["addon"] | None = None
    id: str = ""


@dataclass
class PlanChangeVariant3OfferApplicationAppliesToVariant3:
    type: Literal["credit_pack"] | None = None
    id: str = ""


@dataclass
class PlanChangeVariant3OfferApplicationPhasesItemVariant1:
    type: Literal["free_trial"] | None = None
    duration_days: int = 0
    starts_at: str | None = None
    ends_at: str | None = None


@dataclass
class PlanChangeVariant3OfferApplicationPhasesItemVariant2:
    type: Literal["percentage"] | None = None
    duration_cycles: int | None = None
    duration_interval: Literal["weekly", "monthly", "quarterly", "yearly"] | None = None
    starts_at: str | None = None
    ends_at: str | None = None
    percentage: int = 0


@dataclass
class PlanChangeVariant3OfferApplicationPhasesItemVariant3:
    type: Literal["amount_off"] | None = None
    duration_cycles: int | None = None
    duration_interval: Literal["weekly", "monthly", "quarterly", "yearly"] | None = None
    starts_at: str | None = None
    ends_at: str | None = None
    amount: int = 0


@dataclass
class PlanChangeVariant3OfferApplicationPhasesItemVariant4:
    type: Literal["fixed_price"] | None = None
    duration_cycles: int | None = None
    duration_interval: Literal["weekly", "monthly", "quarterly", "yearly"] | None = None
    starts_at: str | None = None
    ends_at: str | None = None
    price: int = 0


@dataclass
class PlanChangeVariant3PreviousPlan:
    id: str = ""
    name: str = ""


@dataclass
class PlanExchangeRatesItem:
    currency: str = ""
    exchange_rate: float = 0.0


@dataclass
class PlanFeature:
    plan_id: str = ""
    feature_id: str = ""
    enabled: bool = False
    included_amount: int = 0
    unlimited: bool = False
    overage: PlanFeatureOverage | None = None
    credits_per_unit: int | None = None
    pricing_mode: Literal["fixed", "ai_model"] | None = None
    margin: int | None = None
    object: Literal["plan_feature"] | None = None
    livemode: bool = False


@dataclass
class PlanFeatureOverage:
    enabled: bool = False
    unit_price: int = 0


@dataclass
class PlanFeaturesItem:
    code: str = ""
    name: str = ""
    type: FeatureType | None = None
    unit_name: str | None = None
    enabled: bool = False
    included_amount: int | None = None
    unlimited: bool = False
    overage: PlanFeaturesItemOverage | None = None
    regional_prices: list[PlanFeaturesItemRegionalPricesItem] = field(default_factory=list)


@dataclass
class PlanFeaturesItemOverage:
    enabled: bool = False
    model: Literal["per_unit"] | None = None
    unit_price: int | None = None


@dataclass
class PlanFeaturesItemRegionalPricesItem:
    currency: str = ""
    overage_unit_price: int | None = None
    auto_synced: bool = False


@dataclass
class PlanGrant:
    id: str = ""
    customer_id: str = ""
    subscription_id: str = ""
    base_plan_id: str = ""
    plan_id: str = ""
    plan_release_id: str = ""
    status: Literal["active", "expired", "revoked"] | None = None
    duration: Literal["cycles", "until_date", "until_revoked"] | None = None
    duration_cycles: int | None = None
    starts_at: str = ""
    expires_at: str | None = None
    reason: str = ""
    source: Literal["dashboard", "api"] | None = None
    revoked_at: str | None = None
    created_at: str = ""
    updated_at: str = ""
    events: list[PlanGrantEventsItem] = field(default_factory=list)
    object: Literal["plan_grant"] | None = None
    livemode: bool = False


@dataclass
class PlanGrantEventsItem:
    id: str = ""
    type: Literal["created", "updated", "expired", "revoked"] | None = None
    reason: str = ""
    source: Literal["dashboard", "api", "system"] | None = None
    previous_expires_at: str | None = None
    expires_at: str | None = None
    duration: Literal["cycles", "until_date", "until_revoked"] | None = None
    duration_cycles: int | None = None
    requested_expires_at: str | None = None
    created_at: str = ""


@dataclass
class PlanGroup:
    id: str = ""
    name: str = ""
    description: str | None = None
    is_public: bool = False
    created_at: str = ""
    updated_at: str = ""
    object: Literal["plan_group"] | None = None
    livemode: bool = False


@dataclass
class PlanGroupDetail:
    id: str = ""
    name: str = ""
    description: str | None = None
    is_public: bool = False
    created_at: str = ""
    updated_at: str = ""
    plans: list[PlanGroupDetailPlansItem] = field(default_factory=list)
    object: Literal["plan_group"] | None = None
    livemode: bool = False


@dataclass
class PlanGroupDetailPlansItem:
    id: str = ""
    name: str = ""
    sort_order: int = 0


@dataclass
class PlanGroupsListResult:
    object: Literal["list"] | None = None
    data: list[PlanGroup] = field(default_factory=list)
    has_more: bool = False
    next_cursor: str | None = None


@dataclass
class PlanPrice:
    id: str = ""
    plan_id: str = ""
    billing_interval: BillingInterval | None = None
    price: int = 0
    is_default: bool = False
    trial_days: int = 0
    included_balance: int | None = None
    included_credits: int | None = None
    offer_id: str | None = None
    inherits_from_price_id: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    market_prices: list[PlanPriceMarketPricesItem] = field(default_factory=list)
    created_at: str = ""
    updated_at: str = ""
    object: Literal["plan_price"] | None = None
    livemode: bool = False


@dataclass
class PlanPriceMarketPricesItem:
    market_group_id: str = ""
    currency: str = ""
    price: int = 0


@dataclass
class PlanPricesItem:
    id: str = ""
    billing_interval: BillingInterval | None = None
    price: int = 0
    is_default: bool = False
    trial_days: int = 0
    included_balance: int | None = None
    included_credits: int | None = None
    offer_id: str | None = None
    inherits_from_price_id: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    market_prices: list[PlanPricesItemMarketPricesItem] = field(default_factory=list)
    regional_prices: list[PlanPricesItemRegionalPricesItem] = field(default_factory=list)


@dataclass
class PlanPricesItemMarketPricesItem:
    market_group_id: str = ""
    currency: str = ""
    price: int = 0


@dataclass
class PlanPricesItemRegionalPricesItem:
    currency: str = ""
    price: int = 0
    included_balance: int | None = None
    auto_synced: bool = False


@dataclass
class PlanRegionalPricing:
    price_id: str = ""
    overrides: list[PlanRegionalPricingOverridesItem] = field(default_factory=list)
    object: Literal["plan_regional_pricing"] | None = None
    livemode: bool = False


@dataclass
class PlanRegionalPricingOverridesItem:
    currency: str = ""
    price: int = 0
    included_balance: int | None = None


@dataclass
class PlanRegionalPricingResult:
    plan_id: str = ""
    currency: str = ""
    exchange_rate: float = 0.0
    prices_configured: int = 0
    features_configured: int = 0
    object: Literal["plan_regional_pricing"] | None = None
    livemode: bool = False


@dataclass
class PlansListResult:
    object: Literal["list"] | None = None
    data: list[Plan] = field(default_factory=list)
    has_more: bool = False
    next_cursor: str | None = None


@dataclass
class PortalAccess:
    portal_url: str = ""
    object: Literal["portal_session"] | None = None
    livemode: bool = False


@dataclass
class PreviewChange:
    currency: str = ""
    current_plan_credit: int = 0
    new_plan_charge: int = 0
    estimated_total: int = 0
    effective_date: str = ""
    days_remaining: int = 0
    total_days: int = 0
    is_upgrade: bool = False
    offer_application: PreviewChangeOfferApplication | None = None
    object: Literal["plan_change_preview"] | None = None
    livemode: bool = False


@dataclass
class PreviewChangeOfferApplication:
    id: str = ""
    offer_id: str = ""
    name: str = ""
    currency: str = ""
    subtotal: int = 0
    discount_amount: int = 0
    total: int = 0
    phases: list[PreviewChangeOfferApplicationPhasesItem] = field(default_factory=list)
    applies_to: PreviewChangeOfferApplicationAppliesTo | None = None


@dataclass
class PreviewChangeOfferApplicationAppliesToVariant1:
    type: Literal["plan_price"] | None = None
    id: str = ""


@dataclass
class PreviewChangeOfferApplicationAppliesToVariant2:
    type: Literal["addon"] | None = None
    id: str = ""


@dataclass
class PreviewChangeOfferApplicationAppliesToVariant3:
    type: Literal["credit_pack"] | None = None
    id: str = ""


@dataclass
class PreviewChangeOfferApplicationPhasesItemVariant1:
    type: Literal["free_trial"] | None = None
    duration_days: int = 0
    starts_at: str | None = None
    ends_at: str | None = None


@dataclass
class PreviewChangeOfferApplicationPhasesItemVariant2:
    type: Literal["percentage"] | None = None
    duration_cycles: int | None = None
    duration_interval: Literal["weekly", "monthly", "quarterly", "yearly"] | None = None
    starts_at: str | None = None
    ends_at: str | None = None
    percentage: int = 0


@dataclass
class PreviewChangeOfferApplicationPhasesItemVariant3:
    type: Literal["amount_off"] | None = None
    duration_cycles: int | None = None
    duration_interval: Literal["weekly", "monthly", "quarterly", "yearly"] | None = None
    starts_at: str | None = None
    ends_at: str | None = None
    amount: int = 0


@dataclass
class PreviewChangeOfferApplicationPhasesItemVariant4:
    type: Literal["fixed_price"] | None = None
    duration_cycles: int | None = None
    duration_interval: Literal["weekly", "monthly", "quarterly", "yearly"] | None = None
    starts_at: str | None = None
    ends_at: str | None = None
    price: int = 0


@dataclass
class PromoCode:
    id: str = ""
    code: str = ""
    offer_id: str = ""
    billing_interval: BillingInterval | None = None
    max_redemptions: int | None = None
    expires_at: str | None = None
    is_active: bool = False
    redemption_count: int = 0
    created_at: str = ""
    updated_at: str = ""
    object: Literal["promo_code"] | None = None
    livemode: bool = False


@dataclass
class PromoCodesListResult:
    object: Literal["list"] | None = None
    data: list[PromoCode] = field(default_factory=list)
    has_more: bool = False
    next_cursor: str | None = None


@dataclass
class QuotaGetAllResult:
    object: Literal["list"] | None = None
    data: list[UsageQuota] = field(default_factory=list)
    has_more: bool = False
    next_cursor: str | None = None


@dataclass
class ReactivatedSubscription:
    subscription_id: str = ""
    invoice_id: str = ""
    status: Literal["processing", "succeeded"] | None = None
    offer_application: ReactivatedSubscriptionOfferApplication | None = None
    object: Literal["subscription_reactivation"] | None = None
    livemode: bool = False


@dataclass
class ReactivatedSubscriptionOfferApplication:
    id: str = ""
    offer_id: str = ""
    name: str = ""
    currency: str = ""
    subtotal: int = 0
    discount_amount: int = 0
    total: int = 0
    phases: list[ReactivatedSubscriptionOfferApplicationPhasesItem] = field(default_factory=list)
    applies_to: ReactivatedSubscriptionOfferApplicationAppliesTo | None = None


@dataclass
class ReactivatedSubscriptionOfferApplicationAppliesToVariant1:
    type: Literal["plan_price"] | None = None
    id: str = ""


@dataclass
class ReactivatedSubscriptionOfferApplicationAppliesToVariant2:
    type: Literal["addon"] | None = None
    id: str = ""


@dataclass
class ReactivatedSubscriptionOfferApplicationAppliesToVariant3:
    type: Literal["credit_pack"] | None = None
    id: str = ""


@dataclass
class ReactivatedSubscriptionOfferApplicationPhasesItemVariant1:
    type: Literal["free_trial"] | None = None
    duration_days: int = 0
    starts_at: str | None = None
    ends_at: str | None = None


@dataclass
class ReactivatedSubscriptionOfferApplicationPhasesItemVariant2:
    type: Literal["percentage"] | None = None
    duration_cycles: int | None = None
    duration_interval: Literal["weekly", "monthly", "quarterly", "yearly"] | None = None
    starts_at: str | None = None
    ends_at: str | None = None
    percentage: int = 0


@dataclass
class ReactivatedSubscriptionOfferApplicationPhasesItemVariant3:
    type: Literal["amount_off"] | None = None
    duration_cycles: int | None = None
    duration_interval: Literal["weekly", "monthly", "quarterly", "yearly"] | None = None
    starts_at: str | None = None
    ends_at: str | None = None
    amount: int = 0


@dataclass
class ReactivatedSubscriptionOfferApplicationPhasesItemVariant4:
    type: Literal["fixed_price"] | None = None
    duration_cycles: int | None = None
    duration_interval: Literal["weekly", "monthly", "quarterly", "yearly"] | None = None
    starts_at: str | None = None
    ends_at: str | None = None
    price: int = 0


@dataclass
class RecoveryLink:
    url: str = ""
    token: str = ""
    object: Literal["recovery_link"] | None = None
    livemode: bool = False


@dataclass
class Refund:
    id: str = ""
    transaction_id: str = ""
    amount: int = 0
    currency: str = ""
    charge_id: str | None = None
    status: Literal["pending", "requires_action", "succeeded", "failed", "canceled"] | None = None
    reason: Literal["duplicate", "fraudulent", "requested_by_customer"] | None = None
    object: Literal["refund"] | None = None
    livemode: bool = False


@dataclass
class RemovedPlanFeature:
    id: str = ""
    removed: Literal[True] | None = None
    object: Literal["plan_feature"] | None = None
    livemode: bool = False


@dataclass
class RemovedPlanFromGroup:
    id: str = ""
    removed: bool = False
    object: Literal["plan_group_membership"] | None = None
    livemode: bool = False


@dataclass
class ReorderedPlans:
    reordered: bool = False
    object: Literal["plan_group_order"] | None = None
    livemode: bool = False


@dataclass
class SeatBalance:
    current: int = 0
    as_of: str = ""
    object: Literal["seat_balance"] | None = None
    livemode: bool = False


@dataclass
class SeatBalanceCollection:
    balances: dict[str, SeatBalanceCollectionBalancesValue] = field(default_factory=dict)
    object: Literal["seat_balance_collection"] | None = None
    livemode: bool = False


@dataclass
class SeatBalanceCollectionBalancesValue:
    current: int = 0
    as_of: str = ""


@dataclass
class SeatEvent:
    id: str = ""
    customer_id: str = ""
    feature_code: str = ""
    previous_balance: int = 0
    new_balance: int = 0
    ts: str = ""
    created_at: str = ""
    object: Literal["seat_event"] | None = None
    livemode: bool = False


@dataclass
class SeatsSetAllResult:
    object: Literal["list"] | None = None
    data: list[SeatEvent] = field(default_factory=list)
    has_more: bool = False
    next_cursor: str | None = None


@dataclass
class SentInvoice:
    sent: bool = False
    sent_at: str = ""
    object: Literal["invoice_delivery"] | None = None
    livemode: bool = False


@dataclass
class SetPlanRegionalPricingParamsFeaturesItem:
    feature_id: str = ""
    overage_unit_price: int = 0


@dataclass
class SetPlanRegionalPricingParamsPricesItem:
    price_id: str = ""
    price: int = 0
    included_balance: int | None = None


@dataclass
class Subscription:
    id: str = ""
    customer_id: str = ""
    plan: SubscriptionPlan | None = None
    name: str = ""
    description: str | None = None
    status: SubscriptionStatus | None = None
    billing_interval: BillingInterval | None = None
    trial_ends_at: str | None = None
    current_period: SubscriptionCurrentPeriod | None = None
    cancellation: SubscriptionCancellation | None = None
    cancel_at_period_end: bool = False
    scheduled_plan_change: SubscriptionScheduledPlanChange | None = None
    start_date: str = ""
    end_date: str | None = None
    billing_day_of_month: int | None = None
    next_billing_date: str | None = None
    checkout_url: str | None = None
    created_at: str = ""
    updated_at: str = ""
    offer_applications: list[SubscriptionOfferApplication] = field(default_factory=list)
    plan_grant: SubscriptionPlanGrant | None = None
    consumption_model: ConsumptionModel | None = None
    features: list[SubscriptionFeaturesItem] = field(default_factory=list)
    credits: SubscriptionCredits | None = None
    balance: SubscriptionBalance | None = None
    price_id: str | None = None
    object: Literal["subscription"] | None = None
    livemode: bool = False


@dataclass
class SubscriptionAddon:
    addon_id: str = ""
    status: Literal["active"] | None = None
    prorated_charge: int = 0
    object: Literal["subscription_addon"] | None = None
    livemode: bool = False


@dataclass
class SubscriptionBalance:
    remaining: float = 0.0
    included: float = 0.0
    currency: str = ""


@dataclass
class SubscriptionCancellation:
    scheduled_at: str = ""
    reason: str | None = None
    effective_at: str = ""


@dataclass
class SubscriptionCredits:
    remaining: float = 0.0
    included: float = 0.0
    purchased: float = 0.0


@dataclass
class SubscriptionCurrentPeriod:
    start: str = ""
    end: str = ""
    days_remaining: float = 0.0


@dataclass
class SubscriptionFeaturesItemVariant1:
    code: str = ""
    name: str = ""
    type: Literal["boolean"] | None = None
    enabled: bool = False
    base_access: SubscriptionFeaturesItemVariant1BaseAccess | None = None


@dataclass
class SubscriptionFeaturesItemVariant1BaseAccess:
    enabled: bool = False


@dataclass
class SubscriptionFeaturesItemVariant2:
    code: str = ""
    name: str = ""
    type: Literal["usage"] | None = None
    usage: SubscriptionFeaturesItemVariant2Usage | None = None
    base_access: SubscriptionFeaturesItemVariant2BaseAccess | None = None


@dataclass
class SubscriptionFeaturesItemVariant2BaseAccess:
    included: float = 0.0
    unlimited: bool = False


@dataclass
class SubscriptionFeaturesItemVariant2Usage:
    current: float = 0.0
    included: float = 0.0
    overage_quantity: float = 0.0
    overage_unit_price: float | None = None
    unlimited: bool | None = None


@dataclass
class SubscriptionFeaturesItemVariant3:
    code: str = ""
    name: str = ""
    type: Literal["seats"] | None = None
    usage: SubscriptionFeaturesItemVariant3Usage | None = None
    base_access: SubscriptionFeaturesItemVariant3BaseAccess | None = None


@dataclass
class SubscriptionFeaturesItemVariant3BaseAccess:
    included: float = 0.0
    unlimited: bool = False


@dataclass
class SubscriptionFeaturesItemVariant3Usage:
    current: float = 0.0
    included: float = 0.0
    overage_quantity: float = 0.0
    overage_unit_price: float | None = None
    unlimited: bool | None = None


@dataclass
class SubscriptionFeaturesItemVariant4:
    code: str = ""
    name: str = ""
    type: Literal["quota"] | None = None
    usage: SubscriptionFeaturesItemVariant4Usage | None = None
    base_access: SubscriptionFeaturesItemVariant4BaseAccess | None = None


@dataclass
class SubscriptionFeaturesItemVariant4BaseAccess:
    included: float = 0.0
    unlimited: bool = False


@dataclass
class SubscriptionFeaturesItemVariant4Usage:
    current: float = 0.0
    included: float = 0.0
    overage_quantity: float = 0.0
    overage_unit_price: float | None = None
    unlimited: bool | None = None


@dataclass
class SubscriptionOfferApplication:
    id: str = ""
    name: str = ""
    applies_to: SubscriptionOfferApplicationAppliesTo | None = None
    offer_id: str | None = None
    source: Literal["direct", "introductory", "promo_code", "card_promotion", "custom"] | None = (
        None
    )
    status: Literal["quoted", "applied", "failed", "expired"] | None = None
    currency: str | None = None
    subtotal: int | None = None
    discount_amount: int | None = None
    total: int | None = None
    phases: list[SubscriptionOfferApplicationPhase] = field(default_factory=list)
    quoted_at: str = ""
    expires_at: str | None = None
    applied_at: str | None = None


@dataclass
class SubscriptionOfferApplicationAppliesToVariant1:
    type: Literal["plan_price"] | None = None
    id: str = ""


@dataclass
class SubscriptionOfferApplicationAppliesToVariant2:
    type: Literal["addon"] | None = None
    id: str = ""


@dataclass
class SubscriptionOfferApplicationAppliesToVariant3:
    type: Literal["credit_pack"] | None = None
    id: str = ""


@dataclass
class SubscriptionOfferApplicationPhaseVariant1:
    type: Literal["free_trial"] | None = None
    duration_days: int = 0
    duration_interval: Literal["weekly", "monthly", "quarterly", "yearly"] | None = None
    starts_at: str | None = None
    ends_at: str | None = None


@dataclass
class SubscriptionOfferApplicationPhaseVariant2:
    type: Literal["percentage"] | None = None
    duration_cycles: int | None = None
    duration_interval: Literal["weekly", "monthly", "quarterly", "yearly"] | None = None
    percentage: int = 0
    starts_at: str | None = None
    ends_at: str | None = None


@dataclass
class SubscriptionOfferApplicationPhaseVariant3:
    type: Literal["amount_off"] | None = None
    duration_cycles: int | None = None
    duration_interval: Literal["weekly", "monthly", "quarterly", "yearly"] | None = None
    amount: int = 0
    starts_at: str | None = None
    ends_at: str | None = None


@dataclass
class SubscriptionOfferApplicationPhaseVariant4:
    type: Literal["fixed_price"] | None = None
    duration_cycles: int | None = None
    duration_interval: Literal["weekly", "monthly", "quarterly", "yearly"] | None = None
    price: int = 0
    starts_at: str | None = None
    ends_at: str | None = None


@dataclass
class SubscriptionPlan:
    id: str = ""
    name: str = ""
    base_price: float = 0.0


@dataclass
class SubscriptionPlanGrant:
    id: str = ""
    plan: SubscriptionPlanGrantPlan | None = None
    expires_at: str | None = None


@dataclass
class SubscriptionPlanGrantPlan:
    id: str = ""
    name: str = ""


@dataclass
class SubscriptionScheduledPlanChange:
    change_type: Literal["plan_downgrade", "interval_change"] | None = None
    new_plan_id: str | None = None
    new_plan_name: str | None = None
    new_billing_interval: str | None = None
    scheduled_for: str = ""


@dataclass
class SubscriptionsListResult:
    object: Literal["list"] | None = None
    data: list[SubscriptionSummary] = field(default_factory=list)
    has_more: bool = False
    next_cursor: str | None = None


@dataclass
class SubscriptionSummary:
    id: str = ""
    customer_id: str = ""
    plan: SubscriptionSummaryPlan | None = None
    name: str = ""
    description: str | None = None
    status: SubscriptionStatus | None = None
    billing_interval: BillingInterval | None = None
    trial_ends_at: str | None = None
    current_period: SubscriptionSummaryCurrentPeriod | None = None
    cancellation: SubscriptionSummaryCancellation | None = None
    cancel_at_period_end: bool = False
    scheduled_plan_change: SubscriptionSummaryScheduledPlanChange | None = None
    start_date: str = ""
    end_date: str | None = None
    billing_day_of_month: int | None = None
    next_billing_date: str | None = None
    checkout_url: str | None = None
    created_at: str = ""
    updated_at: str = ""
    offer_applications: list[SubscriptionOfferApplication] = field(default_factory=list)
    price_id: str | None = None
    object: Literal["subscription"] | None = None
    livemode: bool = False


@dataclass
class SubscriptionSummaryCancellation:
    scheduled_at: str = ""
    reason: str | None = None
    effective_at: str = ""


@dataclass
class SubscriptionSummaryCurrentPeriod:
    start: str = ""
    end: str = ""
    days_remaining: float = 0.0


@dataclass
class SubscriptionSummaryPlan:
    id: str = ""
    name: str = ""


@dataclass
class SubscriptionSummaryScheduledPlanChange:
    change_type: Literal["plan_downgrade", "interval_change"] | None = None
    new_plan_id: str | None = None
    new_plan_name: str | None = None
    new_billing_interval: str | None = None
    scheduled_for: str = ""


@dataclass
class TestClock:
    simulated_time: str | None = None
    is_active: bool = False
    now: str = ""
    latest_run: TestClockLatestRun | None = None
    object: Literal["test_clock"] | None = None
    livemode: bool = False


@dataclass
class TestClockLatestRun:
    id: str = ""
    status: Literal["pending", "running", "completed", "failed"] | None = None
    started_at_time: str = ""
    target_time: str = ""
    estimated_deadline_count: int = 0
    completed_deadline_count: int = 0
    failed_deadline_count: int = 0
    error: str | None = None
    items: list[TestClockLatestRunItemsItem] = field(default_factory=list)


@dataclass
class TestClockLatestRunItemsItem:
    kind: Literal["billing_cycle", "dunning_retry"] | None = None
    status: Literal["pending", "processing", "completed", "failed"] | None = None
    due_at: str = ""
    subscription_id: str = ""
    customer_name: str | None = None
    invoice_number: str | None = None
    invoice_id: str | None = None
    outcome: str | None = None
    detail: str | None = None
    error: str | None = None


@dataclass
class TestClockRun:
    id: str = ""
    status: Literal["pending", "running", "completed", "failed"] | None = None
    started_at_time: str = ""
    target_time: str = ""
    estimated_deadline_count: int = 0
    completed_deadline_count: int = 0
    failed_deadline_count: int = 0
    error: str | None = None
    items: list[TestClockRunItemsItem] = field(default_factory=list)
    object: Literal["test_clock_run"] | None = None
    livemode: bool = False


@dataclass
class TestClockRunItemsItem:
    kind: Literal["billing_cycle", "dunning_retry"] | None = None
    status: Literal["pending", "processing", "completed", "failed"] | None = None
    due_at: str = ""
    subscription_id: str = ""
    customer_name: str | None = None
    invoice_number: str | None = None
    invoice_id: str | None = None
    outcome: str | None = None
    detail: str | None = None
    error: str | None = None


@dataclass
class TrackUsageParamsPropertiesItem:
    property: str = ""
    value: str = ""


@dataclass
class Transaction:
    id: str = ""
    invoice_id: str | None = None
    gross_amount: int | None = None
    subtotal: int | None = None
    tax_amount: int | None = None
    presentment_amount: int | None = None
    currency: str = ""
    provider: PaymentProvider | None = None
    status: TransactionStatus | None = None
    customer_email: str | None = None
    customer_name: str | None = None
    paid_at: str | None = None
    created_at: str = ""
    updated_at: str = ""
    available_at: str | None = None
    object: Literal["transaction"] | None = None
    livemode: bool = False


@dataclass
class TransactionListItem:
    id: str = ""
    invoice_id: str | None = None
    gross_amount: int | None = None
    subtotal: int | None = None
    tax_amount: int | None = None
    presentment_amount: int | None = None
    currency: str = ""
    provider: PaymentProvider | None = None
    status: TransactionStatus | None = None
    customer_email: str | None = None
    customer_name: str | None = None
    paid_at: str | None = None
    created_at: str = ""
    updated_at: str = ""
    object: Literal["transaction"] | None = None
    livemode: bool = False


@dataclass
class TransactionRetry:
    original_transaction_id: str = ""
    invoice_id: str = ""
    status: Literal["processing", "succeeded"] | None = None
    object: Literal["transaction_retry"] | None = None
    livemode: bool = False


@dataclass
class TransactionsListResult:
    object: Literal["list"] | None = None
    data: list[TransactionListItem] = field(default_factory=list)
    has_more: bool = False
    next_cursor: str | None = None


@dataclass
class UpdateCustomerParamsAddress:
    line1: str = ""
    line2: str | None = None
    city: str = ""
    state: str | None = None
    postal_code: str = ""
    country: str = ""
    region: str | None = None


@dataclass
class UpdateOfferParamsPhasesItemVariant1:
    type: Literal["free_trial"] | None = None
    duration_days: int = 0


@dataclass
class UpdateOfferParamsPhasesItemVariant2:
    type: Literal["percentage"] | None = None
    duration_cycles: int | None = None
    duration_interval: Literal["weekly", "monthly", "quarterly", "yearly"] | None = None
    percentage: int = 0


@dataclass
class UpdateOfferParamsPhasesItemVariant3:
    type: Literal["amount_off"] | None = None
    duration_cycles: int | None = None
    duration_interval: Literal["weekly", "monthly", "quarterly", "yearly"] | None = None
    amounts: list[UpdateOfferParamsPhasesItemVariant3AmountsItem] = field(default_factory=list)


@dataclass
class UpdateOfferParamsPhasesItemVariant3AmountsItem:
    currency: str = ""
    amount: int = 0


@dataclass
class UpdateOfferParamsPhasesItemVariant4:
    type: Literal["fixed_price"] | None = None
    duration_cycles: int | None = None
    duration_interval: Literal["weekly", "monthly", "quarterly", "yearly"] | None = None
    prices: list[UpdateOfferParamsPhasesItemVariant4PricesItem] = field(default_factory=list)


@dataclass
class UpdateOfferParamsPhasesItemVariant4PricesItem:
    currency: str = ""
    amount: int = 0


@dataclass
class UpdatePlanFeatureParamsOverage:
    enabled: bool | None = None
    unit_price: int | None = None


@dataclass
class UpdatePlanPriceParamsMarketPricesItem:
    market_group_id: str = ""
    currency: (
        Literal[
            "usd",
            "ars",
            "brl",
            "clp",
            "cop",
            "pen",
            "uyu",
            "pyg",
            "bob",
            "mxn",
            "cad",
            "eur",
            "jpy",
            "cny",
            "krw",
            "hkd",
            "sgd",
            "twd",
            "inr",
            "thb",
        ]
        | None
    ) = None
    price: int = 0


@dataclass
class UpsertRegionalPricesParamsOverridesItem:
    currency: str = ""
    price: int = 0
    included_balance: int | None = None


@dataclass
class UsageAdjustment:
    id: str = ""
    value: int = 0
    previous_value: int = 0
    adjustment: int = 0
    customer_id: str = ""
    reason: str | None = None
    ts: str = ""
    created_at: str = ""
    feature_code: str = ""
    object: Literal["usage_adjustment"] | None = None
    livemode: bool = False


@dataclass
class UsageCheckVariant1:
    allowed: bool = False
    subscription_status: str = ""
    feature_code: str = ""
    quantity: int = 0
    reason: str | None = None
    message: str | None = None
    consumption_model: Literal["metered"] | None = None
    current: float = 0.0
    remaining: float = 0.0
    unlimited: bool = False
    included: float = 0.0
    overage_enabled: bool = False
    overage_unit_price: float | None = None
    object: Literal["usage_check"] | None = None
    livemode: bool = False


@dataclass
class UsageCheckVariant2:
    allowed: bool = False
    subscription_status: str = ""
    feature_code: str = ""
    quantity: int = 0
    reason: str | None = None
    message: str | None = None
    consumption_model: Literal["credits"] | None = None
    credits_per_unit: int = 0
    estimated_credits: int = 0
    plan_credits: int = 0
    purchased_credits: int = 0
    total_credits: int = 0
    object: Literal["usage_check"] | None = None
    livemode: bool = False


@dataclass
class UsageCheckVariant3:
    allowed: bool = False
    subscription_status: str = ""
    feature_code: str = ""
    quantity: int = 0
    reason: str | None = None
    message: str | None = None
    consumption_model: Literal["balance"] | None = None
    unit_price: float = 0.0
    estimated_amount: float = 0.0
    current_balance: float = 0.0
    block_on_exhaustion: bool = False
    currency: str = ""
    object: Literal["usage_check"] | None = None
    livemode: bool = False


@dataclass
class UsageEvent:
    id: str = ""
    feature_code: str = ""
    value: float = 0.0
    customer_id: str = ""
    event_id: str | None = None
    ts: str = ""
    created_at: str = ""
    properties: list[UsageEventPropertiesItem] = field(default_factory=list)
    consumption: UsageEventConsumption | None = None
    object: Literal["usage_event"] | None = None
    livemode: bool = False


@dataclass
class UsageEventConsumption:
    model: Literal["credits", "balance"] | None = None
    deducted: float = 0.0
    remaining: float = 0.0
    blocked: bool = False


@dataclass
class UsageEventPropertiesItem:
    property: str = ""
    value: str = ""


@dataclass
class UsageQuota:
    feature_code: str = ""
    current: float = 0.0
    included: float = 0.0
    remaining: float | None = None
    billed_quantity: float = 0.0
    unlimited: bool = False
    overage_enabled: bool = False
    as_of: str | None = None
    object: Literal["usage_quota"] | None = None
    livemode: bool = False


@dataclass
class UsageQuotaEvent:
    id: str = ""
    customer_id: str = ""
    feature_code: str = ""
    previous_balance: int = 0
    new_balance: int = 0
    ts: str = ""
    created_at: str = ""
    object: Literal["usage_quota_event"] | None = None
    livemode: bool = False


@dataclass
class Webhook:
    id: str = ""
    url: str = ""
    events: list[str] = field(default_factory=list)
    description: str | None = None
    is_active: bool = False
    api_version: str | None = None
    created_at: str = ""
    object: Literal["webhook"] | None = None
    livemode: bool = False


@dataclass
class WebhookAddonRef:
    id: str = ""
    name: str = ""


@dataclass
class WebhookBalance:
    current_balance: float = 0.0


@dataclass
class WebhookBankRef:
    bank_name: str | None = None
    last4: str = ""


@dataclass
class WebhookCardInfo:
    brand: str = ""
    last4: str = ""
    exp_month: float = 0.0
    exp_year: float = 0.0


@dataclass
class WebhookCreditsBalance:
    plan_credits: float = 0.0
    purchased_credits: float = 0.0
    total_credits: float = 0.0


@dataclass
class WebhookPlanGrantTimelineEvent:
    id: str = ""
    type: Literal["created", "updated", "expired", "revoked"] | None = None
    reason: str = ""
    source: Literal["dashboard", "api", "system"] | None = None
    previous_expires_at: str | None = None
    expires_at: str | None = None
    duration: Literal["cycles", "until_date", "until_revoked"] | None = None
    duration_cycles: int | None = None
    requested_expires_at: str | None = None
    created_at: str = ""


@dataclass
class WebhookPlanRef:
    id: str = ""
    name: str = ""


@dataclass
class WebhookSeatSummary:
    code: str = ""
    current: float | None = None
    included: float | None = None
    remaining: float | None = None
    unlimited: bool | None = None


@dataclass
class WebhooksListResult:
    object: Literal["list"] | None = None
    data: list[Webhook] = field(default_factory=list)
    has_more: bool = False
    next_cursor: str | None = None


@dataclass
class WebhookTest:
    success: bool = False
    delivery_id: str = ""
    delivered_at: str = ""
    object: Literal["webhook_delivery"] | None = None
    livemode: bool = False


ReactivatedSubscriptionOfferApplicationPhasesItem = Union[
    ReactivatedSubscriptionOfferApplicationPhasesItemVariant1,
    ReactivatedSubscriptionOfferApplicationPhasesItemVariant2,
    ReactivatedSubscriptionOfferApplicationPhasesItemVariant3,
    ReactivatedSubscriptionOfferApplicationPhasesItemVariant4,
]


ReactivatedSubscriptionOfferApplicationAppliesTo = Union[
    ReactivatedSubscriptionOfferApplicationAppliesToVariant1,
    ReactivatedSubscriptionOfferApplicationAppliesToVariant2,
    ReactivatedSubscriptionOfferApplicationAppliesToVariant3,
]


PlanChangeVariant1OfferApplicationPhasesItem = Union[
    PlanChangeVariant1OfferApplicationPhasesItemVariant1,
    PlanChangeVariant1OfferApplicationPhasesItemVariant2,
    PlanChangeVariant1OfferApplicationPhasesItemVariant3,
    PlanChangeVariant1OfferApplicationPhasesItemVariant4,
]


PlanChangeVariant3OfferApplicationPhasesItem = Union[
    PlanChangeVariant3OfferApplicationPhasesItemVariant1,
    PlanChangeVariant3OfferApplicationPhasesItemVariant2,
    PlanChangeVariant3OfferApplicationPhasesItemVariant3,
    PlanChangeVariant3OfferApplicationPhasesItemVariant4,
]


PlanChangeVariant1OfferApplicationAppliesTo = Union[
    PlanChangeVariant1OfferApplicationAppliesToVariant1,
    PlanChangeVariant1OfferApplicationAppliesToVariant2,
    PlanChangeVariant1OfferApplicationAppliesToVariant3,
]


PlanChangeVariant3OfferApplicationAppliesTo = Union[
    PlanChangeVariant3OfferApplicationAppliesToVariant1,
    PlanChangeVariant3OfferApplicationAppliesToVariant2,
    PlanChangeVariant3OfferApplicationAppliesToVariant3,
]


PreviewChangeOfferApplicationPhasesItem = Union[
    PreviewChangeOfferApplicationPhasesItemVariant1,
    PreviewChangeOfferApplicationPhasesItemVariant2,
    PreviewChangeOfferApplicationPhasesItemVariant3,
    PreviewChangeOfferApplicationPhasesItemVariant4,
]


PreviewChangeOfferApplicationAppliesTo = Union[
    PreviewChangeOfferApplicationAppliesToVariant1,
    PreviewChangeOfferApplicationAppliesToVariant2,
    PreviewChangeOfferApplicationAppliesToVariant3,
]


SubscriptionOfferApplicationAppliesTo = Union[
    SubscriptionOfferApplicationAppliesToVariant1,
    SubscriptionOfferApplicationAppliesToVariant2,
    SubscriptionOfferApplicationAppliesToVariant3,
]


SubscriptionOfferApplicationPhase = Union[
    SubscriptionOfferApplicationPhaseVariant1,
    SubscriptionOfferApplicationPhaseVariant2,
    SubscriptionOfferApplicationPhaseVariant3,
    SubscriptionOfferApplicationPhaseVariant4,
]


FeatureAccessVariant2Consumption = Union[
    FeatureAccessVariant2ConsumptionVariant1,
    FeatureAccessVariant2ConsumptionVariant2,
    FeatureAccessVariant2ConsumptionVariant3,
]


CreateOfferParamsPhasesItem = Union[
    CreateOfferParamsPhasesItemVariant1,
    CreateOfferParamsPhasesItemVariant2,
    CreateOfferParamsPhasesItemVariant3,
    CreateOfferParamsPhasesItemVariant4,
]


UpdateOfferParamsPhasesItem = Union[
    UpdateOfferParamsPhasesItemVariant1,
    UpdateOfferParamsPhasesItemVariant2,
    UpdateOfferParamsPhasesItemVariant3,
    UpdateOfferParamsPhasesItemVariant4,
]


SubscriptionFeaturesItem = Union[
    SubscriptionFeaturesItemVariant1,
    SubscriptionFeaturesItemVariant2,
    SubscriptionFeaturesItemVariant3,
    SubscriptionFeaturesItemVariant4,
]


OfferPhasesItem = Union[
    OfferPhasesItemVariant1,
    OfferPhasesItemVariant2,
    OfferPhasesItemVariant3,
    OfferPhasesItemVariant4,
]


FeatureAccess = Union[
    FeatureAccessVariant1, FeatureAccessVariant2, FeatureAccessVariant3, FeatureAccessVariant4
]


PlanChange = Union[PlanChangeVariant1, PlanChangeVariant2, PlanChangeVariant3]


UsageCheck = Union[UsageCheckVariant1, UsageCheckVariant2, UsageCheckVariant3]


_ENUM_TYPES.update(
    {
        "BillingInterval": BillingInterval,
        "ConsumptionModel": ConsumptionModel,
        "FeatureType": FeatureType,
        "InvoiceType": InvoiceType,
        "PaymentProvider": PaymentProvider,
        "SubscriptionStatus": SubscriptionStatus,
        "Timezone": Timezone,
        "TransactionStatus": TransactionStatus,
    }
)

_DATACLASS_TYPES.update(
    {
        "ActiveAddon": ActiveAddon,
        "AddedPlanToGroup": AddedPlanToGroup,
        "Addon": Addon,
        "AddonsListActiveResult": AddonsListActiveResult,
        "AddonsListResult": AddonsListResult,
        "AddPlanFeatureParamsOverage": AddPlanFeatureParamsOverage,
        "AddPlanPriceParamsMarketPricesItem": AddPlanPriceParamsMarketPricesItem,
        "ApiKey": ApiKey,
        "ApiKeysListResult": ApiKeysListResult,
        "BalanceAdjustment": BalanceAdjustment,
        "BalanceTopup": BalanceTopup,
        "BatchCreateCustomersParamsCustomersItem": BatchCreateCustomersParamsCustomersItem,
        "BatchCreateCustomersParamsCustomersItemAddress": BatchCreateCustomersParamsCustomersItemAddress,
        "ClaimLink": ClaimLink,
        "CreateCustomerParamsAddress": CreateCustomerParamsAddress,
        "CreatedApiKey": CreatedApiKey,
        "CreatedSubscription": CreatedSubscription,
        "CreatedSubscriptionCancellation": CreatedSubscriptionCancellation,
        "CreatedSubscriptionCurrentPeriod": CreatedSubscriptionCurrentPeriod,
        "CreatedSubscriptionPlan": CreatedSubscriptionPlan,
        "CreatedSubscriptionScheduledPlanChange": CreatedSubscriptionScheduledPlanChange,
        "CreatedWebhook": CreatedWebhook,
        "CreateOfferParamsPhasesItemVariant1": CreateOfferParamsPhasesItemVariant1,
        "CreateOfferParamsPhasesItemVariant2": CreateOfferParamsPhasesItemVariant2,
        "CreateOfferParamsPhasesItemVariant3": CreateOfferParamsPhasesItemVariant3,
        "CreateOfferParamsPhasesItemVariant3AmountsItem": CreateOfferParamsPhasesItemVariant3AmountsItem,
        "CreateOfferParamsPhasesItemVariant4": CreateOfferParamsPhasesItemVariant4,
        "CreateOfferParamsPhasesItemVariant4PricesItem": CreateOfferParamsPhasesItemVariant4PricesItem,
        "CreditGrant": CreditGrant,
        "CreditPack": CreditPack,
        "CreditPackListItem": CreditPackListItem,
        "CreditPacksListResult": CreditPacksListResult,
        "Customer": Customer,
        "CustomerBatch": CustomerBatch,
        "CustomerBatchFailedItem": CustomerBatchFailedItem,
        "CustomerBatchFailedItemData": CustomerBatchFailedItemData,
        "CustomerBatchFailedItemDataAddress": CustomerBatchFailedItemDataAddress,
        "CustomerBatchSuccessfulItem": CustomerBatchSuccessfulItem,
        "CustomerCredit": CustomerCredit,
        "CustomerCreditRevocation": CustomerCreditRevocation,
        "CustomersListCreditsResult": CustomersListCreditsResult,
        "CustomersListPlanGrantsResult": CustomersListPlanGrantsResult,
        "CustomersListResult": CustomersListResult,
        "DeletedObject": DeletedObject,
        "DeletedOffer": DeletedOffer,
        "DeletedPlanRegionalPricing": DeletedPlanRegionalPricing,
        "DeletedSubscriptionAddon": DeletedSubscriptionAddon,
        "Feature": Feature,
        "FeatureAccessListResult": FeatureAccessListResult,
        "FeatureAccessVariant1": FeatureAccessVariant1,
        "FeatureAccessVariant1BaseAccess": FeatureAccessVariant1BaseAccess,
        "FeatureAccessVariant2": FeatureAccessVariant2,
        "FeatureAccessVariant2BaseAccess": FeatureAccessVariant2BaseAccess,
        "FeatureAccessVariant2ConsumptionVariant1": FeatureAccessVariant2ConsumptionVariant1,
        "FeatureAccessVariant2ConsumptionVariant1Overage": FeatureAccessVariant2ConsumptionVariant1Overage,
        "FeatureAccessVariant2ConsumptionVariant1OverageUnitPrice": FeatureAccessVariant2ConsumptionVariant1OverageUnitPrice,
        "FeatureAccessVariant2ConsumptionVariant1Period": FeatureAccessVariant2ConsumptionVariant1Period,
        "FeatureAccessVariant2ConsumptionVariant2": FeatureAccessVariant2ConsumptionVariant2,
        "FeatureAccessVariant2ConsumptionVariant2Period": FeatureAccessVariant2ConsumptionVariant2Period,
        "FeatureAccessVariant2ConsumptionVariant3": FeatureAccessVariant2ConsumptionVariant3,
        "FeatureAccessVariant2ConsumptionVariant3Period": FeatureAccessVariant2ConsumptionVariant3Period,
        "FeatureAccessVariant2ConsumptionVariant3Spent": FeatureAccessVariant2ConsumptionVariant3Spent,
        "FeatureAccessVariant2ConsumptionVariant3UnitPrice": FeatureAccessVariant2ConsumptionVariant3UnitPrice,
        "FeatureAccessVariant3": FeatureAccessVariant3,
        "FeatureAccessVariant3BaseAccess": FeatureAccessVariant3BaseAccess,
        "FeatureAccessVariant3Usage": FeatureAccessVariant3Usage,
        "FeatureAccessVariant3UsageOverage": FeatureAccessVariant3UsageOverage,
        "FeatureAccessVariant3UsageOverageUnitPrice": FeatureAccessVariant3UsageOverageUnitPrice,
        "FeatureAccessVariant3UsagePeriod": FeatureAccessVariant3UsagePeriod,
        "FeatureAccessVariant4": FeatureAccessVariant4,
        "FeatureAccessVariant4BaseAccess": FeatureAccessVariant4BaseAccess,
        "FeatureAccessVariant4Usage": FeatureAccessVariant4Usage,
        "FeatureAccessVariant4UsageOverage": FeatureAccessVariant4UsageOverage,
        "FeatureAccessVariant4UsageOverageUnitPrice": FeatureAccessVariant4UsageOverageUnitPrice,
        "FeatureAccessVariant4UsagePeriod": FeatureAccessVariant4UsagePeriod,
        "FeaturesListResult": FeaturesListResult,
        "Invoice": Invoice,
        "InvoiceDownload": InvoiceDownload,
        "InvoiceLineItemsItem": InvoiceLineItemsItem,
        "InvoiceListItem": InvoiceListItem,
        "InvoicesListResult": InvoicesListResult,
        "Market": Market,
        "MarketsListResult": MarketsListResult,
        "Offer": Offer,
        "OfferPhasesItemVariant1": OfferPhasesItemVariant1,
        "OfferPhasesItemVariant2": OfferPhasesItemVariant2,
        "OfferPhasesItemVariant3": OfferPhasesItemVariant3,
        "OfferPhasesItemVariant3AmountsItem": OfferPhasesItemVariant3AmountsItem,
        "OfferPhasesItemVariant4": OfferPhasesItemVariant4,
        "OfferPhasesItemVariant4PricesItem": OfferPhasesItemVariant4PricesItem,
        "OffersListResult": OffersListResult,
        "Payment": Payment,
        "PaymentMethodUpdateCheckout": PaymentMethodUpdateCheckout,
        "PaymentsListResult": PaymentsListResult,
        "Payout": Payout,
        "PayoutBankAccount": PayoutBankAccount,
        "Plan": Plan,
        "PlanChangeVariant1": PlanChangeVariant1,
        "PlanChangeVariant1OfferApplication": PlanChangeVariant1OfferApplication,
        "PlanChangeVariant1OfferApplicationAppliesToVariant1": PlanChangeVariant1OfferApplicationAppliesToVariant1,
        "PlanChangeVariant1OfferApplicationAppliesToVariant2": PlanChangeVariant1OfferApplicationAppliesToVariant2,
        "PlanChangeVariant1OfferApplicationAppliesToVariant3": PlanChangeVariant1OfferApplicationAppliesToVariant3,
        "PlanChangeVariant1OfferApplicationPhasesItemVariant1": PlanChangeVariant1OfferApplicationPhasesItemVariant1,
        "PlanChangeVariant1OfferApplicationPhasesItemVariant2": PlanChangeVariant1OfferApplicationPhasesItemVariant2,
        "PlanChangeVariant1OfferApplicationPhasesItemVariant3": PlanChangeVariant1OfferApplicationPhasesItemVariant3,
        "PlanChangeVariant1OfferApplicationPhasesItemVariant4": PlanChangeVariant1OfferApplicationPhasesItemVariant4,
        "PlanChangeVariant2": PlanChangeVariant2,
        "PlanChangeVariant2SeatLimitWarning": PlanChangeVariant2SeatLimitWarning,
        "PlanChangeVariant3": PlanChangeVariant3,
        "PlanChangeVariant3Billing": PlanChangeVariant3Billing,
        "PlanChangeVariant3CurrentPlan": PlanChangeVariant3CurrentPlan,
        "PlanChangeVariant3OfferApplication": PlanChangeVariant3OfferApplication,
        "PlanChangeVariant3OfferApplicationAppliesToVariant1": PlanChangeVariant3OfferApplicationAppliesToVariant1,
        "PlanChangeVariant3OfferApplicationAppliesToVariant2": PlanChangeVariant3OfferApplicationAppliesToVariant2,
        "PlanChangeVariant3OfferApplicationAppliesToVariant3": PlanChangeVariant3OfferApplicationAppliesToVariant3,
        "PlanChangeVariant3OfferApplicationPhasesItemVariant1": PlanChangeVariant3OfferApplicationPhasesItemVariant1,
        "PlanChangeVariant3OfferApplicationPhasesItemVariant2": PlanChangeVariant3OfferApplicationPhasesItemVariant2,
        "PlanChangeVariant3OfferApplicationPhasesItemVariant3": PlanChangeVariant3OfferApplicationPhasesItemVariant3,
        "PlanChangeVariant3OfferApplicationPhasesItemVariant4": PlanChangeVariant3OfferApplicationPhasesItemVariant4,
        "PlanChangeVariant3PreviousPlan": PlanChangeVariant3PreviousPlan,
        "PlanExchangeRatesItem": PlanExchangeRatesItem,
        "PlanFeature": PlanFeature,
        "PlanFeatureOverage": PlanFeatureOverage,
        "PlanFeaturesItem": PlanFeaturesItem,
        "PlanFeaturesItemOverage": PlanFeaturesItemOverage,
        "PlanFeaturesItemRegionalPricesItem": PlanFeaturesItemRegionalPricesItem,
        "PlanGrant": PlanGrant,
        "PlanGrantEventsItem": PlanGrantEventsItem,
        "PlanGroup": PlanGroup,
        "PlanGroupDetail": PlanGroupDetail,
        "PlanGroupDetailPlansItem": PlanGroupDetailPlansItem,
        "PlanGroupsListResult": PlanGroupsListResult,
        "PlanPrice": PlanPrice,
        "PlanPriceMarketPricesItem": PlanPriceMarketPricesItem,
        "PlanPricesItem": PlanPricesItem,
        "PlanPricesItemMarketPricesItem": PlanPricesItemMarketPricesItem,
        "PlanPricesItemRegionalPricesItem": PlanPricesItemRegionalPricesItem,
        "PlanRegionalPricing": PlanRegionalPricing,
        "PlanRegionalPricingOverridesItem": PlanRegionalPricingOverridesItem,
        "PlanRegionalPricingResult": PlanRegionalPricingResult,
        "PlansListResult": PlansListResult,
        "PortalAccess": PortalAccess,
        "PreviewChange": PreviewChange,
        "PreviewChangeOfferApplication": PreviewChangeOfferApplication,
        "PreviewChangeOfferApplicationAppliesToVariant1": PreviewChangeOfferApplicationAppliesToVariant1,
        "PreviewChangeOfferApplicationAppliesToVariant2": PreviewChangeOfferApplicationAppliesToVariant2,
        "PreviewChangeOfferApplicationAppliesToVariant3": PreviewChangeOfferApplicationAppliesToVariant3,
        "PreviewChangeOfferApplicationPhasesItemVariant1": PreviewChangeOfferApplicationPhasesItemVariant1,
        "PreviewChangeOfferApplicationPhasesItemVariant2": PreviewChangeOfferApplicationPhasesItemVariant2,
        "PreviewChangeOfferApplicationPhasesItemVariant3": PreviewChangeOfferApplicationPhasesItemVariant3,
        "PreviewChangeOfferApplicationPhasesItemVariant4": PreviewChangeOfferApplicationPhasesItemVariant4,
        "PromoCode": PromoCode,
        "PromoCodesListResult": PromoCodesListResult,
        "QuotaGetAllResult": QuotaGetAllResult,
        "ReactivatedSubscription": ReactivatedSubscription,
        "ReactivatedSubscriptionOfferApplication": ReactivatedSubscriptionOfferApplication,
        "ReactivatedSubscriptionOfferApplicationAppliesToVariant1": ReactivatedSubscriptionOfferApplicationAppliesToVariant1,
        "ReactivatedSubscriptionOfferApplicationAppliesToVariant2": ReactivatedSubscriptionOfferApplicationAppliesToVariant2,
        "ReactivatedSubscriptionOfferApplicationAppliesToVariant3": ReactivatedSubscriptionOfferApplicationAppliesToVariant3,
        "ReactivatedSubscriptionOfferApplicationPhasesItemVariant1": ReactivatedSubscriptionOfferApplicationPhasesItemVariant1,
        "ReactivatedSubscriptionOfferApplicationPhasesItemVariant2": ReactivatedSubscriptionOfferApplicationPhasesItemVariant2,
        "ReactivatedSubscriptionOfferApplicationPhasesItemVariant3": ReactivatedSubscriptionOfferApplicationPhasesItemVariant3,
        "ReactivatedSubscriptionOfferApplicationPhasesItemVariant4": ReactivatedSubscriptionOfferApplicationPhasesItemVariant4,
        "RecoveryLink": RecoveryLink,
        "Refund": Refund,
        "RemovedPlanFeature": RemovedPlanFeature,
        "RemovedPlanFromGroup": RemovedPlanFromGroup,
        "ReorderedPlans": ReorderedPlans,
        "SeatBalance": SeatBalance,
        "SeatBalanceCollection": SeatBalanceCollection,
        "SeatBalanceCollectionBalancesValue": SeatBalanceCollectionBalancesValue,
        "SeatEvent": SeatEvent,
        "SeatsSetAllResult": SeatsSetAllResult,
        "SentInvoice": SentInvoice,
        "SetPlanRegionalPricingParamsFeaturesItem": SetPlanRegionalPricingParamsFeaturesItem,
        "SetPlanRegionalPricingParamsPricesItem": SetPlanRegionalPricingParamsPricesItem,
        "Subscription": Subscription,
        "SubscriptionAddon": SubscriptionAddon,
        "SubscriptionBalance": SubscriptionBalance,
        "SubscriptionCancellation": SubscriptionCancellation,
        "SubscriptionCredits": SubscriptionCredits,
        "SubscriptionCurrentPeriod": SubscriptionCurrentPeriod,
        "SubscriptionFeaturesItemVariant1": SubscriptionFeaturesItemVariant1,
        "SubscriptionFeaturesItemVariant1BaseAccess": SubscriptionFeaturesItemVariant1BaseAccess,
        "SubscriptionFeaturesItemVariant2": SubscriptionFeaturesItemVariant2,
        "SubscriptionFeaturesItemVariant2BaseAccess": SubscriptionFeaturesItemVariant2BaseAccess,
        "SubscriptionFeaturesItemVariant2Usage": SubscriptionFeaturesItemVariant2Usage,
        "SubscriptionFeaturesItemVariant3": SubscriptionFeaturesItemVariant3,
        "SubscriptionFeaturesItemVariant3BaseAccess": SubscriptionFeaturesItemVariant3BaseAccess,
        "SubscriptionFeaturesItemVariant3Usage": SubscriptionFeaturesItemVariant3Usage,
        "SubscriptionFeaturesItemVariant4": SubscriptionFeaturesItemVariant4,
        "SubscriptionFeaturesItemVariant4BaseAccess": SubscriptionFeaturesItemVariant4BaseAccess,
        "SubscriptionFeaturesItemVariant4Usage": SubscriptionFeaturesItemVariant4Usage,
        "SubscriptionOfferApplication": SubscriptionOfferApplication,
        "SubscriptionOfferApplicationAppliesToVariant1": SubscriptionOfferApplicationAppliesToVariant1,
        "SubscriptionOfferApplicationAppliesToVariant2": SubscriptionOfferApplicationAppliesToVariant2,
        "SubscriptionOfferApplicationAppliesToVariant3": SubscriptionOfferApplicationAppliesToVariant3,
        "SubscriptionOfferApplicationPhaseVariant1": SubscriptionOfferApplicationPhaseVariant1,
        "SubscriptionOfferApplicationPhaseVariant2": SubscriptionOfferApplicationPhaseVariant2,
        "SubscriptionOfferApplicationPhaseVariant3": SubscriptionOfferApplicationPhaseVariant3,
        "SubscriptionOfferApplicationPhaseVariant4": SubscriptionOfferApplicationPhaseVariant4,
        "SubscriptionPlan": SubscriptionPlan,
        "SubscriptionPlanGrant": SubscriptionPlanGrant,
        "SubscriptionPlanGrantPlan": SubscriptionPlanGrantPlan,
        "SubscriptionScheduledPlanChange": SubscriptionScheduledPlanChange,
        "SubscriptionsListResult": SubscriptionsListResult,
        "SubscriptionSummary": SubscriptionSummary,
        "SubscriptionSummaryCancellation": SubscriptionSummaryCancellation,
        "SubscriptionSummaryCurrentPeriod": SubscriptionSummaryCurrentPeriod,
        "SubscriptionSummaryPlan": SubscriptionSummaryPlan,
        "SubscriptionSummaryScheduledPlanChange": SubscriptionSummaryScheduledPlanChange,
        "TestClock": TestClock,
        "TestClockLatestRun": TestClockLatestRun,
        "TestClockLatestRunItemsItem": TestClockLatestRunItemsItem,
        "TestClockRun": TestClockRun,
        "TestClockRunItemsItem": TestClockRunItemsItem,
        "TrackUsageParamsPropertiesItem": TrackUsageParamsPropertiesItem,
        "Transaction": Transaction,
        "TransactionListItem": TransactionListItem,
        "TransactionRetry": TransactionRetry,
        "TransactionsListResult": TransactionsListResult,
        "UpdateCustomerParamsAddress": UpdateCustomerParamsAddress,
        "UpdateOfferParamsPhasesItemVariant1": UpdateOfferParamsPhasesItemVariant1,
        "UpdateOfferParamsPhasesItemVariant2": UpdateOfferParamsPhasesItemVariant2,
        "UpdateOfferParamsPhasesItemVariant3": UpdateOfferParamsPhasesItemVariant3,
        "UpdateOfferParamsPhasesItemVariant3AmountsItem": UpdateOfferParamsPhasesItemVariant3AmountsItem,
        "UpdateOfferParamsPhasesItemVariant4": UpdateOfferParamsPhasesItemVariant4,
        "UpdateOfferParamsPhasesItemVariant4PricesItem": UpdateOfferParamsPhasesItemVariant4PricesItem,
        "UpdatePlanFeatureParamsOverage": UpdatePlanFeatureParamsOverage,
        "UpdatePlanPriceParamsMarketPricesItem": UpdatePlanPriceParamsMarketPricesItem,
        "UpsertRegionalPricesParamsOverridesItem": UpsertRegionalPricesParamsOverridesItem,
        "UsageAdjustment": UsageAdjustment,
        "UsageCheckVariant1": UsageCheckVariant1,
        "UsageCheckVariant2": UsageCheckVariant2,
        "UsageCheckVariant3": UsageCheckVariant3,
        "UsageEvent": UsageEvent,
        "UsageEventConsumption": UsageEventConsumption,
        "UsageEventPropertiesItem": UsageEventPropertiesItem,
        "UsageQuota": UsageQuota,
        "UsageQuotaEvent": UsageQuotaEvent,
        "Webhook": Webhook,
        "WebhookAddonRef": WebhookAddonRef,
        "WebhookBalance": WebhookBalance,
        "WebhookBankRef": WebhookBankRef,
        "WebhookCardInfo": WebhookCardInfo,
        "WebhookCreditsBalance": WebhookCreditsBalance,
        "WebhookPlanGrantTimelineEvent": WebhookPlanGrantTimelineEvent,
        "WebhookPlanRef": WebhookPlanRef,
        "WebhookSeatSummary": WebhookSeatSummary,
        "WebhooksListResult": WebhooksListResult,
        "WebhookTest": WebhookTest,
    }
)

_UNION_TYPES.update(
    {
        "ReactivatedSubscriptionOfferApplicationPhasesItem": (
            "type",
            {
                "free_trial": ReactivatedSubscriptionOfferApplicationPhasesItemVariant1,
                "percentage": ReactivatedSubscriptionOfferApplicationPhasesItemVariant2,
                "amount_off": ReactivatedSubscriptionOfferApplicationPhasesItemVariant3,
                "fixed_price": ReactivatedSubscriptionOfferApplicationPhasesItemVariant4,
            },
            [],
        ),
        "ReactivatedSubscriptionOfferApplicationAppliesTo": (
            "type",
            {
                "plan_price": ReactivatedSubscriptionOfferApplicationAppliesToVariant1,
                "addon": ReactivatedSubscriptionOfferApplicationAppliesToVariant2,
                "credit_pack": ReactivatedSubscriptionOfferApplicationAppliesToVariant3,
            },
            [],
        ),
        "PlanChangeVariant1OfferApplicationPhasesItem": (
            "type",
            {
                "free_trial": PlanChangeVariant1OfferApplicationPhasesItemVariant1,
                "percentage": PlanChangeVariant1OfferApplicationPhasesItemVariant2,
                "amount_off": PlanChangeVariant1OfferApplicationPhasesItemVariant3,
                "fixed_price": PlanChangeVariant1OfferApplicationPhasesItemVariant4,
            },
            [],
        ),
        "PlanChangeVariant3OfferApplicationPhasesItem": (
            "type",
            {
                "free_trial": PlanChangeVariant3OfferApplicationPhasesItemVariant1,
                "percentage": PlanChangeVariant3OfferApplicationPhasesItemVariant2,
                "amount_off": PlanChangeVariant3OfferApplicationPhasesItemVariant3,
                "fixed_price": PlanChangeVariant3OfferApplicationPhasesItemVariant4,
            },
            [],
        ),
        "PlanChangeVariant1OfferApplicationAppliesTo": (
            "type",
            {
                "plan_price": PlanChangeVariant1OfferApplicationAppliesToVariant1,
                "addon": PlanChangeVariant1OfferApplicationAppliesToVariant2,
                "credit_pack": PlanChangeVariant1OfferApplicationAppliesToVariant3,
            },
            [],
        ),
        "PlanChangeVariant3OfferApplicationAppliesTo": (
            "type",
            {
                "plan_price": PlanChangeVariant3OfferApplicationAppliesToVariant1,
                "addon": PlanChangeVariant3OfferApplicationAppliesToVariant2,
                "credit_pack": PlanChangeVariant3OfferApplicationAppliesToVariant3,
            },
            [],
        ),
        "PreviewChangeOfferApplicationPhasesItem": (
            "type",
            {
                "free_trial": PreviewChangeOfferApplicationPhasesItemVariant1,
                "percentage": PreviewChangeOfferApplicationPhasesItemVariant2,
                "amount_off": PreviewChangeOfferApplicationPhasesItemVariant3,
                "fixed_price": PreviewChangeOfferApplicationPhasesItemVariant4,
            },
            [],
        ),
        "PreviewChangeOfferApplicationAppliesTo": (
            "type",
            {
                "plan_price": PreviewChangeOfferApplicationAppliesToVariant1,
                "addon": PreviewChangeOfferApplicationAppliesToVariant2,
                "credit_pack": PreviewChangeOfferApplicationAppliesToVariant3,
            },
            [],
        ),
        "SubscriptionOfferApplicationAppliesTo": (
            "type",
            {
                "plan_price": SubscriptionOfferApplicationAppliesToVariant1,
                "addon": SubscriptionOfferApplicationAppliesToVariant2,
                "credit_pack": SubscriptionOfferApplicationAppliesToVariant3,
            },
            [],
        ),
        "SubscriptionOfferApplicationPhase": (
            "type",
            {
                "free_trial": SubscriptionOfferApplicationPhaseVariant1,
                "percentage": SubscriptionOfferApplicationPhaseVariant2,
                "amount_off": SubscriptionOfferApplicationPhaseVariant3,
                "fixed_price": SubscriptionOfferApplicationPhaseVariant4,
            },
            [],
        ),
        "FeatureAccessVariant2Consumption": (
            "model",
            {
                "metered": FeatureAccessVariant2ConsumptionVariant1,
                "credits": FeatureAccessVariant2ConsumptionVariant2,
                "balance": FeatureAccessVariant2ConsumptionVariant3,
            },
            [],
        ),
        "CreateOfferParamsPhasesItem": (
            "type",
            {
                "free_trial": CreateOfferParamsPhasesItemVariant1,
                "percentage": CreateOfferParamsPhasesItemVariant2,
                "amount_off": CreateOfferParamsPhasesItemVariant3,
                "fixed_price": CreateOfferParamsPhasesItemVariant4,
            },
            [],
        ),
        "UpdateOfferParamsPhasesItem": (
            "type",
            {
                "free_trial": UpdateOfferParamsPhasesItemVariant1,
                "percentage": UpdateOfferParamsPhasesItemVariant2,
                "amount_off": UpdateOfferParamsPhasesItemVariant3,
                "fixed_price": UpdateOfferParamsPhasesItemVariant4,
            },
            [],
        ),
        "SubscriptionFeaturesItem": (
            "type",
            {
                "boolean": SubscriptionFeaturesItemVariant1,
                "usage": SubscriptionFeaturesItemVariant2,
                "seats": SubscriptionFeaturesItemVariant3,
                "quota": SubscriptionFeaturesItemVariant4,
            },
            [],
        ),
        "OfferPhasesItem": (
            "type",
            {
                "free_trial": OfferPhasesItemVariant1,
                "percentage": OfferPhasesItemVariant2,
                "amount_off": OfferPhasesItemVariant3,
                "fixed_price": OfferPhasesItemVariant4,
            },
            [],
        ),
        "FeatureAccess": (
            "type",
            {
                "boolean": FeatureAccessVariant1,
                "usage": FeatureAccessVariant2,
                "seats": FeatureAccessVariant3,
                "quota": FeatureAccessVariant4,
            },
            [],
        ),
        "PlanChange": (
            "outcome",
            {
                "requires_checkout": PlanChangeVariant1,
                "scheduled": PlanChangeVariant2,
                "completed": PlanChangeVariant3,
            },
            [],
        ),
        "UsageCheck": (
            "consumptionModel",
            {
                "metered": UsageCheckVariant1,
                "credits": UsageCheckVariant2,
                "balance": UsageCheckVariant3,
            },
            [],
        ),
    }
)
