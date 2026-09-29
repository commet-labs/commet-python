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
    RESUME = "resume"


class PaymentMethod(str, Enum):
    CARD = "card"
    OXXO = "oxxo"
    MERCADO_PAGO = "mercado_pago"


class PaymentProvider(str, Enum):
    STRIPE = "stripe"
    COMMET = "commet"
    DLOCAL = "dlocal"


class SubPaymentMethod(str, Enum):
    CREDIT_CARD = "credit_card"
    DEBIT_CARD = "debit_card"
    PREPAID_CARD = "prepaid_card"
    BANK_TRANSFER = "bank_transfer"
    ACCOUNT_MONEY = "account_money"


class SubscriptionStatus(str, Enum):
    DRAFT = "draft"
    PENDING_PAYMENT = "pending_payment"
    TRIALING = "trialing"
    ACTIVE = "active"
    PAST_DUE = "past_due"
    PAUSED = "paused"
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
    slug: str = field(default="", metadata={"wire_name": "slug", "required": True})
    name: str = field(default="", metadata={"wire_name": "name", "required": True})
    base_price: int = field(default=0, metadata={"wire_name": "basePrice", "required": True})
    feature_code: str = field(default="", metadata={"wire_name": "featureCode", "required": True})
    feature_name: str = field(default="", metadata={"wire_name": "featureName", "required": True})
    feature_type: FeatureType | None = field(
        default=None, metadata={"wire_name": "featureType", "required": True}
    )
    consumption_model: Literal["boolean", "metered", "credits", "balance"] | None = field(
        default=None, metadata={"wire_name": "consumptionModel", "required": True}
    )
    activated_at: str = field(default="", metadata={"wire_name": "activatedAt", "required": True})
    object: Literal["subscription_addon"] | None = field(
        default=None, metadata={"wire_name": "object", "required": True}
    )
    livemode: bool = field(default=False, metadata={"wire_name": "livemode", "required": True})


@dataclass
class AddedPlanToGroup:
    success: bool = field(default=False, metadata={"wire_name": "success", "required": True})
    object: Literal["plan_group_membership"] | None = field(
        default=None, metadata={"wire_name": "object", "required": True}
    )
    livemode: bool = field(default=False, metadata={"wire_name": "livemode", "required": True})


@dataclass
class Addon:
    id: str = field(default="", metadata={"wire_name": "id", "required": True})
    name: str = field(default="", metadata={"wire_name": "name", "required": True})
    slug: str = field(default="", metadata={"wire_name": "slug", "required": True})
    description: str | None = field(
        default=None, metadata={"wire_name": "description", "required": True}
    )
    base_price: int = field(default=0, metadata={"wire_name": "basePrice", "required": True})
    feature_code: str = field(default="", metadata={"wire_name": "featureCode", "required": True})
    feature_name: str = field(default="", metadata={"wire_name": "featureName", "required": True})
    created_at: str = field(default="", metadata={"wire_name": "createdAt", "required": True})
    updated_at: str = field(default="", metadata={"wire_name": "updatedAt", "required": True})
    consumption_model: Literal["boolean", "metered", "credits", "balance"] | None = field(
        default=None, metadata={"wire_name": "consumptionModel", "required": True}
    )
    included_units: int | None = field(
        default=None, metadata={"wire_name": "includedUnits", "required": True}
    )
    overage_rate: int | None = field(
        default=None, metadata={"wire_name": "overageRate", "required": True}
    )
    credit_cost: int | None = field(
        default=None, metadata={"wire_name": "creditCost", "required": True}
    )
    object: Literal["addon"] | None = field(
        default=None, metadata={"wire_name": "object", "required": True}
    )
    livemode: bool = field(default=False, metadata={"wire_name": "livemode", "required": True})


@dataclass
class AddonsListActiveResult:
    object: Literal["list"] | None = field(
        default=None, metadata={"wire_name": "object", "required": True}
    )
    data: list[ActiveAddon] = field(
        default_factory=list, metadata={"wire_name": "data", "required": True}
    )
    has_more: bool = field(default=False, metadata={"wire_name": "hasMore", "required": True})
    next_cursor: str | None = field(
        default=None, metadata={"wire_name": "nextCursor", "required": False}
    )


@dataclass
class AddonsListResult:
    object: Literal["list"] | None = field(
        default=None, metadata={"wire_name": "object", "required": True}
    )
    data: list[Addon] = field(
        default_factory=list, metadata={"wire_name": "data", "required": True}
    )
    has_more: bool = field(default=False, metadata={"wire_name": "hasMore", "required": True})
    next_cursor: str | None = field(
        default=None, metadata={"wire_name": "nextCursor", "required": False}
    )


@dataclass
class AddPlanFeatureParamsOverage:
    enabled: bool | None = field(default=None, metadata={"wire_name": "enabled", "required": False})
    unit_price: int | None = field(
        default=None, metadata={"wire_name": "unitPrice", "required": False}
    )


@dataclass
class AddPlanPriceParamsMarketPricesItem:
    market_group_id: str = field(
        default="", metadata={"wire_name": "marketGroupId", "required": True}
    )
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
            "gbp",
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
    ) = field(default=None, metadata={"wire_name": "currency", "required": True})
    price: int = field(default=0, metadata={"wire_name": "price", "required": True})


@dataclass
class ApiKey:
    id: str = field(default="", metadata={"wire_name": "id", "required": True})
    name: str = field(default="", metadata={"wire_name": "name", "required": True})
    prefix: str = field(default="", metadata={"wire_name": "prefix", "required": True})
    expires_at: str | None = field(
        default=None, metadata={"wire_name": "expiresAt", "required": True}
    )
    last_used_at: str | None = field(
        default=None, metadata={"wire_name": "lastUsedAt", "required": True}
    )
    created_at: str = field(default="", metadata={"wire_name": "createdAt", "required": True})
    object: Literal["api_key"] | None = field(
        default=None, metadata={"wire_name": "object", "required": True}
    )
    livemode: bool = field(default=False, metadata={"wire_name": "livemode", "required": True})


@dataclass
class ApiKeysListResult:
    object: Literal["list"] | None = field(
        default=None, metadata={"wire_name": "object", "required": True}
    )
    data: list[ApiKey] = field(
        default_factory=list, metadata={"wire_name": "data", "required": True}
    )
    has_more: bool = field(default=False, metadata={"wire_name": "hasMore", "required": True})
    next_cursor: str | None = field(
        default=None, metadata={"wire_name": "nextCursor", "required": False}
    )


@dataclass
class BalanceAdjustment:
    amount: int = field(default=0, metadata={"wire_name": "amount", "required": True})
    new_balance: int = field(default=0, metadata={"wire_name": "newBalance", "required": True})
    reason: str | None = field(default=None, metadata={"wire_name": "reason", "required": True})
    object: Literal["balance_transaction"] | None = field(
        default=None, metadata={"wire_name": "object", "required": True}
    )
    livemode: bool = field(default=False, metadata={"wire_name": "livemode", "required": True})


@dataclass
class BalanceTopup:
    amount: int = field(default=0, metadata={"wire_name": "amount", "required": True})
    object: Literal["balance_topup"] | None = field(
        default=None, metadata={"wire_name": "object", "required": True}
    )
    livemode: bool = field(default=False, metadata={"wire_name": "livemode", "required": True})


@dataclass
class BatchCreateCustomersParamsCustomersItem:
    email: str = field(default="", metadata={"wire_name": "email", "required": True})
    id: str | None = field(default=None, metadata={"wire_name": "id", "required": False})
    external_id: str | None = field(
        default=None, metadata={"wire_name": "externalId", "required": False}
    )
    full_name: str | None = field(
        default=None, metadata={"wire_name": "fullName", "required": False}
    )
    tax_document: str | None = field(
        default=None, metadata={"wire_name": "taxDocument", "required": False}
    )
    timezone: Timezone | None = field(
        default=None, metadata={"wire_name": "timezone", "required": False}
    )
    metadata: dict[str, Any] | None = field(
        default=None, metadata={"wire_name": "metadata", "required": False}
    )
    address: BatchCreateCustomersParamsCustomersItemAddress | None = field(
        default=None, metadata={"wire_name": "address", "required": False}
    )


@dataclass
class BatchCreateCustomersParamsCustomersItemAddress:
    line1: str = field(default="", metadata={"wire_name": "line1", "required": True})
    line2: str | None = field(default=None, metadata={"wire_name": "line2", "required": False})
    city: str = field(default="", metadata={"wire_name": "city", "required": True})
    state: str | None = field(default=None, metadata={"wire_name": "state", "required": False})
    postal_code: str = field(default="", metadata={"wire_name": "postalCode", "required": True})
    country: str = field(default="", metadata={"wire_name": "country", "required": True})
    region: str | None = field(default=None, metadata={"wire_name": "region", "required": False})


@dataclass
class ClaimLink:
    url: str = field(default="", metadata={"wire_name": "url", "required": True})
    expires_at: str = field(default="", metadata={"wire_name": "expiresAt", "required": True})
    object: Literal["claim_link"] | None = field(
        default=None, metadata={"wire_name": "object", "required": True}
    )
    livemode: bool = field(default=False, metadata={"wire_name": "livemode", "required": True})


@dataclass
class CreateApiKeyParamsPermissions:
    customer: list[Literal["read", "write"]] | None = field(
        default=None, metadata={"wire_name": "customer", "required": False}
    )
    subscription: list[Literal["read", "write"]] | None = field(
        default=None, metadata={"wire_name": "subscription", "required": False}
    )
    invoice: list[Literal["read", "write"]] | None = field(
        default=None, metadata={"wire_name": "invoice", "required": False}
    )
    usage: list[Literal["read", "write"]] | None = field(
        default=None, metadata={"wire_name": "usage", "required": False}
    )
    seat: list[Literal["read", "write"]] | None = field(
        default=None, metadata={"wire_name": "seat", "required": False}
    )
    plan: list[Literal["read", "write"]] | None = field(
        default=None, metadata={"wire_name": "plan", "required": False}
    )
    plan_group: list[Literal["read", "write"]] | None = field(
        default=None, metadata={"wire_name": "plan_group", "required": False}
    )
    feature: list[Literal["read", "write"]] | None = field(
        default=None, metadata={"wire_name": "feature", "required": False}
    )
    addon: list[Literal["read", "write"]] | None = field(
        default=None, metadata={"wire_name": "addon", "required": False}
    )
    credit_pack: list[Literal["read", "write"]] | None = field(
        default=None, metadata={"wire_name": "credit_pack", "required": False}
    )
    offer: list[Literal["read", "write"]] | None = field(
        default=None, metadata={"wire_name": "offer", "required": False}
    )
    promo_code: list[Literal["read", "write"]] | None = field(
        default=None, metadata={"wire_name": "promo_code", "required": False}
    )
    market_group: list[Literal["read", "write"]] | None = field(
        default=None, metadata={"wire_name": "market_group", "required": False}
    )
    payment: list[Literal["read", "write"]] | None = field(
        default=None, metadata={"wire_name": "payment", "required": False}
    )
    transaction: list[Literal["read", "write"]] | None = field(
        default=None, metadata={"wire_name": "transaction", "required": False}
    )
    payout: list[Literal["read", "write"]] | None = field(
        default=None, metadata={"wire_name": "payout", "required": False}
    )
    test_clock: list[Literal["read", "write"]] | None = field(
        default=None, metadata={"wire_name": "test_clock", "required": False}
    )
    organization: list[Literal["read", "write"]] | None = field(
        default=None, metadata={"wire_name": "organization", "required": False}
    )
    api_key: list[Literal["read", "write"]] | None = field(
        default=None, metadata={"wire_name": "api_key", "required": False}
    )


@dataclass
class CreateCustomerParamsAddress:
    line1: str = field(default="", metadata={"wire_name": "line1", "required": True})
    line2: str | None = field(default=None, metadata={"wire_name": "line2", "required": False})
    city: str = field(default="", metadata={"wire_name": "city", "required": True})
    state: str | None = field(default=None, metadata={"wire_name": "state", "required": False})
    postal_code: str = field(default="", metadata={"wire_name": "postalCode", "required": True})
    country: str = field(default="", metadata={"wire_name": "country", "required": True})
    region: str | None = field(default=None, metadata={"wire_name": "region", "required": False})


@dataclass
class CreatedApiKey:
    id: str = field(default="", metadata={"wire_name": "id", "required": True})
    name: str = field(default="", metadata={"wire_name": "name", "required": True})
    api_key: str = field(default="", metadata={"wire_name": "apiKey", "required": True})
    prefix: str = field(default="", metadata={"wire_name": "prefix", "required": True})
    expires_at: str = field(default="", metadata={"wire_name": "expiresAt", "required": True})
    created_at: str = field(default="", metadata={"wire_name": "createdAt", "required": True})
    object: Literal["api_key"] | None = field(
        default=None, metadata={"wire_name": "object", "required": True}
    )
    livemode: bool = field(default=False, metadata={"wire_name": "livemode", "required": True})


@dataclass
class CreatedSubscription:
    id: str = field(default="", metadata={"wire_name": "id", "required": True})
    customer_id: str = field(default="", metadata={"wire_name": "customerId", "required": True})
    plan: CreatedSubscriptionPlan | None = field(
        default=None, metadata={"wire_name": "plan", "required": True}
    )
    name: str = field(default="", metadata={"wire_name": "name", "required": True})
    description: str | None = field(
        default=None, metadata={"wire_name": "description", "required": True}
    )
    status: SubscriptionStatus | None = field(
        default=None, metadata={"wire_name": "status", "required": True}
    )
    billing_interval: BillingInterval | None = field(
        default=None, metadata={"wire_name": "billingInterval", "required": True}
    )
    trial_ends_at: str | None = field(
        default=None, metadata={"wire_name": "trialEndsAt", "required": True}
    )
    current_period: CreatedSubscriptionCurrentPeriod | None = field(
        default=None, metadata={"wire_name": "currentPeriod", "required": True}
    )
    cancellation: CreatedSubscriptionCancellation | None = field(
        default=None, metadata={"wire_name": "cancellation", "required": True}
    )
    cancel_at_period_end: bool = field(
        default=False, metadata={"wire_name": "cancelAtPeriodEnd", "required": True}
    )
    scheduled_plan_change: CreatedSubscriptionScheduledPlanChange | None = field(
        default=None, metadata={"wire_name": "scheduledPlanChange", "required": True}
    )
    start_date: str = field(default="", metadata={"wire_name": "startDate", "required": True})
    end_date: str | None = field(default=None, metadata={"wire_name": "endDate", "required": True})
    billing_day_of_month: int | None = field(
        default=None, metadata={"wire_name": "billingDayOfMonth", "required": True}
    )
    next_billing_date: str | None = field(
        default=None, metadata={"wire_name": "nextBillingDate", "required": True}
    )
    checkout_url: str | None = field(
        default=None, metadata={"wire_name": "checkoutUrl", "required": True}
    )
    created_at: str = field(default="", metadata={"wire_name": "createdAt", "required": True})
    updated_at: str = field(default="", metadata={"wire_name": "updatedAt", "required": True})
    offer_applications: list[SubscriptionOfferApplication] = field(
        default_factory=list, metadata={"wire_name": "offerApplications", "required": True}
    )
    pause: CreatedSubscriptionPause | None = field(
        default=None, metadata={"wire_name": "pause", "required": True}
    )
    checkout_provider: PaymentProvider | None = field(
        default=None, metadata={"wire_name": "checkoutProvider", "required": True}
    )
    price_id: str | None = field(default=None, metadata={"wire_name": "priceId", "required": True})
    object: Literal["subscription"] | None = field(
        default=None, metadata={"wire_name": "object", "required": True}
    )
    livemode: bool = field(default=False, metadata={"wire_name": "livemode", "required": True})


@dataclass
class CreatedSubscriptionCancellation:
    scheduled_at: str = field(default="", metadata={"wire_name": "scheduledAt", "required": True})
    reason: str | None = field(default=None, metadata={"wire_name": "reason", "required": True})
    effective_at: str = field(default="", metadata={"wire_name": "effectiveAt", "required": True})


@dataclass
class CreatedSubscriptionCurrentPeriod:
    start: str = field(default="", metadata={"wire_name": "start", "required": True})
    end: str = field(default="", metadata={"wire_name": "end", "required": True})
    days_remaining: float = field(
        default=0.0, metadata={"wire_name": "daysRemaining", "required": True}
    )


@dataclass
class CreatedSubscriptionPauseVariant1:
    status: Literal["scheduled"] | None = field(
        default=None, metadata={"wire_name": "status", "required": True}
    )
    mode: Literal["period_end"] | None = field(
        default=None, metadata={"wire_name": "mode", "required": True}
    )
    requested_at: str = field(default="", metadata={"wire_name": "requestedAt", "required": True})
    effective_at: str = field(default="", metadata={"wire_name": "effectiveAt", "required": True})
    resume_at: str | None = field(
        default=None, metadata={"wire_name": "resumeAt", "required": True}
    )


@dataclass
class CreatedSubscriptionPauseVariant2:
    status: Literal["active"] | None = field(
        default=None, metadata={"wire_name": "status", "required": True}
    )
    mode: Literal["immediate", "period_end"] | None = field(
        default=None, metadata={"wire_name": "mode", "required": True}
    )
    requested_at: str = field(default="", metadata={"wire_name": "requestedAt", "required": True})
    effective_at: str = field(default="", metadata={"wire_name": "effectiveAt", "required": True})
    resume_at: str | None = field(
        default=None, metadata={"wire_name": "resumeAt", "required": True}
    )


@dataclass
class CreatedSubscriptionPlan:
    id: str = field(default="", metadata={"wire_name": "id", "required": True})
    name: str = field(default="", metadata={"wire_name": "name", "required": True})


@dataclass
class CreatedSubscriptionScheduledPlanChange:
    change_type: Literal["plan_downgrade", "interval_change"] | None = field(
        default=None, metadata={"wire_name": "changeType", "required": True}
    )
    new_plan_id: str | None = field(
        default=None, metadata={"wire_name": "newPlanId", "required": True}
    )
    new_plan_name: str | None = field(
        default=None, metadata={"wire_name": "newPlanName", "required": True}
    )
    new_billing_interval: str | None = field(
        default=None, metadata={"wire_name": "newBillingInterval", "required": True}
    )
    scheduled_for: str = field(default="", metadata={"wire_name": "scheduledFor", "required": True})


@dataclass
class CreatedWebhook:
    id: str = field(default="", metadata={"wire_name": "id", "required": True})
    url: str = field(default="", metadata={"wire_name": "url", "required": True})
    events: list[str] = field(
        default_factory=list, metadata={"wire_name": "events", "required": True}
    )
    description: str | None = field(
        default=None, metadata={"wire_name": "description", "required": True}
    )
    is_active: bool = field(default=False, metadata={"wire_name": "isActive", "required": True})
    api_version: str | None = field(
        default=None, metadata={"wire_name": "apiVersion", "required": True}
    )
    created_at: str = field(default="", metadata={"wire_name": "createdAt", "required": True})
    secret_key: str = field(default="", metadata={"wire_name": "secretKey", "required": True})
    object: Literal["webhook"] | None = field(
        default=None, metadata={"wire_name": "object", "required": True}
    )
    livemode: bool = field(default=False, metadata={"wire_name": "livemode", "required": True})


@dataclass
class CreateOfferParamsPhasesItemVariant1:
    type: Literal["free_trial"] | None = field(
        default=None, metadata={"wire_name": "type", "required": True}
    )
    duration_days: int = field(default=0, metadata={"wire_name": "durationDays", "required": True})


@dataclass
class CreateOfferParamsPhasesItemVariant2:
    type: Literal["percentage"] | None = field(
        default=None, metadata={"wire_name": "type", "required": True}
    )
    duration_cycles: int | None = field(
        default=None, metadata={"wire_name": "durationCycles", "required": True}
    )
    duration_interval: Literal["weekly", "monthly", "quarterly", "yearly"] | None = field(
        default=None, metadata={"wire_name": "durationInterval", "required": False}
    )
    percentage: int = field(default=0, metadata={"wire_name": "percentage", "required": True})


@dataclass
class CreateOfferParamsPhasesItemVariant3:
    type: Literal["amount_off"] | None = field(
        default=None, metadata={"wire_name": "type", "required": True}
    )
    duration_cycles: int | None = field(
        default=None, metadata={"wire_name": "durationCycles", "required": True}
    )
    duration_interval: Literal["weekly", "monthly", "quarterly", "yearly"] | None = field(
        default=None, metadata={"wire_name": "durationInterval", "required": False}
    )
    amounts: list[CreateOfferParamsPhasesItemVariant3AmountsItem] = field(
        default_factory=list, metadata={"wire_name": "amounts", "required": True}
    )


@dataclass
class CreateOfferParamsPhasesItemVariant3AmountsItem:
    currency: str = field(default="", metadata={"wire_name": "currency", "required": True})
    amount: int = field(default=0, metadata={"wire_name": "amount", "required": True})


@dataclass
class CreateOfferParamsPhasesItemVariant4:
    type: Literal["fixed_price"] | None = field(
        default=None, metadata={"wire_name": "type", "required": True}
    )
    duration_cycles: int | None = field(
        default=None, metadata={"wire_name": "durationCycles", "required": True}
    )
    duration_interval: Literal["weekly", "monthly", "quarterly", "yearly"] | None = field(
        default=None, metadata={"wire_name": "durationInterval", "required": False}
    )
    prices: list[CreateOfferParamsPhasesItemVariant4PricesItem] = field(
        default_factory=list, metadata={"wire_name": "prices", "required": True}
    )


@dataclass
class CreateOfferParamsPhasesItemVariant4PricesItem:
    currency: str = field(default="", metadata={"wire_name": "currency", "required": True})
    amount: int = field(default=0, metadata={"wire_name": "amount", "required": True})


@dataclass
class CreditGrant:
    credits: int = field(default=0, metadata={"wire_name": "credits", "required": True})
    object: Literal["credit_grant"] | None = field(
        default=None, metadata={"wire_name": "object", "required": True}
    )
    livemode: bool = field(default=False, metadata={"wire_name": "livemode", "required": True})


@dataclass
class CreditPack:
    id: str = field(default="", metadata={"wire_name": "id", "required": True})
    name: str = field(default="", metadata={"wire_name": "name", "required": True})
    description: str | None = field(
        default=None, metadata={"wire_name": "description", "required": True}
    )
    credits: int = field(default=0, metadata={"wire_name": "credits", "required": True})
    price: int = field(default=0, metadata={"wire_name": "price", "required": True})
    is_active: bool = field(default=False, metadata={"wire_name": "isActive", "required": True})
    created_at: str = field(default="", metadata={"wire_name": "createdAt", "required": True})
    updated_at: str = field(default="", metadata={"wire_name": "updatedAt", "required": True})
    object: Literal["credit_pack"] | None = field(
        default=None, metadata={"wire_name": "object", "required": True}
    )
    livemode: bool = field(default=False, metadata={"wire_name": "livemode", "required": True})


@dataclass
class CreditPackListItem:
    id: str = field(default="", metadata={"wire_name": "id", "required": True})
    name: str = field(default="", metadata={"wire_name": "name", "required": True})
    description: str | None = field(
        default=None, metadata={"wire_name": "description", "required": True}
    )
    credits: int = field(default=0, metadata={"wire_name": "credits", "required": True})
    price: int = field(default=0, metadata={"wire_name": "price", "required": True})
    currency: str = field(default="", metadata={"wire_name": "currency", "required": True})
    object: Literal["credit_pack"] | None = field(
        default=None, metadata={"wire_name": "object", "required": True}
    )
    livemode: bool = field(default=False, metadata={"wire_name": "livemode", "required": True})


@dataclass
class CreditPacksListResult:
    object: Literal["list"] | None = field(
        default=None, metadata={"wire_name": "object", "required": True}
    )
    data: list[CreditPackListItem] = field(
        default_factory=list, metadata={"wire_name": "data", "required": True}
    )
    has_more: bool = field(default=False, metadata={"wire_name": "hasMore", "required": True})
    next_cursor: str | None = field(
        default=None, metadata={"wire_name": "nextCursor", "required": False}
    )


@dataclass
class Customer:
    id: str = field(default="", metadata={"wire_name": "id", "required": True})
    external_id: str | None = field(
        default=None, metadata={"wire_name": "externalId", "required": True}
    )
    full_name: str | None = field(
        default=None, metadata={"wire_name": "fullName", "required": True}
    )
    email: str = field(default="", metadata={"wire_name": "email", "required": True})
    tax_document: str | None = field(
        default=None, metadata={"wire_name": "taxDocument", "required": True}
    )
    document_type: str | None = field(
        default=None, metadata={"wire_name": "documentType", "required": True}
    )
    timezone: str | None = field(default=None, metadata={"wire_name": "timezone", "required": True})
    metadata: dict[str, Any] | None = field(
        default=None, metadata={"wire_name": "metadata", "required": True}
    )
    created_at: str = field(default="", metadata={"wire_name": "createdAt", "required": True})
    updated_at: str = field(default="", metadata={"wire_name": "updatedAt", "required": True})
    object: Literal["customer"] | None = field(
        default=None, metadata={"wire_name": "object", "required": True}
    )
    livemode: bool = field(default=False, metadata={"wire_name": "livemode", "required": True})


@dataclass
class CustomerBatch:
    successful: list[CustomerBatchSuccessfulItem] = field(
        default_factory=list, metadata={"wire_name": "successful", "required": True}
    )
    failed: list[CustomerBatchFailedItem] = field(
        default_factory=list, metadata={"wire_name": "failed", "required": True}
    )
    object: Literal["customer_batch"] | None = field(
        default=None, metadata={"wire_name": "object", "required": True}
    )
    livemode: bool = field(default=False, metadata={"wire_name": "livemode", "required": True})


@dataclass
class CustomerBatchFailedItem:
    index: int = field(default=0, metadata={"wire_name": "index", "required": True})
    error: str = field(default="", metadata={"wire_name": "error", "required": True})
    data: CustomerBatchFailedItemData | None = field(
        default=None, metadata={"wire_name": "data", "required": True}
    )


@dataclass
class CustomerBatchFailedItemData:
    id: str | None = field(default=None, metadata={"wire_name": "id", "required": False})
    external_id: str | None = field(
        default=None, metadata={"wire_name": "externalId", "required": False}
    )
    email: str = field(default="", metadata={"wire_name": "email", "required": True})
    full_name: str | None = field(
        default=None, metadata={"wire_name": "fullName", "required": False}
    )
    tax_document: str | None = field(
        default=None, metadata={"wire_name": "taxDocument", "required": False}
    )
    timezone: str | None = field(
        default=None, metadata={"wire_name": "timezone", "required": False}
    )
    metadata: dict[str, Any] | None = field(
        default=None, metadata={"wire_name": "metadata", "required": False}
    )
    address: CustomerBatchFailedItemDataAddress | None = field(
        default=None, metadata={"wire_name": "address", "required": False}
    )


@dataclass
class CustomerBatchFailedItemDataAddress:
    line1: str = field(default="", metadata={"wire_name": "line1", "required": True})
    line2: str | None = field(default=None, metadata={"wire_name": "line2", "required": False})
    city: str = field(default="", metadata={"wire_name": "city", "required": True})
    state: str | None = field(default=None, metadata={"wire_name": "state", "required": False})
    postal_code: str = field(default="", metadata={"wire_name": "postalCode", "required": True})
    country: str = field(default="", metadata={"wire_name": "country", "required": True})
    region: str | None = field(default=None, metadata={"wire_name": "region", "required": False})


@dataclass
class CustomerBatchSuccessfulItem:
    id: str = field(default="", metadata={"wire_name": "id", "required": True})
    external_id: str | None = field(
        default=None, metadata={"wire_name": "externalId", "required": True}
    )
    email: str = field(default="", metadata={"wire_name": "email", "required": True})


@dataclass
class CustomerCredit:
    id: str = field(default="", metadata={"wire_name": "id", "required": True})
    amount: int = field(default=0, metadata={"wire_name": "amount", "required": True})
    applied_amount: int = field(
        default=0, metadata={"wire_name": "appliedAmount", "required": True}
    )
    reversed_amount: int = field(
        default=0, metadata={"wire_name": "reversedAmount", "required": True}
    )
    revoked_amount: int = field(
        default=0, metadata={"wire_name": "revokedAmount", "required": True}
    )
    remaining_amount: int = field(
        default=0, metadata={"wire_name": "remainingAmount", "required": True}
    )
    currency: str = field(default="", metadata={"wire_name": "currency", "required": True})
    reason: str = field(default="", metadata={"wire_name": "reason", "required": True})
    source: Literal["dashboard", "api", "plan_change", "migration"] | None = field(
        default=None, metadata={"wire_name": "source", "required": True}
    )
    expires_at: str | None = field(
        default=None, metadata={"wire_name": "expiresAt", "required": True}
    )
    created_at: str = field(default="", metadata={"wire_name": "createdAt", "required": True})
    object: Literal["customer_credit"] | None = field(
        default=None, metadata={"wire_name": "object", "required": True}
    )
    livemode: bool = field(default=False, metadata={"wire_name": "livemode", "required": True})


@dataclass
class CustomerCreditRevocation:
    id: str = field(default="", metadata={"wire_name": "id", "required": True})
    remaining_amount: int = field(
        default=0, metadata={"wire_name": "remainingAmount", "required": True}
    )
    revoked_amount: int = field(
        default=0, metadata={"wire_name": "revokedAmount", "required": True}
    )
    currency: str = field(default="", metadata={"wire_name": "currency", "required": True})
    object: Literal["customer_credit"] | None = field(
        default=None, metadata={"wire_name": "object", "required": True}
    )
    livemode: bool = field(default=False, metadata={"wire_name": "livemode", "required": True})


@dataclass
class CustomersListCreditsResult:
    object: Literal["list"] | None = field(
        default=None, metadata={"wire_name": "object", "required": True}
    )
    data: list[CustomerCredit] = field(
        default_factory=list, metadata={"wire_name": "data", "required": True}
    )
    has_more: bool = field(default=False, metadata={"wire_name": "hasMore", "required": True})
    next_cursor: str | None = field(
        default=None, metadata={"wire_name": "nextCursor", "required": False}
    )


@dataclass
class CustomersListPlanGrantsResult:
    object: Literal["list"] | None = field(
        default=None, metadata={"wire_name": "object", "required": True}
    )
    data: list[PlanGrant] = field(
        default_factory=list, metadata={"wire_name": "data", "required": True}
    )
    has_more: bool = field(default=False, metadata={"wire_name": "hasMore", "required": True})
    next_cursor: str | None = field(
        default=None, metadata={"wire_name": "nextCursor", "required": False}
    )


@dataclass
class CustomersListResult:
    object: Literal["list"] | None = field(
        default=None, metadata={"wire_name": "object", "required": True}
    )
    data: list[Customer] = field(
        default_factory=list, metadata={"wire_name": "data", "required": True}
    )
    has_more: bool = field(default=False, metadata={"wire_name": "hasMore", "required": True})
    next_cursor: str | None = field(
        default=None, metadata={"wire_name": "nextCursor", "required": False}
    )


@dataclass
class DeletedObject:
    id: str = field(default="", metadata={"wire_name": "id", "required": True})
    deleted: Literal[True] | None = field(
        default=None, metadata={"wire_name": "deleted", "required": True}
    )
    object: str = field(default="", metadata={"wire_name": "object", "required": True})
    livemode: bool = field(default=False, metadata={"wire_name": "livemode", "required": True})


@dataclass
class DeletedOffer:
    deleted: Literal[True] | None = field(
        default=None, metadata={"wire_name": "deleted", "required": True}
    )
    object: Literal["offer"] | None = field(
        default=None, metadata={"wire_name": "object", "required": True}
    )
    livemode: bool = field(default=False, metadata={"wire_name": "livemode", "required": True})


@dataclass
class DeletedPlanRegionalPricing:
    deleted: Literal[True] | None = field(
        default=None, metadata={"wire_name": "deleted", "required": True}
    )
    object: Literal["plan_regional_pricing"] | None = field(
        default=None, metadata={"wire_name": "object", "required": True}
    )
    livemode: bool = field(default=False, metadata={"wire_name": "livemode", "required": True})


@dataclass
class DeletedSubscriptionAddon:
    id: str = field(default="", metadata={"wire_name": "id", "required": True})
    status: Literal["inactive"] | None = field(
        default=None, metadata={"wire_name": "status", "required": True}
    )
    deactivated_at: str | None = field(
        default=None, metadata={"wire_name": "deactivatedAt", "required": True}
    )
    object: Literal["subscription_addon"] | None = field(
        default=None, metadata={"wire_name": "object", "required": True}
    )
    livemode: bool = field(default=False, metadata={"wire_name": "livemode", "required": True})


@dataclass
class Feature:
    id: str = field(default="", metadata={"wire_name": "id", "required": True})
    name: str = field(default="", metadata={"wire_name": "name", "required": True})
    code: str = field(default="", metadata={"wire_name": "code", "required": True})
    type: FeatureType | None = field(default=None, metadata={"wire_name": "type", "required": True})
    description: str | None = field(
        default=None, metadata={"wire_name": "description", "required": True}
    )
    unit_name: str | None = field(
        default=None, metadata={"wire_name": "unitName", "required": True}
    )
    created_at: str = field(default="", metadata={"wire_name": "createdAt", "required": True})
    updated_at: str = field(default="", metadata={"wire_name": "updatedAt", "required": True})
    object: Literal["feature"] | None = field(
        default=None, metadata={"wire_name": "object", "required": True}
    )
    livemode: bool = field(default=False, metadata={"wire_name": "livemode", "required": True})


@dataclass
class FeatureAccessListResult:
    object: Literal["list"] | None = field(
        default=None, metadata={"wire_name": "object", "required": True}
    )
    data: list[FeatureAccess] = field(
        default_factory=list, metadata={"wire_name": "data", "required": True}
    )
    has_more: bool = field(default=False, metadata={"wire_name": "hasMore", "required": True})
    next_cursor: str | None = field(
        default=None, metadata={"wire_name": "nextCursor", "required": False}
    )


@dataclass
class FeatureAccessVariant1:
    code: str = field(default="", metadata={"wire_name": "code", "required": True})
    name: str = field(default="", metadata={"wire_name": "name", "required": True})
    unit_name: str | None = field(
        default=None, metadata={"wire_name": "unitName", "required": True}
    )
    allowed: bool = field(default=False, metadata={"wire_name": "allowed", "required": True})
    type: Literal["boolean"] | None = field(
        default=None, metadata={"wire_name": "type", "required": True}
    )
    enabled: bool = field(default=False, metadata={"wire_name": "enabled", "required": True})
    base_access: FeatureAccessVariant1BaseAccess | None = field(
        default=None, metadata={"wire_name": "baseAccess", "required": False}
    )
    object: Literal["feature_access"] | None = field(
        default=None, metadata={"wire_name": "object", "required": True}
    )
    livemode: bool = field(default=False, metadata={"wire_name": "livemode", "required": True})


@dataclass
class FeatureAccessVariant1BaseAccess:
    enabled: bool = field(default=False, metadata={"wire_name": "enabled", "required": True})


@dataclass
class FeatureAccessVariant2:
    code: str = field(default="", metadata={"wire_name": "code", "required": True})
    name: str = field(default="", metadata={"wire_name": "name", "required": True})
    unit_name: str | None = field(
        default=None, metadata={"wire_name": "unitName", "required": True}
    )
    allowed: bool = field(default=False, metadata={"wire_name": "allowed", "required": True})
    type: Literal["usage"] | None = field(
        default=None, metadata={"wire_name": "type", "required": True}
    )
    consumption: FeatureAccessVariant2Consumption | None = field(
        default=None, metadata={"wire_name": "consumption", "required": True}
    )
    base_access: FeatureAccessVariant2BaseAccess | None = field(
        default=None, metadata={"wire_name": "baseAccess", "required": False}
    )
    object: Literal["feature_access"] | None = field(
        default=None, metadata={"wire_name": "object", "required": True}
    )
    livemode: bool = field(default=False, metadata={"wire_name": "livemode", "required": True})


@dataclass
class FeatureAccessVariant2BaseAccess:
    included_units: float = field(
        default=0.0, metadata={"wire_name": "includedUnits", "required": True}
    )
    unlimited: bool = field(default=False, metadata={"wire_name": "unlimited", "required": True})


@dataclass
class FeatureAccessVariant2ConsumptionVariant1:
    model: Literal["metered"] | None = field(
        default=None, metadata={"wire_name": "model", "required": True}
    )
    period: FeatureAccessVariant2ConsumptionVariant1Period | None = field(
        default=None, metadata={"wire_name": "period", "required": True}
    )
    units_used: float = field(default=0.0, metadata={"wire_name": "unitsUsed", "required": True})
    included_units: float = field(
        default=0.0, metadata={"wire_name": "includedUnits", "required": True}
    )
    remaining_units: float | None = field(
        default=None, metadata={"wire_name": "remainingUnits", "required": False}
    )
    unlimited: bool = field(default=False, metadata={"wire_name": "unlimited", "required": True})
    overage: FeatureAccessVariant2ConsumptionVariant1Overage | None = field(
        default=None, metadata={"wire_name": "overage", "required": True}
    )


@dataclass
class FeatureAccessVariant2ConsumptionVariant1Overage:
    enabled: bool = field(default=False, metadata={"wire_name": "enabled", "required": True})
    units: float = field(default=0.0, metadata={"wire_name": "units", "required": True})
    unit_price: FeatureAccessVariant2ConsumptionVariant1OverageUnitPrice | None = field(
        default=None, metadata={"wire_name": "unitPrice", "required": False}
    )


@dataclass
class FeatureAccessVariant2ConsumptionVariant1OverageUnitPrice:
    amount: int = field(default=0, metadata={"wire_name": "amount", "required": True})
    currency: str = field(default="", metadata={"wire_name": "currency", "required": True})
    scale: Literal[10000] | None = field(
        default=None, metadata={"wire_name": "scale", "required": True}
    )


@dataclass
class FeatureAccessVariant2ConsumptionVariant1Period:
    start: str = field(default="", metadata={"wire_name": "start", "required": True})
    end: str = field(default="", metadata={"wire_name": "end", "required": True})


@dataclass
class FeatureAccessVariant2ConsumptionVariant2:
    model: Literal["credits"] | None = field(
        default=None, metadata={"wire_name": "model", "required": True}
    )
    period: FeatureAccessVariant2ConsumptionVariant2Period | None = field(
        default=None, metadata={"wire_name": "period", "required": True}
    )
    units_used: float = field(default=0.0, metadata={"wire_name": "unitsUsed", "required": True})
    credits_per_unit: int = field(
        default=0, metadata={"wire_name": "creditsPerUnit", "required": True}
    )
    credits_consumed: float = field(
        default=0.0, metadata={"wire_name": "creditsConsumed", "required": True}
    )
    available_units: int = field(
        default=0, metadata={"wire_name": "availableUnits", "required": True}
    )


@dataclass
class FeatureAccessVariant2ConsumptionVariant2Period:
    start: str = field(default="", metadata={"wire_name": "start", "required": True})
    end: str = field(default="", metadata={"wire_name": "end", "required": True})


@dataclass
class FeatureAccessVariant2ConsumptionVariant3:
    model: Literal["balance"] | None = field(
        default=None, metadata={"wire_name": "model", "required": True}
    )
    period: FeatureAccessVariant2ConsumptionVariant3Period | None = field(
        default=None, metadata={"wire_name": "period", "required": True}
    )
    units_used: float = field(default=0.0, metadata={"wire_name": "unitsUsed", "required": True})
    spent: FeatureAccessVariant2ConsumptionVariant3Spent | None = field(
        default=None, metadata={"wire_name": "spent", "required": True}
    )
    available_units: int | None = field(
        default=None, metadata={"wire_name": "availableUnits", "required": False}
    )
    unit_price: FeatureAccessVariant2ConsumptionVariant3UnitPrice | None = field(
        default=None, metadata={"wire_name": "unitPrice", "required": False}
    )


@dataclass
class FeatureAccessVariant2ConsumptionVariant3Period:
    start: str = field(default="", metadata={"wire_name": "start", "required": True})
    end: str = field(default="", metadata={"wire_name": "end", "required": True})


@dataclass
class FeatureAccessVariant2ConsumptionVariant3Spent:
    amount: int = field(default=0, metadata={"wire_name": "amount", "required": True})
    currency: str = field(default="", metadata={"wire_name": "currency", "required": True})


@dataclass
class FeatureAccessVariant2ConsumptionVariant3UnitPrice:
    amount: int = field(default=0, metadata={"wire_name": "amount", "required": True})
    currency: str = field(default="", metadata={"wire_name": "currency", "required": True})
    scale: Literal[10000] | None = field(
        default=None, metadata={"wire_name": "scale", "required": True}
    )


@dataclass
class FeatureAccessVariant3:
    code: str = field(default="", metadata={"wire_name": "code", "required": True})
    name: str = field(default="", metadata={"wire_name": "name", "required": True})
    unit_name: str | None = field(
        default=None, metadata={"wire_name": "unitName", "required": True}
    )
    allowed: bool = field(default=False, metadata={"wire_name": "allowed", "required": True})
    type: Literal["seats"] | None = field(
        default=None, metadata={"wire_name": "type", "required": True}
    )
    usage: FeatureAccessVariant3Usage | None = field(
        default=None, metadata={"wire_name": "usage", "required": True}
    )
    base_access: FeatureAccessVariant3BaseAccess | None = field(
        default=None, metadata={"wire_name": "baseAccess", "required": False}
    )
    object: Literal["feature_access"] | None = field(
        default=None, metadata={"wire_name": "object", "required": True}
    )
    livemode: bool = field(default=False, metadata={"wire_name": "livemode", "required": True})


@dataclass
class FeatureAccessVariant3BaseAccess:
    included_units: float = field(
        default=0.0, metadata={"wire_name": "includedUnits", "required": True}
    )
    unlimited: bool = field(default=False, metadata={"wire_name": "unlimited", "required": True})


@dataclass
class FeatureAccessVariant3Usage:
    period: FeatureAccessVariant3UsagePeriod | None = field(
        default=None, metadata={"wire_name": "period", "required": True}
    )
    units_used: float = field(default=0.0, metadata={"wire_name": "unitsUsed", "required": True})
    included_units: float = field(
        default=0.0, metadata={"wire_name": "includedUnits", "required": True}
    )
    remaining_units: float | None = field(
        default=None, metadata={"wire_name": "remainingUnits", "required": False}
    )
    unlimited: bool = field(default=False, metadata={"wire_name": "unlimited", "required": True})
    overage: FeatureAccessVariant3UsageOverage | None = field(
        default=None, metadata={"wire_name": "overage", "required": True}
    )


@dataclass
class FeatureAccessVariant3UsageOverage:
    enabled: bool = field(default=False, metadata={"wire_name": "enabled", "required": True})
    units: float = field(default=0.0, metadata={"wire_name": "units", "required": True})
    unit_price: FeatureAccessVariant3UsageOverageUnitPrice | None = field(
        default=None, metadata={"wire_name": "unitPrice", "required": False}
    )


@dataclass
class FeatureAccessVariant3UsageOverageUnitPrice:
    amount: int = field(default=0, metadata={"wire_name": "amount", "required": True})
    currency: str = field(default="", metadata={"wire_name": "currency", "required": True})
    scale: Literal[10000] | None = field(
        default=None, metadata={"wire_name": "scale", "required": True}
    )


@dataclass
class FeatureAccessVariant3UsagePeriod:
    start: str = field(default="", metadata={"wire_name": "start", "required": True})
    end: str = field(default="", metadata={"wire_name": "end", "required": True})


@dataclass
class FeatureAccessVariant4:
    code: str = field(default="", metadata={"wire_name": "code", "required": True})
    name: str = field(default="", metadata={"wire_name": "name", "required": True})
    unit_name: str | None = field(
        default=None, metadata={"wire_name": "unitName", "required": True}
    )
    allowed: bool = field(default=False, metadata={"wire_name": "allowed", "required": True})
    type: Literal["quota"] | None = field(
        default=None, metadata={"wire_name": "type", "required": True}
    )
    usage: FeatureAccessVariant4Usage | None = field(
        default=None, metadata={"wire_name": "usage", "required": True}
    )
    base_access: FeatureAccessVariant4BaseAccess | None = field(
        default=None, metadata={"wire_name": "baseAccess", "required": False}
    )
    object: Literal["feature_access"] | None = field(
        default=None, metadata={"wire_name": "object", "required": True}
    )
    livemode: bool = field(default=False, metadata={"wire_name": "livemode", "required": True})


@dataclass
class FeatureAccessVariant4BaseAccess:
    included_units: float = field(
        default=0.0, metadata={"wire_name": "includedUnits", "required": True}
    )
    unlimited: bool = field(default=False, metadata={"wire_name": "unlimited", "required": True})


@dataclass
class FeatureAccessVariant4Usage:
    period: FeatureAccessVariant4UsagePeriod | None = field(
        default=None, metadata={"wire_name": "period", "required": True}
    )
    units_used: float = field(default=0.0, metadata={"wire_name": "unitsUsed", "required": True})
    included_units: float = field(
        default=0.0, metadata={"wire_name": "includedUnits", "required": True}
    )
    remaining_units: float | None = field(
        default=None, metadata={"wire_name": "remainingUnits", "required": False}
    )
    unlimited: bool = field(default=False, metadata={"wire_name": "unlimited", "required": True})
    overage: FeatureAccessVariant4UsageOverage | None = field(
        default=None, metadata={"wire_name": "overage", "required": True}
    )
    billed_units: float = field(
        default=0.0, metadata={"wire_name": "billedUnits", "required": True}
    )


@dataclass
class FeatureAccessVariant4UsageOverage:
    enabled: bool = field(default=False, metadata={"wire_name": "enabled", "required": True})
    units: float = field(default=0.0, metadata={"wire_name": "units", "required": True})
    unit_price: FeatureAccessVariant4UsageOverageUnitPrice | None = field(
        default=None, metadata={"wire_name": "unitPrice", "required": False}
    )


@dataclass
class FeatureAccessVariant4UsageOverageUnitPrice:
    amount: int = field(default=0, metadata={"wire_name": "amount", "required": True})
    currency: str = field(default="", metadata={"wire_name": "currency", "required": True})
    scale: Literal[10000] | None = field(
        default=None, metadata={"wire_name": "scale", "required": True}
    )


@dataclass
class FeatureAccessVariant4UsagePeriod:
    start: str = field(default="", metadata={"wire_name": "start", "required": True})
    end: str = field(default="", metadata={"wire_name": "end", "required": True})


@dataclass
class FeaturesListResult:
    object: Literal["list"] | None = field(
        default=None, metadata={"wire_name": "object", "required": True}
    )
    data: list[Feature] = field(
        default_factory=list, metadata={"wire_name": "data", "required": True}
    )
    has_more: bool = field(default=False, metadata={"wire_name": "hasMore", "required": True})
    next_cursor: str | None = field(
        default=None, metadata={"wire_name": "nextCursor", "required": False}
    )


@dataclass
class Invoice:
    id: str = field(default="", metadata={"wire_name": "id", "required": True})
    customer_id: str = field(default="", metadata={"wire_name": "customerId", "required": True})
    subscription_id: str | None = field(
        default=None, metadata={"wire_name": "subscriptionId", "required": True}
    )
    invoice_number: str = field(
        default="", metadata={"wire_name": "invoiceNumber", "required": True}
    )
    status: Literal["draft", "outstanding", "paid", "void", "uncollectible"] | None = field(
        default=None, metadata={"wire_name": "status", "required": True}
    )
    invoice_type: InvoiceType | None = field(
        default=None, metadata={"wire_name": "invoiceType", "required": True}
    )
    currency: str = field(default="", metadata={"wire_name": "currency", "required": True})
    subtotal: int = field(default=0, metadata={"wire_name": "subtotal", "required": True})
    discount_amount: int = field(
        default=0, metadata={"wire_name": "discountAmount", "required": True}
    )
    tax_amount: int = field(default=0, metadata={"wire_name": "taxAmount", "required": True})
    total: int = field(default=0, metadata={"wire_name": "total", "required": True})
    period_start: str = field(default="", metadata={"wire_name": "periodStart", "required": True})
    period_end: str = field(default="", metadata={"wire_name": "periodEnd", "required": True})
    issue_date: str = field(default="", metadata={"wire_name": "issueDate", "required": True})
    due_date: str = field(default="", metadata={"wire_name": "dueDate", "required": True})
    memo: str | None = field(default=None, metadata={"wire_name": "memo", "required": True})
    metadata: dict[str, Any] = field(
        default_factory=dict, metadata={"wire_name": "metadata", "required": True}
    )
    created_at: str = field(default="", metadata={"wire_name": "createdAt", "required": True})
    updated_at: str = field(default="", metadata={"wire_name": "updatedAt", "required": True})
    credit_applied: int = field(
        default=0, metadata={"wire_name": "creditApplied", "required": True}
    )
    plan_name: str | None = field(
        default=None, metadata={"wire_name": "planName", "required": True}
    )
    po_number: str | None = field(
        default=None, metadata={"wire_name": "poNumber", "required": True}
    )
    reference: str | None = field(
        default=None, metadata={"wire_name": "reference", "required": True}
    )
    line_items: list[InvoiceLineItemsItem] = field(
        default_factory=list, metadata={"wire_name": "lineItems", "required": True}
    )
    object: Literal["invoice"] | None = field(
        default=None, metadata={"wire_name": "object", "required": True}
    )
    livemode: bool = field(default=False, metadata={"wire_name": "livemode", "required": True})


@dataclass
class InvoiceDownload:
    url: str = field(default="", metadata={"wire_name": "url", "required": True})
    expires_at: str = field(default="", metadata={"wire_name": "expiresAt", "required": True})
    object: Literal["invoice_download_link"] | None = field(
        default=None, metadata={"wire_name": "object", "required": True}
    )
    livemode: bool = field(default=False, metadata={"wire_name": "livemode", "required": True})


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
    ) = field(default=None, metadata={"wire_name": "lineType", "required": True})
    feature_name: str | None = field(
        default=None, metadata={"wire_name": "featureName", "required": True}
    )
    description: str = field(default="", metadata={"wire_name": "description", "required": True})
    quantity: int = field(default=0, metadata={"wire_name": "quantity", "required": True})
    unit_amount: int = field(default=0, metadata={"wire_name": "unitAmount", "required": True})
    amount: int = field(default=0, metadata={"wire_name": "amount", "required": True})
    included_amount: int | None = field(
        default=None, metadata={"wire_name": "includedAmount", "required": True}
    )
    used_amount: int | None = field(
        default=None, metadata={"wire_name": "usedAmount", "required": True}
    )
    overage_amount: int | None = field(
        default=None, metadata={"wire_name": "overageAmount", "required": True}
    )
    discount_type: str | None = field(
        default=None, metadata={"wire_name": "discountType", "required": True}
    )
    discount_value: int | None = field(
        default=None, metadata={"wire_name": "discountValue", "required": True}
    )
    discount_name: str | None = field(
        default=None, metadata={"wire_name": "discountName", "required": True}
    )
    charge_type: Literal["standard", "advance", "true_up"] | None = field(
        default=None, metadata={"wire_name": "chargeType", "required": True}
    )


@dataclass
class InvoiceListItem:
    id: str = field(default="", metadata={"wire_name": "id", "required": True})
    customer_id: str = field(default="", metadata={"wire_name": "customerId", "required": True})
    subscription_id: str | None = field(
        default=None, metadata={"wire_name": "subscriptionId", "required": True}
    )
    invoice_number: str = field(
        default="", metadata={"wire_name": "invoiceNumber", "required": True}
    )
    status: Literal["draft", "outstanding", "paid", "void", "uncollectible"] | None = field(
        default=None, metadata={"wire_name": "status", "required": True}
    )
    invoice_type: InvoiceType | None = field(
        default=None, metadata={"wire_name": "invoiceType", "required": True}
    )
    currency: str = field(default="", metadata={"wire_name": "currency", "required": True})
    subtotal: int = field(default=0, metadata={"wire_name": "subtotal", "required": True})
    discount_amount: int = field(
        default=0, metadata={"wire_name": "discountAmount", "required": True}
    )
    tax_amount: int = field(default=0, metadata={"wire_name": "taxAmount", "required": True})
    total: int = field(default=0, metadata={"wire_name": "total", "required": True})
    period_start: str = field(default="", metadata={"wire_name": "periodStart", "required": True})
    period_end: str = field(default="", metadata={"wire_name": "periodEnd", "required": True})
    issue_date: str = field(default="", metadata={"wire_name": "issueDate", "required": True})
    due_date: str = field(default="", metadata={"wire_name": "dueDate", "required": True})
    memo: str | None = field(default=None, metadata={"wire_name": "memo", "required": True})
    metadata: dict[str, Any] = field(
        default_factory=dict, metadata={"wire_name": "metadata", "required": True}
    )
    created_at: str = field(default="", metadata={"wire_name": "createdAt", "required": True})
    updated_at: str = field(default="", metadata={"wire_name": "updatedAt", "required": True})
    object: Literal["invoice"] | None = field(
        default=None, metadata={"wire_name": "object", "required": True}
    )
    livemode: bool = field(default=False, metadata={"wire_name": "livemode", "required": True})


@dataclass
class InvoicesListResult:
    object: Literal["list"] | None = field(
        default=None, metadata={"wire_name": "object", "required": True}
    )
    data: list[InvoiceListItem] = field(
        default_factory=list, metadata={"wire_name": "data", "required": True}
    )
    has_more: bool = field(default=False, metadata={"wire_name": "hasMore", "required": True})
    next_cursor: str | None = field(
        default=None, metadata={"wire_name": "nextCursor", "required": False}
    )


@dataclass
class Market:
    id: str = field(default="", metadata={"wire_name": "id", "required": True})
    name: str = field(default="", metadata={"wire_name": "name", "required": True})
    country_codes: list[str] = field(
        default_factory=list, metadata={"wire_name": "countryCodes", "required": True}
    )
    metadata: dict[str, Any] = field(
        default_factory=dict, metadata={"wire_name": "metadata", "required": True}
    )
    created_at: str = field(default="", metadata={"wire_name": "createdAt", "required": True})
    updated_at: str = field(default="", metadata={"wire_name": "updatedAt", "required": True})
    object: Literal["market"] | None = field(
        default=None, metadata={"wire_name": "object", "required": True}
    )
    livemode: bool = field(default=False, metadata={"wire_name": "livemode", "required": True})


@dataclass
class MarketsListResult:
    object: Literal["list"] | None = field(
        default=None, metadata={"wire_name": "object", "required": True}
    )
    data: list[Market] = field(
        default_factory=list, metadata={"wire_name": "data", "required": True}
    )
    has_more: bool = field(default=False, metadata={"wire_name": "hasMore", "required": True})
    next_cursor: str | None = field(
        default=None, metadata={"wire_name": "nextCursor", "required": False}
    )


@dataclass
class Offer:
    id: str = field(default="", metadata={"wire_name": "id", "required": True})
    name: str = field(default="", metadata={"wire_name": "name", "required": True})
    phases: list[OfferPhasesItem] = field(
        default_factory=list, metadata={"wire_name": "phases", "required": True}
    )
    metadata: dict[str, Any] = field(
        default_factory=dict, metadata={"wire_name": "metadata", "required": True}
    )
    starts_at: str | None = field(
        default=None, metadata={"wire_name": "startsAt", "required": True}
    )
    ends_at: str | None = field(default=None, metadata={"wire_name": "endsAt", "required": True})
    active: bool = field(default=False, metadata={"wire_name": "active", "required": True})
    created_at: str = field(default="", metadata={"wire_name": "createdAt", "required": True})
    updated_at: str = field(default="", metadata={"wire_name": "updatedAt", "required": True})
    object: Literal["offer"] | None = field(
        default=None, metadata={"wire_name": "object", "required": True}
    )
    livemode: bool = field(default=False, metadata={"wire_name": "livemode", "required": True})


@dataclass
class OfferPhasesItemVariant1:
    type: Literal["free_trial"] | None = field(
        default=None, metadata={"wire_name": "type", "required": True}
    )
    duration_days: int = field(default=0, metadata={"wire_name": "durationDays", "required": True})


@dataclass
class OfferPhasesItemVariant2:
    type: Literal["percentage"] | None = field(
        default=None, metadata={"wire_name": "type", "required": True}
    )
    duration_cycles: int | None = field(
        default=None, metadata={"wire_name": "durationCycles", "required": True}
    )
    duration_interval: Literal["weekly", "monthly", "quarterly", "yearly"] | None = field(
        default=None, metadata={"wire_name": "durationInterval", "required": True}
    )
    percentage: int = field(default=0, metadata={"wire_name": "percentage", "required": True})


@dataclass
class OfferPhasesItemVariant3:
    type: Literal["amount_off"] | None = field(
        default=None, metadata={"wire_name": "type", "required": True}
    )
    duration_cycles: int | None = field(
        default=None, metadata={"wire_name": "durationCycles", "required": True}
    )
    duration_interval: Literal["weekly", "monthly", "quarterly", "yearly"] | None = field(
        default=None, metadata={"wire_name": "durationInterval", "required": True}
    )
    amounts: list[OfferPhasesItemVariant3AmountsItem] = field(
        default_factory=list, metadata={"wire_name": "amounts", "required": True}
    )


@dataclass
class OfferPhasesItemVariant3AmountsItem:
    currency: str = field(default="", metadata={"wire_name": "currency", "required": True})
    amount: int = field(default=0, metadata={"wire_name": "amount", "required": True})


@dataclass
class OfferPhasesItemVariant4:
    type: Literal["fixed_price"] | None = field(
        default=None, metadata={"wire_name": "type", "required": True}
    )
    duration_cycles: int | None = field(
        default=None, metadata={"wire_name": "durationCycles", "required": True}
    )
    duration_interval: Literal["weekly", "monthly", "quarterly", "yearly"] | None = field(
        default=None, metadata={"wire_name": "durationInterval", "required": True}
    )
    prices: list[OfferPhasesItemVariant4PricesItem] = field(
        default_factory=list, metadata={"wire_name": "prices", "required": True}
    )


@dataclass
class OfferPhasesItemVariant4PricesItem:
    currency: str = field(default="", metadata={"wire_name": "currency", "required": True})
    amount: int = field(default=0, metadata={"wire_name": "amount", "required": True})


@dataclass
class OffersListResult:
    object: Literal["list"] | None = field(
        default=None, metadata={"wire_name": "object", "required": True}
    )
    data: list[Offer] = field(
        default_factory=list, metadata={"wire_name": "data", "required": True}
    )
    has_more: bool = field(default=False, metadata={"wire_name": "hasMore", "required": True})
    next_cursor: str | None = field(
        default=None, metadata={"wire_name": "nextCursor", "required": False}
    )


@dataclass
class Payment:
    payment_context: PaymentPaymentContext | None = field(
        default=None, metadata={"wire_name": "paymentContext", "required": True}
    )
    id: str = field(default="", metadata={"wire_name": "id", "required": True})
    customer_id: str | None = field(
        default=None, metadata={"wire_name": "customerId", "required": True}
    )
    kind: Literal["link", "charge"] | None = field(
        default=None, metadata={"wire_name": "kind", "required": True}
    )
    status: (
        Literal["pending", "processing", "succeeded", "requires_action", "failed", "canceled"]
        | None
    ) = field(default=None, metadata={"wire_name": "status", "required": True})
    provider: Literal["stripe", "commet", "dlocal"] | None = field(
        default=None, metadata={"wire_name": "provider", "required": True}
    )
    amount_subtotal: int = field(
        default=0, metadata={"wire_name": "amountSubtotal", "required": True}
    )
    tax_amount: int = field(default=0, metadata={"wire_name": "taxAmount", "required": True})
    amount_total: int = field(default=0, metadata={"wire_name": "amountTotal", "required": True})
    currency: str = field(default="", metadata={"wire_name": "currency", "required": True})
    description: str = field(default="", metadata={"wire_name": "description", "required": True})
    metadata: dict[str, Any] | None = field(
        default=None, metadata={"wire_name": "metadata", "required": True}
    )
    url: str | None = field(default=None, metadata={"wire_name": "url", "required": True})
    expires_at: str | None = field(
        default=None, metadata={"wire_name": "expiresAt", "required": True}
    )
    created_at: str = field(default="", metadata={"wire_name": "createdAt", "required": True})
    updated_at: str = field(default="", metadata={"wire_name": "updatedAt", "required": True})
    object: Literal["payment"] | None = field(
        default=None, metadata={"wire_name": "object", "required": True}
    )
    livemode: bool = field(default=False, metadata={"wire_name": "livemode", "required": True})


@dataclass
class PaymentMethodUpdateCheckout:
    checkout_url: str = field(default="", metadata={"wire_name": "checkoutUrl", "required": True})
    object: Literal["checkout_session"] | None = field(
        default=None, metadata={"wire_name": "object", "required": True}
    )
    livemode: bool = field(default=False, metadata={"wire_name": "livemode", "required": True})


@dataclass
class PaymentPaymentContext:
    reason: (
        Literal[
            "first_subscription_payment",
            "trial_conversion",
            "recurring_billing",
            "plan_change",
            "reactivation",
            "subscription_resume",
            "one_time_payment",
            "overage",
            "adjustment",
        ]
        | None
    ) = field(default=None, metadata={"wire_name": "reason", "required": True})
    payment_link_id: str | None = field(
        default=None, metadata={"wire_name": "paymentLinkId", "required": True}
    )
    recovery: PaymentPaymentContextRecovery | None = field(
        default=None, metadata={"wire_name": "recovery", "required": True}
    )


@dataclass
class PaymentPaymentContextRecoveryVariant1:
    type: Literal["payment_recovery"] | None = field(
        default=None, metadata={"wire_name": "type", "required": True}
    )


@dataclass
class PaymentPaymentContextRecoveryVariant2:
    type: Literal["dunning_retry"] | None = field(
        default=None, metadata={"wire_name": "type", "required": True}
    )
    attempt: int = field(default=0, metadata={"wire_name": "attempt", "required": True})
    max_attempts: int = field(default=0, metadata={"wire_name": "maxAttempts", "required": True})


@dataclass
class PaymentsListResult:
    object: Literal["list"] | None = field(
        default=None, metadata={"wire_name": "object", "required": True}
    )
    data: list[Payment] = field(
        default_factory=list, metadata={"wire_name": "data", "required": True}
    )
    has_more: bool = field(default=False, metadata={"wire_name": "hasMore", "required": True})
    next_cursor: str | None = field(
        default=None, metadata={"wire_name": "nextCursor", "required": False}
    )


@dataclass
class Payout:
    id: str = field(default="", metadata={"wire_name": "id", "required": True})
    status: Literal["pending", "in_transit", "paid", "failed", "canceled"] | None = field(
        default=None, metadata={"wire_name": "status", "required": True}
    )
    amount: int = field(default=0, metadata={"wire_name": "amount", "required": True})
    fee: int = field(default=0, metadata={"wire_name": "fee", "required": True})
    net_amount: int = field(default=0, metadata={"wire_name": "netAmount", "required": True})
    currency: str = field(default="", metadata={"wire_name": "currency", "required": True})
    description: str | None = field(
        default=None, metadata={"wire_name": "description", "required": True}
    )
    provider_transfer_id: str = field(
        default="", metadata={"wire_name": "providerTransferId", "required": True}
    )
    created_at: str = field(default="", metadata={"wire_name": "createdAt", "required": True})
    object: Literal["payout"] | None = field(
        default=None, metadata={"wire_name": "object", "required": True}
    )
    livemode: bool = field(default=False, metadata={"wire_name": "livemode", "required": True})


@dataclass
class PayoutBankAccount:
    id: str = field(default="", metadata={"wire_name": "id", "required": True})
    provider_external_account_id: str | None = field(
        default=None, metadata={"wire_name": "providerExternalAccountId", "required": True}
    )
    holder_name: str = field(default="", metadata={"wire_name": "holderName", "required": True})
    last4: str = field(default="", metadata={"wire_name": "last4", "required": True})
    bank_name: str | None = field(
        default=None, metadata={"wire_name": "bankName", "required": True}
    )
    country: str = field(default="", metadata={"wire_name": "country", "required": True})
    currency: str = field(default="", metadata={"wire_name": "currency", "required": True})
    account_type: Literal["checking", "savings"] | None = field(
        default=None, metadata={"wire_name": "accountType", "required": True}
    )
    is_default: bool = field(default=False, metadata={"wire_name": "isDefault", "required": True})
    status: Literal["active", "errored"] | None = field(
        default=None, metadata={"wire_name": "status", "required": True}
    )
    created_at: str = field(default="", metadata={"wire_name": "createdAt", "required": True})
    object: Literal["payout_bank_account"] | None = field(
        default=None, metadata={"wire_name": "object", "required": True}
    )
    livemode: bool = field(default=False, metadata={"wire_name": "livemode", "required": True})


@dataclass
class Plan:
    id: str = field(default="", metadata={"wire_name": "id", "required": True})
    name: str = field(default="", metadata={"wire_name": "name", "required": True})
    code: str = field(default="", metadata={"wire_name": "code", "required": True})
    description: str | None = field(
        default=None, metadata={"wire_name": "description", "required": True}
    )
    consumption_model: ConsumptionModel | None = field(
        default=None, metadata={"wire_name": "consumptionModel", "required": True}
    )
    is_public: bool = field(default=False, metadata={"wire_name": "isPublic", "required": True})
    is_default: bool = field(default=False, metadata={"wire_name": "isDefault", "required": True})
    is_free: bool = field(default=False, metadata={"wire_name": "isFree", "required": True})
    block_on_exhaustion: bool | None = field(
        default=None, metadata={"wire_name": "blockOnExhaustion", "required": True}
    )
    sort_order: int = field(default=0, metadata={"wire_name": "sortOrder", "required": True})
    plan_group_id: str | None = field(
        default=None, metadata={"wire_name": "planGroupId", "required": True}
    )
    metadata: dict[str, Any] | None = field(
        default=None, metadata={"wire_name": "metadata", "required": True}
    )
    created_at: str = field(default="", metadata={"wire_name": "createdAt", "required": True})
    updated_at: str = field(default="", metadata={"wire_name": "updatedAt", "required": True})
    features: list[PlanFeaturesItem] = field(
        default_factory=list, metadata={"wire_name": "features", "required": True}
    )
    prices: list[PlanPricesItem] = field(
        default_factory=list, metadata={"wire_name": "prices", "required": True}
    )
    exchange_rates: list[PlanExchangeRatesItem] = field(
        default_factory=list, metadata={"wire_name": "exchangeRates", "required": True}
    )
    object: Literal["plan"] | None = field(
        default=None, metadata={"wire_name": "object", "required": True}
    )
    livemode: bool = field(default=False, metadata={"wire_name": "livemode", "required": True})


@dataclass
class PlanChangeVariant1:
    outcome: Literal["requires_checkout"] | None = field(
        default=None, metadata={"wire_name": "outcome", "required": True}
    )
    requires_checkout: Literal[True] | None = field(
        default=None, metadata={"wire_name": "requiresCheckout", "required": True}
    )
    checkout_url: str = field(default="", metadata={"wire_name": "checkoutUrl", "required": True})
    offer_application: PlanChangeVariant1OfferApplication | None = field(
        default=None, metadata={"wire_name": "offerApplication", "required": False}
    )
    object: Literal["plan_change"] | None = field(
        default=None, metadata={"wire_name": "object", "required": True}
    )
    livemode: bool = field(default=False, metadata={"wire_name": "livemode", "required": True})


@dataclass
class PlanChangeVariant1OfferApplication:
    id: str = field(default="", metadata={"wire_name": "id", "required": True})
    offer_id: str = field(default="", metadata={"wire_name": "offerId", "required": True})
    name: str = field(default="", metadata={"wire_name": "name", "required": True})
    currency: str = field(default="", metadata={"wire_name": "currency", "required": True})
    subtotal: int = field(default=0, metadata={"wire_name": "subtotal", "required": True})
    discount_amount: int = field(
        default=0, metadata={"wire_name": "discountAmount", "required": True}
    )
    total: int = field(default=0, metadata={"wire_name": "total", "required": True})
    phases: list[PlanChangeVariant1OfferApplicationPhasesItem] = field(
        default_factory=list, metadata={"wire_name": "phases", "required": True}
    )
    applies_to: PlanChangeVariant1OfferApplicationAppliesTo | None = field(
        default=None, metadata={"wire_name": "appliesTo", "required": True}
    )


@dataclass
class PlanChangeVariant1OfferApplicationAppliesToVariant1:
    type: Literal["plan_price"] | None = field(
        default=None, metadata={"wire_name": "type", "required": True}
    )
    id: str = field(default="", metadata={"wire_name": "id", "required": True})


@dataclass
class PlanChangeVariant1OfferApplicationAppliesToVariant2:
    type: Literal["addon"] | None = field(
        default=None, metadata={"wire_name": "type", "required": True}
    )
    id: str = field(default="", metadata={"wire_name": "id", "required": True})


@dataclass
class PlanChangeVariant1OfferApplicationAppliesToVariant3:
    type: Literal["credit_pack"] | None = field(
        default=None, metadata={"wire_name": "type", "required": True}
    )
    id: str = field(default="", metadata={"wire_name": "id", "required": True})


@dataclass
class PlanChangeVariant1OfferApplicationPhasesItemVariant1:
    type: Literal["free_trial"] | None = field(
        default=None, metadata={"wire_name": "type", "required": True}
    )
    duration_days: int = field(default=0, metadata={"wire_name": "durationDays", "required": True})
    starts_at: str | None = field(
        default=None, metadata={"wire_name": "startsAt", "required": True}
    )
    ends_at: str | None = field(default=None, metadata={"wire_name": "endsAt", "required": True})


@dataclass
class PlanChangeVariant1OfferApplicationPhasesItemVariant2:
    type: Literal["percentage"] | None = field(
        default=None, metadata={"wire_name": "type", "required": True}
    )
    duration_cycles: int | None = field(
        default=None, metadata={"wire_name": "durationCycles", "required": True}
    )
    duration_interval: Literal["weekly", "monthly", "quarterly", "yearly"] | None = field(
        default=None, metadata={"wire_name": "durationInterval", "required": True}
    )
    starts_at: str | None = field(
        default=None, metadata={"wire_name": "startsAt", "required": True}
    )
    ends_at: str | None = field(default=None, metadata={"wire_name": "endsAt", "required": True})
    percentage: int = field(default=0, metadata={"wire_name": "percentage", "required": True})


@dataclass
class PlanChangeVariant1OfferApplicationPhasesItemVariant3:
    type: Literal["amount_off"] | None = field(
        default=None, metadata={"wire_name": "type", "required": True}
    )
    duration_cycles: int | None = field(
        default=None, metadata={"wire_name": "durationCycles", "required": True}
    )
    duration_interval: Literal["weekly", "monthly", "quarterly", "yearly"] | None = field(
        default=None, metadata={"wire_name": "durationInterval", "required": True}
    )
    starts_at: str | None = field(
        default=None, metadata={"wire_name": "startsAt", "required": True}
    )
    ends_at: str | None = field(default=None, metadata={"wire_name": "endsAt", "required": True})
    amount: int = field(default=0, metadata={"wire_name": "amount", "required": True})


@dataclass
class PlanChangeVariant1OfferApplicationPhasesItemVariant4:
    type: Literal["fixed_price"] | None = field(
        default=None, metadata={"wire_name": "type", "required": True}
    )
    duration_cycles: int | None = field(
        default=None, metadata={"wire_name": "durationCycles", "required": True}
    )
    duration_interval: Literal["weekly", "monthly", "quarterly", "yearly"] | None = field(
        default=None, metadata={"wire_name": "durationInterval", "required": True}
    )
    starts_at: str | None = field(
        default=None, metadata={"wire_name": "startsAt", "required": True}
    )
    ends_at: str | None = field(default=None, metadata={"wire_name": "endsAt", "required": True})
    price: int = field(default=0, metadata={"wire_name": "price", "required": True})


@dataclass
class PlanChangeVariant2:
    outcome: Literal["scheduled"] | None = field(
        default=None, metadata={"wire_name": "outcome", "required": True}
    )
    id: str = field(default="", metadata={"wire_name": "id", "required": True})
    scheduled: Literal[True] | None = field(
        default=None, metadata={"wire_name": "scheduled", "required": True}
    )
    scheduled_for: str = field(default="", metadata={"wire_name": "scheduledFor", "required": True})
    change_type: (
        Literal[
            "subscription.plan_downgrade", "subscription.interval_change", "subscription.cancel"
        ]
        | None
    ) = field(default=None, metadata={"wire_name": "changeType", "required": True})
    customer_id: str = field(default="", metadata={"wire_name": "customerId", "required": True})
    new_plan_id: str | None = field(
        default=None, metadata={"wire_name": "newPlanId", "required": False}
    )
    new_plan_name: str | None = field(
        default=None, metadata={"wire_name": "newPlanName", "required": False}
    )
    new_billing_interval: str | None = field(
        default=None, metadata={"wire_name": "newBillingInterval", "required": False}
    )
    seat_limit_warning: PlanChangeVariant2SeatLimitWarning | None = field(
        default=None, metadata={"wire_name": "seatLimitWarning", "required": False}
    )
    object: Literal["plan_change"] | None = field(
        default=None, metadata={"wire_name": "object", "required": True}
    )
    livemode: bool = field(default=False, metadata={"wire_name": "livemode", "required": True})


@dataclass
class PlanChangeVariant2SeatLimitWarning:
    feature_code: str = field(default="", metadata={"wire_name": "featureCode", "required": True})
    feature_name: str = field(default="", metadata={"wire_name": "featureName", "required": True})
    current_seats: int = field(default=0, metadata={"wire_name": "currentSeats", "required": True})
    included: int = field(default=0, metadata={"wire_name": "included", "required": True})
    new_plan_name: str = field(default="", metadata={"wire_name": "newPlanName", "required": True})
    effective_date: str = field(
        default="", metadata={"wire_name": "effectiveDate", "required": True}
    )


@dataclass
class PlanChangeVariant3:
    outcome: Literal["completed"] | None = field(
        default=None, metadata={"wire_name": "outcome", "required": True}
    )
    id: str = field(default="", metadata={"wire_name": "id", "required": True})
    scheduled: Literal[False] | None = field(
        default=None, metadata={"wire_name": "scheduled", "required": True}
    )
    customer_id: str = field(default="", metadata={"wire_name": "customerId", "required": True})
    previous_plan: PlanChangeVariant3PreviousPlan | None = field(
        default=None, metadata={"wire_name": "previousPlan", "required": True}
    )
    current_plan: PlanChangeVariant3CurrentPlan | None = field(
        default=None, metadata={"wire_name": "currentPlan", "required": True}
    )
    billing_interval: str = field(
        default="", metadata={"wire_name": "billingInterval", "required": True}
    )
    billing: PlanChangeVariant3Billing | None = field(
        default=None, metadata={"wire_name": "billing", "required": True}
    )
    invoice_id: str | None = field(
        default=None, metadata={"wire_name": "invoiceId", "required": False}
    )
    offer_application: PlanChangeVariant3OfferApplication | None = field(
        default=None, metadata={"wire_name": "offerApplication", "required": False}
    )
    object: Literal["plan_change"] | None = field(
        default=None, metadata={"wire_name": "object", "required": True}
    )
    livemode: bool = field(default=False, metadata={"wire_name": "livemode", "required": True})


@dataclass
class PlanChangeVariant3Billing:
    credit: int = field(default=0, metadata={"wire_name": "credit", "required": True})
    credits_applied: int = field(
        default=0, metadata={"wire_name": "creditsApplied", "required": True}
    )
    charge: int = field(default=0, metadata={"wire_name": "charge", "required": True})
    tax_amount: int = field(default=0, metadata={"wire_name": "taxAmount", "required": True})
    net_amount: int = field(default=0, metadata={"wire_name": "netAmount", "required": True})
    total_charged: int = field(default=0, metadata={"wire_name": "totalCharged", "required": True})
    remaining_credit_balance: int = field(
        default=0, metadata={"wire_name": "remainingCreditBalance", "required": True}
    )


@dataclass
class PlanChangeVariant3CurrentPlan:
    id: str = field(default="", metadata={"wire_name": "id", "required": True})
    name: str = field(default="", metadata={"wire_name": "name", "required": True})
    price: int = field(default=0, metadata={"wire_name": "price", "required": True})


@dataclass
class PlanChangeVariant3OfferApplication:
    id: str = field(default="", metadata={"wire_name": "id", "required": True})
    offer_id: str = field(default="", metadata={"wire_name": "offerId", "required": True})
    name: str = field(default="", metadata={"wire_name": "name", "required": True})
    currency: str = field(default="", metadata={"wire_name": "currency", "required": True})
    subtotal: int = field(default=0, metadata={"wire_name": "subtotal", "required": True})
    discount_amount: int = field(
        default=0, metadata={"wire_name": "discountAmount", "required": True}
    )
    total: int = field(default=0, metadata={"wire_name": "total", "required": True})
    phases: list[PlanChangeVariant3OfferApplicationPhasesItem] = field(
        default_factory=list, metadata={"wire_name": "phases", "required": True}
    )
    applies_to: PlanChangeVariant3OfferApplicationAppliesTo | None = field(
        default=None, metadata={"wire_name": "appliesTo", "required": True}
    )


@dataclass
class PlanChangeVariant3OfferApplicationAppliesToVariant1:
    type: Literal["plan_price"] | None = field(
        default=None, metadata={"wire_name": "type", "required": True}
    )
    id: str = field(default="", metadata={"wire_name": "id", "required": True})


@dataclass
class PlanChangeVariant3OfferApplicationAppliesToVariant2:
    type: Literal["addon"] | None = field(
        default=None, metadata={"wire_name": "type", "required": True}
    )
    id: str = field(default="", metadata={"wire_name": "id", "required": True})


@dataclass
class PlanChangeVariant3OfferApplicationAppliesToVariant3:
    type: Literal["credit_pack"] | None = field(
        default=None, metadata={"wire_name": "type", "required": True}
    )
    id: str = field(default="", metadata={"wire_name": "id", "required": True})


@dataclass
class PlanChangeVariant3OfferApplicationPhasesItemVariant1:
    type: Literal["free_trial"] | None = field(
        default=None, metadata={"wire_name": "type", "required": True}
    )
    duration_days: int = field(default=0, metadata={"wire_name": "durationDays", "required": True})
    starts_at: str | None = field(
        default=None, metadata={"wire_name": "startsAt", "required": True}
    )
    ends_at: str | None = field(default=None, metadata={"wire_name": "endsAt", "required": True})


@dataclass
class PlanChangeVariant3OfferApplicationPhasesItemVariant2:
    type: Literal["percentage"] | None = field(
        default=None, metadata={"wire_name": "type", "required": True}
    )
    duration_cycles: int | None = field(
        default=None, metadata={"wire_name": "durationCycles", "required": True}
    )
    duration_interval: Literal["weekly", "monthly", "quarterly", "yearly"] | None = field(
        default=None, metadata={"wire_name": "durationInterval", "required": True}
    )
    starts_at: str | None = field(
        default=None, metadata={"wire_name": "startsAt", "required": True}
    )
    ends_at: str | None = field(default=None, metadata={"wire_name": "endsAt", "required": True})
    percentage: int = field(default=0, metadata={"wire_name": "percentage", "required": True})


@dataclass
class PlanChangeVariant3OfferApplicationPhasesItemVariant3:
    type: Literal["amount_off"] | None = field(
        default=None, metadata={"wire_name": "type", "required": True}
    )
    duration_cycles: int | None = field(
        default=None, metadata={"wire_name": "durationCycles", "required": True}
    )
    duration_interval: Literal["weekly", "monthly", "quarterly", "yearly"] | None = field(
        default=None, metadata={"wire_name": "durationInterval", "required": True}
    )
    starts_at: str | None = field(
        default=None, metadata={"wire_name": "startsAt", "required": True}
    )
    ends_at: str | None = field(default=None, metadata={"wire_name": "endsAt", "required": True})
    amount: int = field(default=0, metadata={"wire_name": "amount", "required": True})


@dataclass
class PlanChangeVariant3OfferApplicationPhasesItemVariant4:
    type: Literal["fixed_price"] | None = field(
        default=None, metadata={"wire_name": "type", "required": True}
    )
    duration_cycles: int | None = field(
        default=None, metadata={"wire_name": "durationCycles", "required": True}
    )
    duration_interval: Literal["weekly", "monthly", "quarterly", "yearly"] | None = field(
        default=None, metadata={"wire_name": "durationInterval", "required": True}
    )
    starts_at: str | None = field(
        default=None, metadata={"wire_name": "startsAt", "required": True}
    )
    ends_at: str | None = field(default=None, metadata={"wire_name": "endsAt", "required": True})
    price: int = field(default=0, metadata={"wire_name": "price", "required": True})


@dataclass
class PlanChangeVariant3PreviousPlan:
    id: str = field(default="", metadata={"wire_name": "id", "required": True})
    name: str = field(default="", metadata={"wire_name": "name", "required": True})


@dataclass
class PlanExchangeRatesItem:
    currency: str = field(default="", metadata={"wire_name": "currency", "required": True})
    exchange_rate: float = field(
        default=0.0, metadata={"wire_name": "exchangeRate", "required": True}
    )


@dataclass
class PlanFeature:
    plan_id: str = field(default="", metadata={"wire_name": "planId", "required": True})
    feature_id: str = field(default="", metadata={"wire_name": "featureId", "required": True})
    enabled: bool = field(default=False, metadata={"wire_name": "enabled", "required": True})
    included_amount: int = field(
        default=0, metadata={"wire_name": "includedAmount", "required": True}
    )
    unlimited: bool = field(default=False, metadata={"wire_name": "unlimited", "required": True})
    overage: PlanFeatureOverage | None = field(
        default=None, metadata={"wire_name": "overage", "required": True}
    )
    credits_per_unit: int | None = field(
        default=None, metadata={"wire_name": "creditsPerUnit", "required": True}
    )
    pricing_mode: Literal["fixed", "ai_model"] | None = field(
        default=None, metadata={"wire_name": "pricingMode", "required": True}
    )
    margin: int | None = field(default=None, metadata={"wire_name": "margin", "required": True})
    object: Literal["plan_feature"] | None = field(
        default=None, metadata={"wire_name": "object", "required": True}
    )
    livemode: bool = field(default=False, metadata={"wire_name": "livemode", "required": True})


@dataclass
class PlanFeatureOverage:
    enabled: bool = field(default=False, metadata={"wire_name": "enabled", "required": True})
    unit_price: int = field(default=0, metadata={"wire_name": "unitPrice", "required": True})


@dataclass
class PlanFeaturesItem:
    code: str = field(default="", metadata={"wire_name": "code", "required": True})
    name: str = field(default="", metadata={"wire_name": "name", "required": True})
    type: FeatureType | None = field(default=None, metadata={"wire_name": "type", "required": True})
    unit_name: str | None = field(
        default=None, metadata={"wire_name": "unitName", "required": True}
    )
    enabled: bool = field(default=False, metadata={"wire_name": "enabled", "required": True})
    included_amount: int | None = field(
        default=None, metadata={"wire_name": "includedAmount", "required": True}
    )
    unlimited: bool = field(default=False, metadata={"wire_name": "unlimited", "required": True})
    overage: PlanFeaturesItemOverage | None = field(
        default=None, metadata={"wire_name": "overage", "required": True}
    )
    regional_prices: list[PlanFeaturesItemRegionalPricesItem] = field(
        default_factory=list, metadata={"wire_name": "regionalPrices", "required": True}
    )


@dataclass
class PlanFeaturesItemOverage:
    enabled: bool = field(default=False, metadata={"wire_name": "enabled", "required": True})
    model: Literal["per_unit"] | None = field(
        default=None, metadata={"wire_name": "model", "required": True}
    )
    unit_price: int | None = field(
        default=None, metadata={"wire_name": "unitPrice", "required": True}
    )


@dataclass
class PlanFeaturesItemRegionalPricesItem:
    currency: str = field(default="", metadata={"wire_name": "currency", "required": True})
    overage_unit_price: int | None = field(
        default=None, metadata={"wire_name": "overageUnitPrice", "required": True}
    )
    auto_synced: bool = field(default=False, metadata={"wire_name": "autoSynced", "required": True})


@dataclass
class PlanGrant:
    id: str = field(default="", metadata={"wire_name": "id", "required": True})
    customer_id: str = field(default="", metadata={"wire_name": "customerId", "required": True})
    subscription_id: str = field(
        default="", metadata={"wire_name": "subscriptionId", "required": True}
    )
    base_plan_id: str = field(default="", metadata={"wire_name": "basePlanId", "required": True})
    plan_id: str = field(default="", metadata={"wire_name": "planId", "required": True})
    plan_release_id: str = field(
        default="", metadata={"wire_name": "planReleaseId", "required": True}
    )
    status: Literal["active", "expired", "revoked"] | None = field(
        default=None, metadata={"wire_name": "status", "required": True}
    )
    duration: Literal["cycles", "until_date", "until_revoked"] | None = field(
        default=None, metadata={"wire_name": "duration", "required": True}
    )
    duration_cycles: int | None = field(
        default=None, metadata={"wire_name": "durationCycles", "required": True}
    )
    starts_at: str = field(default="", metadata={"wire_name": "startsAt", "required": True})
    expires_at: str | None = field(
        default=None, metadata={"wire_name": "expiresAt", "required": True}
    )
    reason: str = field(default="", metadata={"wire_name": "reason", "required": True})
    source: Literal["dashboard", "api"] | None = field(
        default=None, metadata={"wire_name": "source", "required": True}
    )
    revoked_at: str | None = field(
        default=None, metadata={"wire_name": "revokedAt", "required": True}
    )
    created_at: str = field(default="", metadata={"wire_name": "createdAt", "required": True})
    updated_at: str = field(default="", metadata={"wire_name": "updatedAt", "required": True})
    events: list[PlanGrantEventsItem] = field(
        default_factory=list, metadata={"wire_name": "events", "required": True}
    )
    object: Literal["plan_grant"] | None = field(
        default=None, metadata={"wire_name": "object", "required": True}
    )
    livemode: bool = field(default=False, metadata={"wire_name": "livemode", "required": True})


@dataclass
class PlanGrantEventsItem:
    id: str = field(default="", metadata={"wire_name": "id", "required": True})
    type: Literal["created", "updated", "expired", "revoked"] | None = field(
        default=None, metadata={"wire_name": "type", "required": True}
    )
    reason: str = field(default="", metadata={"wire_name": "reason", "required": True})
    source: Literal["dashboard", "api", "system"] | None = field(
        default=None, metadata={"wire_name": "source", "required": True}
    )
    previous_expires_at: str | None = field(
        default=None, metadata={"wire_name": "previousExpiresAt", "required": True}
    )
    expires_at: str | None = field(
        default=None, metadata={"wire_name": "expiresAt", "required": True}
    )
    duration: Literal["cycles", "until_date", "until_revoked"] | None = field(
        default=None, metadata={"wire_name": "duration", "required": True}
    )
    duration_cycles: int | None = field(
        default=None, metadata={"wire_name": "durationCycles", "required": True}
    )
    requested_expires_at: str | None = field(
        default=None, metadata={"wire_name": "requestedExpiresAt", "required": True}
    )
    created_at: str = field(default="", metadata={"wire_name": "createdAt", "required": True})


@dataclass
class PlanGroup:
    id: str = field(default="", metadata={"wire_name": "id", "required": True})
    name: str = field(default="", metadata={"wire_name": "name", "required": True})
    description: str | None = field(
        default=None, metadata={"wire_name": "description", "required": True}
    )
    is_public: bool = field(default=False, metadata={"wire_name": "isPublic", "required": True})
    created_at: str = field(default="", metadata={"wire_name": "createdAt", "required": True})
    updated_at: str = field(default="", metadata={"wire_name": "updatedAt", "required": True})
    object: Literal["plan_group"] | None = field(
        default=None, metadata={"wire_name": "object", "required": True}
    )
    livemode: bool = field(default=False, metadata={"wire_name": "livemode", "required": True})


@dataclass
class PlanGroupDetail:
    id: str = field(default="", metadata={"wire_name": "id", "required": True})
    name: str = field(default="", metadata={"wire_name": "name", "required": True})
    description: str | None = field(
        default=None, metadata={"wire_name": "description", "required": True}
    )
    is_public: bool = field(default=False, metadata={"wire_name": "isPublic", "required": True})
    created_at: str = field(default="", metadata={"wire_name": "createdAt", "required": True})
    updated_at: str = field(default="", metadata={"wire_name": "updatedAt", "required": True})
    plans: list[PlanGroupDetailPlansItem] = field(
        default_factory=list, metadata={"wire_name": "plans", "required": True}
    )
    object: Literal["plan_group"] | None = field(
        default=None, metadata={"wire_name": "object", "required": True}
    )
    livemode: bool = field(default=False, metadata={"wire_name": "livemode", "required": True})


@dataclass
class PlanGroupDetailPlansItem:
    id: str = field(default="", metadata={"wire_name": "id", "required": True})
    name: str = field(default="", metadata={"wire_name": "name", "required": True})
    sort_order: int = field(default=0, metadata={"wire_name": "sortOrder", "required": True})


@dataclass
class PlanGroupsListResult:
    object: Literal["list"] | None = field(
        default=None, metadata={"wire_name": "object", "required": True}
    )
    data: list[PlanGroup] = field(
        default_factory=list, metadata={"wire_name": "data", "required": True}
    )
    has_more: bool = field(default=False, metadata={"wire_name": "hasMore", "required": True})
    next_cursor: str | None = field(
        default=None, metadata={"wire_name": "nextCursor", "required": False}
    )


@dataclass
class PlanPrice:
    id: str = field(default="", metadata={"wire_name": "id", "required": True})
    plan_id: str = field(default="", metadata={"wire_name": "planId", "required": True})
    billing_interval: BillingInterval | None = field(
        default=None, metadata={"wire_name": "billingInterval", "required": True}
    )
    price: int = field(default=0, metadata={"wire_name": "price", "required": True})
    is_default: bool = field(default=False, metadata={"wire_name": "isDefault", "required": True})
    trial_days: int = field(default=0, metadata={"wire_name": "trialDays", "required": True})
    included_balance: int | None = field(
        default=None, metadata={"wire_name": "includedBalance", "required": True}
    )
    included_credits: int | None = field(
        default=None, metadata={"wire_name": "includedCredits", "required": True}
    )
    offer_id: str | None = field(default=None, metadata={"wire_name": "offerId", "required": True})
    inherits_from_price_id: str | None = field(
        default=None, metadata={"wire_name": "inheritsFromPriceId", "required": True}
    )
    metadata: dict[str, Any] = field(
        default_factory=dict, metadata={"wire_name": "metadata", "required": True}
    )
    market_prices: list[PlanPriceMarketPricesItem] = field(
        default_factory=list, metadata={"wire_name": "marketPrices", "required": True}
    )
    created_at: str = field(default="", metadata={"wire_name": "createdAt", "required": True})
    updated_at: str = field(default="", metadata={"wire_name": "updatedAt", "required": True})
    object: Literal["plan_price"] | None = field(
        default=None, metadata={"wire_name": "object", "required": True}
    )
    livemode: bool = field(default=False, metadata={"wire_name": "livemode", "required": True})


@dataclass
class PlanPriceMarketPricesItem:
    market_group_id: str = field(
        default="", metadata={"wire_name": "marketGroupId", "required": True}
    )
    currency: str = field(default="", metadata={"wire_name": "currency", "required": True})
    price: int = field(default=0, metadata={"wire_name": "price", "required": True})


@dataclass
class PlanPricesItem:
    id: str = field(default="", metadata={"wire_name": "id", "required": True})
    billing_interval: BillingInterval | None = field(
        default=None, metadata={"wire_name": "billingInterval", "required": True}
    )
    price: int = field(default=0, metadata={"wire_name": "price", "required": True})
    is_default: bool = field(default=False, metadata={"wire_name": "isDefault", "required": True})
    trial_days: int = field(default=0, metadata={"wire_name": "trialDays", "required": True})
    included_balance: int | None = field(
        default=None, metadata={"wire_name": "includedBalance", "required": True}
    )
    included_credits: int | None = field(
        default=None, metadata={"wire_name": "includedCredits", "required": True}
    )
    offer_id: str | None = field(default=None, metadata={"wire_name": "offerId", "required": True})
    inherits_from_price_id: str | None = field(
        default=None, metadata={"wire_name": "inheritsFromPriceId", "required": True}
    )
    metadata: dict[str, Any] = field(
        default_factory=dict, metadata={"wire_name": "metadata", "required": True}
    )
    market_prices: list[PlanPricesItemMarketPricesItem] = field(
        default_factory=list, metadata={"wire_name": "marketPrices", "required": True}
    )
    regional_prices: list[PlanPricesItemRegionalPricesItem] = field(
        default_factory=list, metadata={"wire_name": "regionalPrices", "required": True}
    )


@dataclass
class PlanPricesItemMarketPricesItem:
    market_group_id: str = field(
        default="", metadata={"wire_name": "marketGroupId", "required": True}
    )
    currency: str = field(default="", metadata={"wire_name": "currency", "required": True})
    price: int = field(default=0, metadata={"wire_name": "price", "required": True})


@dataclass
class PlanPricesItemRegionalPricesItem:
    currency: str = field(default="", metadata={"wire_name": "currency", "required": True})
    price: int = field(default=0, metadata={"wire_name": "price", "required": True})
    included_balance: int | None = field(
        default=None, metadata={"wire_name": "includedBalance", "required": True}
    )
    auto_synced: bool = field(default=False, metadata={"wire_name": "autoSynced", "required": True})


@dataclass
class PlanRegionalPricing:
    price_id: str = field(default="", metadata={"wire_name": "priceId", "required": True})
    overrides: list[PlanRegionalPricingOverridesItem] = field(
        default_factory=list, metadata={"wire_name": "overrides", "required": True}
    )
    object: Literal["plan_regional_pricing"] | None = field(
        default=None, metadata={"wire_name": "object", "required": True}
    )
    livemode: bool = field(default=False, metadata={"wire_name": "livemode", "required": True})


@dataclass
class PlanRegionalPricingOverridesItem:
    currency: str = field(default="", metadata={"wire_name": "currency", "required": True})
    price: int = field(default=0, metadata={"wire_name": "price", "required": True})
    included_balance: int | None = field(
        default=None, metadata={"wire_name": "includedBalance", "required": False}
    )


@dataclass
class PlanRegionalPricingResult:
    plan_id: str = field(default="", metadata={"wire_name": "planId", "required": True})
    currency: str = field(default="", metadata={"wire_name": "currency", "required": True})
    exchange_rate: float = field(
        default=0.0, metadata={"wire_name": "exchangeRate", "required": True}
    )
    prices_configured: int = field(
        default=0, metadata={"wire_name": "pricesConfigured", "required": True}
    )
    features_configured: int = field(
        default=0, metadata={"wire_name": "featuresConfigured", "required": True}
    )
    object: Literal["plan_regional_pricing"] | None = field(
        default=None, metadata={"wire_name": "object", "required": True}
    )
    livemode: bool = field(default=False, metadata={"wire_name": "livemode", "required": True})


@dataclass
class PlansListResult:
    object: Literal["list"] | None = field(
        default=None, metadata={"wire_name": "object", "required": True}
    )
    data: list[Plan] = field(default_factory=list, metadata={"wire_name": "data", "required": True})
    has_more: bool = field(default=False, metadata={"wire_name": "hasMore", "required": True})
    next_cursor: str | None = field(
        default=None, metadata={"wire_name": "nextCursor", "required": False}
    )


@dataclass
class PortalAccess:
    portal_url: str = field(default="", metadata={"wire_name": "portalUrl", "required": True})
    object: Literal["portal_session"] | None = field(
        default=None, metadata={"wire_name": "object", "required": True}
    )
    livemode: bool = field(default=False, metadata={"wire_name": "livemode", "required": True})


@dataclass
class PreviewChange:
    currency: str = field(default="", metadata={"wire_name": "currency", "required": True})
    current_plan_credit: int = field(
        default=0, metadata={"wire_name": "currentPlanCredit", "required": True}
    )
    new_plan_charge: int = field(
        default=0, metadata={"wire_name": "newPlanCharge", "required": True}
    )
    estimated_total: int = field(
        default=0, metadata={"wire_name": "estimatedTotal", "required": True}
    )
    effective_date: str = field(
        default="", metadata={"wire_name": "effectiveDate", "required": True}
    )
    days_remaining: int = field(
        default=0, metadata={"wire_name": "daysRemaining", "required": True}
    )
    total_days: int = field(default=0, metadata={"wire_name": "totalDays", "required": True})
    is_upgrade: bool = field(default=False, metadata={"wire_name": "isUpgrade", "required": True})
    offer_application: PreviewChangeOfferApplication | None = field(
        default=None, metadata={"wire_name": "offerApplication", "required": False}
    )
    object: Literal["plan_change_preview"] | None = field(
        default=None, metadata={"wire_name": "object", "required": True}
    )
    livemode: bool = field(default=False, metadata={"wire_name": "livemode", "required": True})


@dataclass
class PreviewChangeOfferApplication:
    id: str = field(default="", metadata={"wire_name": "id", "required": True})
    offer_id: str = field(default="", metadata={"wire_name": "offerId", "required": True})
    name: str = field(default="", metadata={"wire_name": "name", "required": True})
    currency: str = field(default="", metadata={"wire_name": "currency", "required": True})
    subtotal: int = field(default=0, metadata={"wire_name": "subtotal", "required": True})
    discount_amount: int = field(
        default=0, metadata={"wire_name": "discountAmount", "required": True}
    )
    total: int = field(default=0, metadata={"wire_name": "total", "required": True})
    phases: list[PreviewChangeOfferApplicationPhasesItem] = field(
        default_factory=list, metadata={"wire_name": "phases", "required": True}
    )
    applies_to: PreviewChangeOfferApplicationAppliesTo | None = field(
        default=None, metadata={"wire_name": "appliesTo", "required": True}
    )


@dataclass
class PreviewChangeOfferApplicationAppliesToVariant1:
    type: Literal["plan_price"] | None = field(
        default=None, metadata={"wire_name": "type", "required": True}
    )
    id: str = field(default="", metadata={"wire_name": "id", "required": True})


@dataclass
class PreviewChangeOfferApplicationAppliesToVariant2:
    type: Literal["addon"] | None = field(
        default=None, metadata={"wire_name": "type", "required": True}
    )
    id: str = field(default="", metadata={"wire_name": "id", "required": True})


@dataclass
class PreviewChangeOfferApplicationAppliesToVariant3:
    type: Literal["credit_pack"] | None = field(
        default=None, metadata={"wire_name": "type", "required": True}
    )
    id: str = field(default="", metadata={"wire_name": "id", "required": True})


@dataclass
class PreviewChangeOfferApplicationPhasesItemVariant1:
    type: Literal["free_trial"] | None = field(
        default=None, metadata={"wire_name": "type", "required": True}
    )
    duration_days: int = field(default=0, metadata={"wire_name": "durationDays", "required": True})
    starts_at: str | None = field(
        default=None, metadata={"wire_name": "startsAt", "required": True}
    )
    ends_at: str | None = field(default=None, metadata={"wire_name": "endsAt", "required": True})


@dataclass
class PreviewChangeOfferApplicationPhasesItemVariant2:
    type: Literal["percentage"] | None = field(
        default=None, metadata={"wire_name": "type", "required": True}
    )
    duration_cycles: int | None = field(
        default=None, metadata={"wire_name": "durationCycles", "required": True}
    )
    duration_interval: Literal["weekly", "monthly", "quarterly", "yearly"] | None = field(
        default=None, metadata={"wire_name": "durationInterval", "required": True}
    )
    starts_at: str | None = field(
        default=None, metadata={"wire_name": "startsAt", "required": True}
    )
    ends_at: str | None = field(default=None, metadata={"wire_name": "endsAt", "required": True})
    percentage: int = field(default=0, metadata={"wire_name": "percentage", "required": True})


@dataclass
class PreviewChangeOfferApplicationPhasesItemVariant3:
    type: Literal["amount_off"] | None = field(
        default=None, metadata={"wire_name": "type", "required": True}
    )
    duration_cycles: int | None = field(
        default=None, metadata={"wire_name": "durationCycles", "required": True}
    )
    duration_interval: Literal["weekly", "monthly", "quarterly", "yearly"] | None = field(
        default=None, metadata={"wire_name": "durationInterval", "required": True}
    )
    starts_at: str | None = field(
        default=None, metadata={"wire_name": "startsAt", "required": True}
    )
    ends_at: str | None = field(default=None, metadata={"wire_name": "endsAt", "required": True})
    amount: int = field(default=0, metadata={"wire_name": "amount", "required": True})


@dataclass
class PreviewChangeOfferApplicationPhasesItemVariant4:
    type: Literal["fixed_price"] | None = field(
        default=None, metadata={"wire_name": "type", "required": True}
    )
    duration_cycles: int | None = field(
        default=None, metadata={"wire_name": "durationCycles", "required": True}
    )
    duration_interval: Literal["weekly", "monthly", "quarterly", "yearly"] | None = field(
        default=None, metadata={"wire_name": "durationInterval", "required": True}
    )
    starts_at: str | None = field(
        default=None, metadata={"wire_name": "startsAt", "required": True}
    )
    ends_at: str | None = field(default=None, metadata={"wire_name": "endsAt", "required": True})
    price: int = field(default=0, metadata={"wire_name": "price", "required": True})


@dataclass
class PromoCode:
    id: str = field(default="", metadata={"wire_name": "id", "required": True})
    code: str = field(default="", metadata={"wire_name": "code", "required": True})
    offer_id: str = field(default="", metadata={"wire_name": "offerId", "required": True})
    billing_interval: BillingInterval | None = field(
        default=None, metadata={"wire_name": "billingInterval", "required": True}
    )
    max_redemptions: int | None = field(
        default=None, metadata={"wire_name": "maxRedemptions", "required": True}
    )
    expires_at: str | None = field(
        default=None, metadata={"wire_name": "expiresAt", "required": True}
    )
    is_active: bool = field(default=False, metadata={"wire_name": "isActive", "required": True})
    redemption_count: int = field(
        default=0, metadata={"wire_name": "redemptionCount", "required": True}
    )
    created_at: str = field(default="", metadata={"wire_name": "createdAt", "required": True})
    updated_at: str = field(default="", metadata={"wire_name": "updatedAt", "required": True})
    object: Literal["promo_code"] | None = field(
        default=None, metadata={"wire_name": "object", "required": True}
    )
    livemode: bool = field(default=False, metadata={"wire_name": "livemode", "required": True})


@dataclass
class PromoCodesListResult:
    object: Literal["list"] | None = field(
        default=None, metadata={"wire_name": "object", "required": True}
    )
    data: list[PromoCode] = field(
        default_factory=list, metadata={"wire_name": "data", "required": True}
    )
    has_more: bool = field(default=False, metadata={"wire_name": "hasMore", "required": True})
    next_cursor: str | None = field(
        default=None, metadata={"wire_name": "nextCursor", "required": False}
    )


@dataclass
class QuotaGetAllResult:
    object: Literal["list"] | None = field(
        default=None, metadata={"wire_name": "object", "required": True}
    )
    data: list[UsageQuota] = field(
        default_factory=list, metadata={"wire_name": "data", "required": True}
    )
    has_more: bool = field(default=False, metadata={"wire_name": "hasMore", "required": True})
    next_cursor: str | None = field(
        default=None, metadata={"wire_name": "nextCursor", "required": False}
    )


@dataclass
class ReactivatedSubscription:
    subscription_id: str = field(
        default="", metadata={"wire_name": "subscriptionId", "required": True}
    )
    invoice_id: str = field(default="", metadata={"wire_name": "invoiceId", "required": True})
    status: Literal["processing", "succeeded"] | None = field(
        default=None, metadata={"wire_name": "status", "required": True}
    )
    offer_application: ReactivatedSubscriptionOfferApplication | None = field(
        default=None, metadata={"wire_name": "offerApplication", "required": False}
    )
    object: Literal["subscription_reactivation"] | None = field(
        default=None, metadata={"wire_name": "object", "required": True}
    )
    livemode: bool = field(default=False, metadata={"wire_name": "livemode", "required": True})


@dataclass
class ReactivatedSubscriptionOfferApplication:
    id: str = field(default="", metadata={"wire_name": "id", "required": True})
    offer_id: str = field(default="", metadata={"wire_name": "offerId", "required": True})
    name: str = field(default="", metadata={"wire_name": "name", "required": True})
    currency: str = field(default="", metadata={"wire_name": "currency", "required": True})
    subtotal: int = field(default=0, metadata={"wire_name": "subtotal", "required": True})
    discount_amount: int = field(
        default=0, metadata={"wire_name": "discountAmount", "required": True}
    )
    total: int = field(default=0, metadata={"wire_name": "total", "required": True})
    phases: list[ReactivatedSubscriptionOfferApplicationPhasesItem] = field(
        default_factory=list, metadata={"wire_name": "phases", "required": True}
    )
    applies_to: ReactivatedSubscriptionOfferApplicationAppliesTo | None = field(
        default=None, metadata={"wire_name": "appliesTo", "required": True}
    )


@dataclass
class ReactivatedSubscriptionOfferApplicationAppliesToVariant1:
    type: Literal["plan_price"] | None = field(
        default=None, metadata={"wire_name": "type", "required": True}
    )
    id: str = field(default="", metadata={"wire_name": "id", "required": True})


@dataclass
class ReactivatedSubscriptionOfferApplicationAppliesToVariant2:
    type: Literal["addon"] | None = field(
        default=None, metadata={"wire_name": "type", "required": True}
    )
    id: str = field(default="", metadata={"wire_name": "id", "required": True})


@dataclass
class ReactivatedSubscriptionOfferApplicationAppliesToVariant3:
    type: Literal["credit_pack"] | None = field(
        default=None, metadata={"wire_name": "type", "required": True}
    )
    id: str = field(default="", metadata={"wire_name": "id", "required": True})


@dataclass
class ReactivatedSubscriptionOfferApplicationPhasesItemVariant1:
    type: Literal["free_trial"] | None = field(
        default=None, metadata={"wire_name": "type", "required": True}
    )
    duration_days: int = field(default=0, metadata={"wire_name": "durationDays", "required": True})
    starts_at: str | None = field(
        default=None, metadata={"wire_name": "startsAt", "required": True}
    )
    ends_at: str | None = field(default=None, metadata={"wire_name": "endsAt", "required": True})


@dataclass
class ReactivatedSubscriptionOfferApplicationPhasesItemVariant2:
    type: Literal["percentage"] | None = field(
        default=None, metadata={"wire_name": "type", "required": True}
    )
    duration_cycles: int | None = field(
        default=None, metadata={"wire_name": "durationCycles", "required": True}
    )
    duration_interval: Literal["weekly", "monthly", "quarterly", "yearly"] | None = field(
        default=None, metadata={"wire_name": "durationInterval", "required": True}
    )
    starts_at: str | None = field(
        default=None, metadata={"wire_name": "startsAt", "required": True}
    )
    ends_at: str | None = field(default=None, metadata={"wire_name": "endsAt", "required": True})
    percentage: int = field(default=0, metadata={"wire_name": "percentage", "required": True})


@dataclass
class ReactivatedSubscriptionOfferApplicationPhasesItemVariant3:
    type: Literal["amount_off"] | None = field(
        default=None, metadata={"wire_name": "type", "required": True}
    )
    duration_cycles: int | None = field(
        default=None, metadata={"wire_name": "durationCycles", "required": True}
    )
    duration_interval: Literal["weekly", "monthly", "quarterly", "yearly"] | None = field(
        default=None, metadata={"wire_name": "durationInterval", "required": True}
    )
    starts_at: str | None = field(
        default=None, metadata={"wire_name": "startsAt", "required": True}
    )
    ends_at: str | None = field(default=None, metadata={"wire_name": "endsAt", "required": True})
    amount: int = field(default=0, metadata={"wire_name": "amount", "required": True})


@dataclass
class ReactivatedSubscriptionOfferApplicationPhasesItemVariant4:
    type: Literal["fixed_price"] | None = field(
        default=None, metadata={"wire_name": "type", "required": True}
    )
    duration_cycles: int | None = field(
        default=None, metadata={"wire_name": "durationCycles", "required": True}
    )
    duration_interval: Literal["weekly", "monthly", "quarterly", "yearly"] | None = field(
        default=None, metadata={"wire_name": "durationInterval", "required": True}
    )
    starts_at: str | None = field(
        default=None, metadata={"wire_name": "startsAt", "required": True}
    )
    ends_at: str | None = field(default=None, metadata={"wire_name": "endsAt", "required": True})
    price: int = field(default=0, metadata={"wire_name": "price", "required": True})


@dataclass
class RecoveryLink:
    url: str = field(default="", metadata={"wire_name": "url", "required": True})
    token: str = field(default="", metadata={"wire_name": "token", "required": True})
    object: Literal["recovery_link"] | None = field(
        default=None, metadata={"wire_name": "object", "required": True}
    )
    livemode: bool = field(default=False, metadata={"wire_name": "livemode", "required": True})


@dataclass
class Refund:
    id: str = field(default="", metadata={"wire_name": "id", "required": True})
    transaction_id: str = field(
        default="", metadata={"wire_name": "transactionId", "required": True}
    )
    amount: int = field(default=0, metadata={"wire_name": "amount", "required": True})
    currency: str = field(default="", metadata={"wire_name": "currency", "required": True})
    charge_id: str | None = field(
        default=None, metadata={"wire_name": "chargeId", "required": True}
    )
    status: Literal["pending", "requires_action", "succeeded", "failed", "canceled"] | None = field(
        default=None, metadata={"wire_name": "status", "required": True}
    )
    reason: Literal["duplicate", "fraudulent", "requested_by_customer"] | None = field(
        default=None, metadata={"wire_name": "reason", "required": True}
    )
    object: Literal["refund"] | None = field(
        default=None, metadata={"wire_name": "object", "required": True}
    )
    livemode: bool = field(default=False, metadata={"wire_name": "livemode", "required": True})


@dataclass
class RemovedPlanFeature:
    id: str = field(default="", metadata={"wire_name": "id", "required": True})
    removed: Literal[True] | None = field(
        default=None, metadata={"wire_name": "removed", "required": True}
    )
    object: Literal["plan_feature"] | None = field(
        default=None, metadata={"wire_name": "object", "required": True}
    )
    livemode: bool = field(default=False, metadata={"wire_name": "livemode", "required": True})


@dataclass
class RemovedPlanFromGroup:
    id: str = field(default="", metadata={"wire_name": "id", "required": True})
    removed: bool = field(default=False, metadata={"wire_name": "removed", "required": True})
    object: Literal["plan_group_membership"] | None = field(
        default=None, metadata={"wire_name": "object", "required": True}
    )
    livemode: bool = field(default=False, metadata={"wire_name": "livemode", "required": True})


@dataclass
class ReorderedPlans:
    reordered: bool = field(default=False, metadata={"wire_name": "reordered", "required": True})
    object: Literal["plan_group_order"] | None = field(
        default=None, metadata={"wire_name": "object", "required": True}
    )
    livemode: bool = field(default=False, metadata={"wire_name": "livemode", "required": True})


@dataclass
class SeatBalance:
    current: int = field(default=0, metadata={"wire_name": "current", "required": True})
    as_of: str = field(default="", metadata={"wire_name": "asOf", "required": True})
    object: Literal["seat_balance"] | None = field(
        default=None, metadata={"wire_name": "object", "required": True}
    )
    livemode: bool = field(default=False, metadata={"wire_name": "livemode", "required": True})


@dataclass
class SeatBalanceCollection:
    balances: dict[str, SeatBalanceCollectionBalancesValue] = field(
        default_factory=dict, metadata={"wire_name": "balances", "required": True}
    )
    object: Literal["seat_balance_collection"] | None = field(
        default=None, metadata={"wire_name": "object", "required": True}
    )
    livemode: bool = field(default=False, metadata={"wire_name": "livemode", "required": True})


@dataclass
class SeatBalanceCollectionBalancesValue:
    current: int = field(default=0, metadata={"wire_name": "current", "required": True})
    as_of: str = field(default="", metadata={"wire_name": "asOf", "required": True})


@dataclass
class SeatEvent:
    id: str = field(default="", metadata={"wire_name": "id", "required": True})
    customer_id: str = field(default="", metadata={"wire_name": "customerId", "required": True})
    feature_code: str = field(default="", metadata={"wire_name": "featureCode", "required": True})
    previous_balance: int = field(
        default=0, metadata={"wire_name": "previousBalance", "required": True}
    )
    new_balance: int = field(default=0, metadata={"wire_name": "newBalance", "required": True})
    ts: str = field(default="", metadata={"wire_name": "ts", "required": True})
    created_at: str = field(default="", metadata={"wire_name": "createdAt", "required": True})
    object: Literal["seat_event"] | None = field(
        default=None, metadata={"wire_name": "object", "required": True}
    )
    livemode: bool = field(default=False, metadata={"wire_name": "livemode", "required": True})


@dataclass
class SeatsSetAllResult:
    object: Literal["list"] | None = field(
        default=None, metadata={"wire_name": "object", "required": True}
    )
    data: list[SeatEvent] = field(
        default_factory=list, metadata={"wire_name": "data", "required": True}
    )
    has_more: bool = field(default=False, metadata={"wire_name": "hasMore", "required": True})
    next_cursor: str | None = field(
        default=None, metadata={"wire_name": "nextCursor", "required": False}
    )


@dataclass
class SentInvoice:
    sent: bool = field(default=False, metadata={"wire_name": "sent", "required": True})
    sent_at: str = field(default="", metadata={"wire_name": "sentAt", "required": True})
    object: Literal["invoice_delivery"] | None = field(
        default=None, metadata={"wire_name": "object", "required": True}
    )
    livemode: bool = field(default=False, metadata={"wire_name": "livemode", "required": True})


@dataclass
class SetPlanRegionalPricingParamsFeaturesItem:
    feature_id: str = field(default="", metadata={"wire_name": "featureId", "required": True})
    overage_unit_price: int = field(
        default=0, metadata={"wire_name": "overageUnitPrice", "required": True}
    )


@dataclass
class SetPlanRegionalPricingParamsPricesItem:
    price_id: str = field(default="", metadata={"wire_name": "priceId", "required": True})
    price: int = field(default=0, metadata={"wire_name": "price", "required": True})
    included_balance: int | None = field(
        default=None, metadata={"wire_name": "includedBalance", "required": False}
    )


@dataclass
class Subscription:
    id: str = field(default="", metadata={"wire_name": "id", "required": True})
    customer_id: str = field(default="", metadata={"wire_name": "customerId", "required": True})
    plan: SubscriptionPlan | None = field(
        default=None, metadata={"wire_name": "plan", "required": True}
    )
    name: str = field(default="", metadata={"wire_name": "name", "required": True})
    description: str | None = field(
        default=None, metadata={"wire_name": "description", "required": True}
    )
    status: SubscriptionStatus | None = field(
        default=None, metadata={"wire_name": "status", "required": True}
    )
    billing_interval: BillingInterval | None = field(
        default=None, metadata={"wire_name": "billingInterval", "required": True}
    )
    trial_ends_at: str | None = field(
        default=None, metadata={"wire_name": "trialEndsAt", "required": True}
    )
    current_period: SubscriptionCurrentPeriod | None = field(
        default=None, metadata={"wire_name": "currentPeriod", "required": True}
    )
    cancellation: SubscriptionCancellation | None = field(
        default=None, metadata={"wire_name": "cancellation", "required": True}
    )
    cancel_at_period_end: bool = field(
        default=False, metadata={"wire_name": "cancelAtPeriodEnd", "required": True}
    )
    scheduled_plan_change: SubscriptionScheduledPlanChange | None = field(
        default=None, metadata={"wire_name": "scheduledPlanChange", "required": True}
    )
    start_date: str = field(default="", metadata={"wire_name": "startDate", "required": True})
    end_date: str | None = field(default=None, metadata={"wire_name": "endDate", "required": True})
    billing_day_of_month: int | None = field(
        default=None, metadata={"wire_name": "billingDayOfMonth", "required": True}
    )
    next_billing_date: str | None = field(
        default=None, metadata={"wire_name": "nextBillingDate", "required": True}
    )
    checkout_url: str | None = field(
        default=None, metadata={"wire_name": "checkoutUrl", "required": True}
    )
    created_at: str = field(default="", metadata={"wire_name": "createdAt", "required": True})
    updated_at: str = field(default="", metadata={"wire_name": "updatedAt", "required": True})
    offer_applications: list[SubscriptionOfferApplication] = field(
        default_factory=list, metadata={"wire_name": "offerApplications", "required": True}
    )
    pause: SubscriptionPause | None = field(
        default=None, metadata={"wire_name": "pause", "required": True}
    )
    plan_grant: SubscriptionPlanGrant | None = field(
        default=None, metadata={"wire_name": "planGrant", "required": False}
    )
    consumption_model: ConsumptionModel | None = field(
        default=None, metadata={"wire_name": "consumptionModel", "required": True}
    )
    features: list[SubscriptionFeaturesItem] = field(
        default_factory=list, metadata={"wire_name": "features", "required": True}
    )
    credits: SubscriptionCredits | None = field(
        default=None, metadata={"wire_name": "credits", "required": True}
    )
    balance: SubscriptionBalance | None = field(
        default=None, metadata={"wire_name": "balance", "required": True}
    )
    price_id: str | None = field(default=None, metadata={"wire_name": "priceId", "required": True})
    object: Literal["subscription"] | None = field(
        default=None, metadata={"wire_name": "object", "required": True}
    )
    livemode: bool = field(default=False, metadata={"wire_name": "livemode", "required": True})


@dataclass
class SubscriptionAddon:
    addon_id: str = field(default="", metadata={"wire_name": "addonId", "required": True})
    status: Literal["active"] | None = field(
        default=None, metadata={"wire_name": "status", "required": True}
    )
    prorated_charge: int = field(
        default=0, metadata={"wire_name": "proratedCharge", "required": True}
    )
    object: Literal["subscription_addon"] | None = field(
        default=None, metadata={"wire_name": "object", "required": True}
    )
    livemode: bool = field(default=False, metadata={"wire_name": "livemode", "required": True})


@dataclass
class SubscriptionBalance:
    remaining: float = field(default=0.0, metadata={"wire_name": "remaining", "required": True})
    included: float = field(default=0.0, metadata={"wire_name": "included", "required": True})
    currency: str = field(default="", metadata={"wire_name": "currency", "required": True})


@dataclass
class SubscriptionCancellation:
    scheduled_at: str = field(default="", metadata={"wire_name": "scheduledAt", "required": True})
    reason: str | None = field(default=None, metadata={"wire_name": "reason", "required": True})
    effective_at: str = field(default="", metadata={"wire_name": "effectiveAt", "required": True})


@dataclass
class SubscriptionCredits:
    remaining: float = field(default=0.0, metadata={"wire_name": "remaining", "required": True})
    included: float = field(default=0.0, metadata={"wire_name": "included", "required": True})
    purchased: float = field(default=0.0, metadata={"wire_name": "purchased", "required": True})


@dataclass
class SubscriptionCurrentPeriod:
    start: str = field(default="", metadata={"wire_name": "start", "required": True})
    end: str = field(default="", metadata={"wire_name": "end", "required": True})
    days_remaining: float = field(
        default=0.0, metadata={"wire_name": "daysRemaining", "required": True}
    )


@dataclass
class SubscriptionFeaturesItemVariant1:
    code: str = field(default="", metadata={"wire_name": "code", "required": True})
    name: str = field(default="", metadata={"wire_name": "name", "required": True})
    type: Literal["boolean"] | None = field(
        default=None, metadata={"wire_name": "type", "required": True}
    )
    enabled: bool = field(default=False, metadata={"wire_name": "enabled", "required": True})
    base_access: SubscriptionFeaturesItemVariant1BaseAccess | None = field(
        default=None, metadata={"wire_name": "baseAccess", "required": False}
    )


@dataclass
class SubscriptionFeaturesItemVariant1BaseAccess:
    enabled: bool = field(default=False, metadata={"wire_name": "enabled", "required": True})


@dataclass
class SubscriptionFeaturesItemVariant2:
    code: str = field(default="", metadata={"wire_name": "code", "required": True})
    name: str = field(default="", metadata={"wire_name": "name", "required": True})
    type: Literal["usage"] | None = field(
        default=None, metadata={"wire_name": "type", "required": True}
    )
    usage: SubscriptionFeaturesItemVariant2Usage | None = field(
        default=None, metadata={"wire_name": "usage", "required": False}
    )
    base_access: SubscriptionFeaturesItemVariant2BaseAccess | None = field(
        default=None, metadata={"wire_name": "baseAccess", "required": False}
    )


@dataclass
class SubscriptionFeaturesItemVariant2BaseAccess:
    included: float = field(default=0.0, metadata={"wire_name": "included", "required": True})
    unlimited: bool = field(default=False, metadata={"wire_name": "unlimited", "required": True})


@dataclass
class SubscriptionFeaturesItemVariant2Usage:
    current: float = field(default=0.0, metadata={"wire_name": "current", "required": True})
    included: float = field(default=0.0, metadata={"wire_name": "included", "required": True})
    overage_quantity: float = field(
        default=0.0, metadata={"wire_name": "overageQuantity", "required": True}
    )
    overage_unit_price: float | None = field(
        default=None, metadata={"wire_name": "overageUnitPrice", "required": False}
    )
    unlimited: bool | None = field(
        default=None, metadata={"wire_name": "unlimited", "required": False}
    )


@dataclass
class SubscriptionFeaturesItemVariant3:
    code: str = field(default="", metadata={"wire_name": "code", "required": True})
    name: str = field(default="", metadata={"wire_name": "name", "required": True})
    type: Literal["seats"] | None = field(
        default=None, metadata={"wire_name": "type", "required": True}
    )
    usage: SubscriptionFeaturesItemVariant3Usage | None = field(
        default=None, metadata={"wire_name": "usage", "required": True}
    )
    base_access: SubscriptionFeaturesItemVariant3BaseAccess | None = field(
        default=None, metadata={"wire_name": "baseAccess", "required": False}
    )


@dataclass
class SubscriptionFeaturesItemVariant3BaseAccess:
    included: float = field(default=0.0, metadata={"wire_name": "included", "required": True})
    unlimited: bool = field(default=False, metadata={"wire_name": "unlimited", "required": True})


@dataclass
class SubscriptionFeaturesItemVariant3Usage:
    current: float = field(default=0.0, metadata={"wire_name": "current", "required": True})
    included: float = field(default=0.0, metadata={"wire_name": "included", "required": True})
    overage_quantity: float = field(
        default=0.0, metadata={"wire_name": "overageQuantity", "required": True}
    )
    overage_unit_price: float | None = field(
        default=None, metadata={"wire_name": "overageUnitPrice", "required": False}
    )
    unlimited: bool | None = field(
        default=None, metadata={"wire_name": "unlimited", "required": False}
    )


@dataclass
class SubscriptionFeaturesItemVariant4:
    code: str = field(default="", metadata={"wire_name": "code", "required": True})
    name: str = field(default="", metadata={"wire_name": "name", "required": True})
    type: Literal["quota"] | None = field(
        default=None, metadata={"wire_name": "type", "required": True}
    )
    usage: SubscriptionFeaturesItemVariant4Usage | None = field(
        default=None, metadata={"wire_name": "usage", "required": False}
    )
    base_access: SubscriptionFeaturesItemVariant4BaseAccess | None = field(
        default=None, metadata={"wire_name": "baseAccess", "required": False}
    )


@dataclass
class SubscriptionFeaturesItemVariant4BaseAccess:
    included: float = field(default=0.0, metadata={"wire_name": "included", "required": True})
    unlimited: bool = field(default=False, metadata={"wire_name": "unlimited", "required": True})


@dataclass
class SubscriptionFeaturesItemVariant4Usage:
    current: float = field(default=0.0, metadata={"wire_name": "current", "required": True})
    included: float = field(default=0.0, metadata={"wire_name": "included", "required": True})
    overage_quantity: float = field(
        default=0.0, metadata={"wire_name": "overageQuantity", "required": True}
    )
    overage_unit_price: float | None = field(
        default=None, metadata={"wire_name": "overageUnitPrice", "required": False}
    )
    unlimited: bool | None = field(
        default=None, metadata={"wire_name": "unlimited", "required": False}
    )


@dataclass
class SubscriptionOfferApplication:
    id: str = field(default="", metadata={"wire_name": "id", "required": True})
    name: str = field(default="", metadata={"wire_name": "name", "required": True})
    applies_to: SubscriptionOfferApplicationAppliesTo | None = field(
        default=None, metadata={"wire_name": "appliesTo", "required": True}
    )
    offer_id: str | None = field(default=None, metadata={"wire_name": "offerId", "required": True})
    source: Literal["direct", "introductory", "promo_code", "card_promotion", "custom"] | None = (
        field(default=None, metadata={"wire_name": "source", "required": True})
    )
    status: Literal["quoted", "applied", "failed", "expired"] | None = field(
        default=None, metadata={"wire_name": "status", "required": True}
    )
    currency: str | None = field(default=None, metadata={"wire_name": "currency", "required": True})
    subtotal: int | None = field(default=None, metadata={"wire_name": "subtotal", "required": True})
    discount_amount: int | None = field(
        default=None, metadata={"wire_name": "discountAmount", "required": True}
    )
    total: int | None = field(default=None, metadata={"wire_name": "total", "required": True})
    phases: list[SubscriptionOfferApplicationPhase] = field(
        default_factory=list, metadata={"wire_name": "phases", "required": True}
    )
    quoted_at: str = field(default="", metadata={"wire_name": "quotedAt", "required": True})
    expires_at: str | None = field(
        default=None, metadata={"wire_name": "expiresAt", "required": True}
    )
    applied_at: str | None = field(
        default=None, metadata={"wire_name": "appliedAt", "required": True}
    )


@dataclass
class SubscriptionOfferApplicationAppliesToVariant1:
    type: Literal["plan_price"] | None = field(
        default=None, metadata={"wire_name": "type", "required": True}
    )
    id: str = field(default="", metadata={"wire_name": "id", "required": True})


@dataclass
class SubscriptionOfferApplicationAppliesToVariant2:
    type: Literal["addon"] | None = field(
        default=None, metadata={"wire_name": "type", "required": True}
    )
    id: str = field(default="", metadata={"wire_name": "id", "required": True})


@dataclass
class SubscriptionOfferApplicationAppliesToVariant3:
    type: Literal["credit_pack"] | None = field(
        default=None, metadata={"wire_name": "type", "required": True}
    )
    id: str = field(default="", metadata={"wire_name": "id", "required": True})


@dataclass
class SubscriptionOfferApplicationPhaseVariant1:
    type: Literal["free_trial"] | None = field(
        default=None, metadata={"wire_name": "type", "required": True}
    )
    duration_days: int = field(default=0, metadata={"wire_name": "durationDays", "required": True})
    duration_interval: Literal["weekly", "monthly", "quarterly", "yearly"] | None = field(
        default=None, metadata={"wire_name": "durationInterval", "required": True}
    )
    starts_at: str | None = field(
        default=None, metadata={"wire_name": "startsAt", "required": True}
    )
    ends_at: str | None = field(default=None, metadata={"wire_name": "endsAt", "required": True})


@dataclass
class SubscriptionOfferApplicationPhaseVariant2:
    type: Literal["percentage"] | None = field(
        default=None, metadata={"wire_name": "type", "required": True}
    )
    duration_cycles: int | None = field(
        default=None, metadata={"wire_name": "durationCycles", "required": True}
    )
    duration_interval: Literal["weekly", "monthly", "quarterly", "yearly"] | None = field(
        default=None, metadata={"wire_name": "durationInterval", "required": True}
    )
    percentage: int = field(default=0, metadata={"wire_name": "percentage", "required": True})
    starts_at: str | None = field(
        default=None, metadata={"wire_name": "startsAt", "required": True}
    )
    ends_at: str | None = field(default=None, metadata={"wire_name": "endsAt", "required": True})


@dataclass
class SubscriptionOfferApplicationPhaseVariant3:
    type: Literal["amount_off"] | None = field(
        default=None, metadata={"wire_name": "type", "required": True}
    )
    duration_cycles: int | None = field(
        default=None, metadata={"wire_name": "durationCycles", "required": True}
    )
    duration_interval: Literal["weekly", "monthly", "quarterly", "yearly"] | None = field(
        default=None, metadata={"wire_name": "durationInterval", "required": True}
    )
    amount: int = field(default=0, metadata={"wire_name": "amount", "required": True})
    starts_at: str | None = field(
        default=None, metadata={"wire_name": "startsAt", "required": True}
    )
    ends_at: str | None = field(default=None, metadata={"wire_name": "endsAt", "required": True})


@dataclass
class SubscriptionOfferApplicationPhaseVariant4:
    type: Literal["fixed_price"] | None = field(
        default=None, metadata={"wire_name": "type", "required": True}
    )
    duration_cycles: int | None = field(
        default=None, metadata={"wire_name": "durationCycles", "required": True}
    )
    duration_interval: Literal["weekly", "monthly", "quarterly", "yearly"] | None = field(
        default=None, metadata={"wire_name": "durationInterval", "required": True}
    )
    price: int = field(default=0, metadata={"wire_name": "price", "required": True})
    starts_at: str | None = field(
        default=None, metadata={"wire_name": "startsAt", "required": True}
    )
    ends_at: str | None = field(default=None, metadata={"wire_name": "endsAt", "required": True})


@dataclass
class SubscriptionPauseVariant1:
    status: Literal["scheduled"] | None = field(
        default=None, metadata={"wire_name": "status", "required": True}
    )
    mode: Literal["period_end"] | None = field(
        default=None, metadata={"wire_name": "mode", "required": True}
    )
    requested_at: str = field(default="", metadata={"wire_name": "requestedAt", "required": True})
    effective_at: str = field(default="", metadata={"wire_name": "effectiveAt", "required": True})
    resume_at: str | None = field(
        default=None, metadata={"wire_name": "resumeAt", "required": True}
    )


@dataclass
class SubscriptionPauseVariant2:
    status: Literal["active"] | None = field(
        default=None, metadata={"wire_name": "status", "required": True}
    )
    mode: Literal["immediate", "period_end"] | None = field(
        default=None, metadata={"wire_name": "mode", "required": True}
    )
    requested_at: str = field(default="", metadata={"wire_name": "requestedAt", "required": True})
    effective_at: str = field(default="", metadata={"wire_name": "effectiveAt", "required": True})
    resume_at: str | None = field(
        default=None, metadata={"wire_name": "resumeAt", "required": True}
    )


@dataclass
class SubscriptionPlan:
    id: str = field(default="", metadata={"wire_name": "id", "required": True})
    name: str = field(default="", metadata={"wire_name": "name", "required": True})
    base_price: float = field(default=0.0, metadata={"wire_name": "basePrice", "required": True})


@dataclass
class SubscriptionPlanGrant:
    id: str = field(default="", metadata={"wire_name": "id", "required": True})
    plan: SubscriptionPlanGrantPlan | None = field(
        default=None, metadata={"wire_name": "plan", "required": True}
    )
    expires_at: str | None = field(
        default=None, metadata={"wire_name": "expiresAt", "required": True}
    )


@dataclass
class SubscriptionPlanGrantPlan:
    id: str = field(default="", metadata={"wire_name": "id", "required": True})
    name: str = field(default="", metadata={"wire_name": "name", "required": True})


@dataclass
class SubscriptionResume:
    subscription_id: str = field(
        default="", metadata={"wire_name": "subscriptionId", "required": True}
    )
    invoice_id: str | None = field(
        default=None, metadata={"wire_name": "invoiceId", "required": True}
    )
    status: Literal["processing", "succeeded"] | None = field(
        default=None, metadata={"wire_name": "status", "required": True}
    )
    object: Literal["subscription_resume"] | None = field(
        default=None, metadata={"wire_name": "object", "required": True}
    )
    livemode: bool = field(default=False, metadata={"wire_name": "livemode", "required": True})


@dataclass
class SubscriptionScheduledPlanChange:
    change_type: Literal["plan_downgrade", "interval_change"] | None = field(
        default=None, metadata={"wire_name": "changeType", "required": True}
    )
    new_plan_id: str | None = field(
        default=None, metadata={"wire_name": "newPlanId", "required": True}
    )
    new_plan_name: str | None = field(
        default=None, metadata={"wire_name": "newPlanName", "required": True}
    )
    new_billing_interval: str | None = field(
        default=None, metadata={"wire_name": "newBillingInterval", "required": True}
    )
    scheduled_for: str = field(default="", metadata={"wire_name": "scheduledFor", "required": True})


@dataclass
class SubscriptionsListResult:
    object: Literal["list"] | None = field(
        default=None, metadata={"wire_name": "object", "required": True}
    )
    data: list[SubscriptionSummary] = field(
        default_factory=list, metadata={"wire_name": "data", "required": True}
    )
    has_more: bool = field(default=False, metadata={"wire_name": "hasMore", "required": True})
    next_cursor: str | None = field(
        default=None, metadata={"wire_name": "nextCursor", "required": False}
    )


@dataclass
class SubscriptionSummary:
    id: str = field(default="", metadata={"wire_name": "id", "required": True})
    customer_id: str = field(default="", metadata={"wire_name": "customerId", "required": True})
    plan: SubscriptionSummaryPlan | None = field(
        default=None, metadata={"wire_name": "plan", "required": True}
    )
    name: str = field(default="", metadata={"wire_name": "name", "required": True})
    description: str | None = field(
        default=None, metadata={"wire_name": "description", "required": True}
    )
    status: SubscriptionStatus | None = field(
        default=None, metadata={"wire_name": "status", "required": True}
    )
    billing_interval: BillingInterval | None = field(
        default=None, metadata={"wire_name": "billingInterval", "required": True}
    )
    trial_ends_at: str | None = field(
        default=None, metadata={"wire_name": "trialEndsAt", "required": True}
    )
    current_period: SubscriptionSummaryCurrentPeriod | None = field(
        default=None, metadata={"wire_name": "currentPeriod", "required": True}
    )
    cancellation: SubscriptionSummaryCancellation | None = field(
        default=None, metadata={"wire_name": "cancellation", "required": True}
    )
    cancel_at_period_end: bool = field(
        default=False, metadata={"wire_name": "cancelAtPeriodEnd", "required": True}
    )
    scheduled_plan_change: SubscriptionSummaryScheduledPlanChange | None = field(
        default=None, metadata={"wire_name": "scheduledPlanChange", "required": True}
    )
    start_date: str = field(default="", metadata={"wire_name": "startDate", "required": True})
    end_date: str | None = field(default=None, metadata={"wire_name": "endDate", "required": True})
    billing_day_of_month: int | None = field(
        default=None, metadata={"wire_name": "billingDayOfMonth", "required": True}
    )
    next_billing_date: str | None = field(
        default=None, metadata={"wire_name": "nextBillingDate", "required": True}
    )
    checkout_url: str | None = field(
        default=None, metadata={"wire_name": "checkoutUrl", "required": True}
    )
    created_at: str = field(default="", metadata={"wire_name": "createdAt", "required": True})
    updated_at: str = field(default="", metadata={"wire_name": "updatedAt", "required": True})
    offer_applications: list[SubscriptionOfferApplication] = field(
        default_factory=list, metadata={"wire_name": "offerApplications", "required": True}
    )
    pause: SubscriptionSummaryPause | None = field(
        default=None, metadata={"wire_name": "pause", "required": True}
    )
    price_id: str | None = field(default=None, metadata={"wire_name": "priceId", "required": True})
    object: Literal["subscription"] | None = field(
        default=None, metadata={"wire_name": "object", "required": True}
    )
    livemode: bool = field(default=False, metadata={"wire_name": "livemode", "required": True})


@dataclass
class SubscriptionSummaryCancellation:
    scheduled_at: str = field(default="", metadata={"wire_name": "scheduledAt", "required": True})
    reason: str | None = field(default=None, metadata={"wire_name": "reason", "required": True})
    effective_at: str = field(default="", metadata={"wire_name": "effectiveAt", "required": True})


@dataclass
class SubscriptionSummaryCurrentPeriod:
    start: str = field(default="", metadata={"wire_name": "start", "required": True})
    end: str = field(default="", metadata={"wire_name": "end", "required": True})
    days_remaining: float = field(
        default=0.0, metadata={"wire_name": "daysRemaining", "required": True}
    )


@dataclass
class SubscriptionSummaryPauseVariant1:
    status: Literal["scheduled"] | None = field(
        default=None, metadata={"wire_name": "status", "required": True}
    )
    mode: Literal["period_end"] | None = field(
        default=None, metadata={"wire_name": "mode", "required": True}
    )
    requested_at: str = field(default="", metadata={"wire_name": "requestedAt", "required": True})
    effective_at: str = field(default="", metadata={"wire_name": "effectiveAt", "required": True})
    resume_at: str | None = field(
        default=None, metadata={"wire_name": "resumeAt", "required": True}
    )


@dataclass
class SubscriptionSummaryPauseVariant2:
    status: Literal["active"] | None = field(
        default=None, metadata={"wire_name": "status", "required": True}
    )
    mode: Literal["immediate", "period_end"] | None = field(
        default=None, metadata={"wire_name": "mode", "required": True}
    )
    requested_at: str = field(default="", metadata={"wire_name": "requestedAt", "required": True})
    effective_at: str = field(default="", metadata={"wire_name": "effectiveAt", "required": True})
    resume_at: str | None = field(
        default=None, metadata={"wire_name": "resumeAt", "required": True}
    )


@dataclass
class SubscriptionSummaryPlan:
    id: str = field(default="", metadata={"wire_name": "id", "required": True})
    name: str = field(default="", metadata={"wire_name": "name", "required": True})


@dataclass
class SubscriptionSummaryScheduledPlanChange:
    change_type: Literal["plan_downgrade", "interval_change"] | None = field(
        default=None, metadata={"wire_name": "changeType", "required": True}
    )
    new_plan_id: str | None = field(
        default=None, metadata={"wire_name": "newPlanId", "required": True}
    )
    new_plan_name: str | None = field(
        default=None, metadata={"wire_name": "newPlanName", "required": True}
    )
    new_billing_interval: str | None = field(
        default=None, metadata={"wire_name": "newBillingInterval", "required": True}
    )
    scheduled_for: str = field(default="", metadata={"wire_name": "scheduledFor", "required": True})


@dataclass
class TestClock:
    simulated_time: str | None = field(
        default=None, metadata={"wire_name": "simulatedTime", "required": True}
    )
    is_active: bool = field(default=False, metadata={"wire_name": "isActive", "required": True})
    now: str = field(default="", metadata={"wire_name": "now", "required": True})
    latest_run: TestClockLatestRun | None = field(
        default=None, metadata={"wire_name": "latestRun", "required": True}
    )
    object: Literal["test_clock"] | None = field(
        default=None, metadata={"wire_name": "object", "required": True}
    )
    livemode: bool = field(default=False, metadata={"wire_name": "livemode", "required": True})


@dataclass
class TestClockLatestRun:
    id: str = field(default="", metadata={"wire_name": "id", "required": True})
    status: Literal["pending", "running", "completed", "failed"] | None = field(
        default=None, metadata={"wire_name": "status", "required": True}
    )
    started_at_time: str = field(
        default="", metadata={"wire_name": "startedAtTime", "required": True}
    )
    target_time: str = field(default="", metadata={"wire_name": "targetTime", "required": True})
    estimated_deadline_count: int = field(
        default=0, metadata={"wire_name": "estimatedDeadlineCount", "required": True}
    )
    completed_deadline_count: int = field(
        default=0, metadata={"wire_name": "completedDeadlineCount", "required": True}
    )
    failed_deadline_count: int = field(
        default=0, metadata={"wire_name": "failedDeadlineCount", "required": True}
    )
    error: str | None = field(default=None, metadata={"wire_name": "error", "required": True})
    items: list[TestClockLatestRunItemsItem] = field(
        default_factory=list, metadata={"wire_name": "items", "required": True}
    )


@dataclass
class TestClockLatestRunItemsItem:
    kind: Literal["billing_cycle", "dunning_retry"] | None = field(
        default=None, metadata={"wire_name": "kind", "required": True}
    )
    status: Literal["pending", "processing", "completed", "failed"] | None = field(
        default=None, metadata={"wire_name": "status", "required": True}
    )
    due_at: str = field(default="", metadata={"wire_name": "dueAt", "required": True})
    subscription_id: str = field(
        default="", metadata={"wire_name": "subscriptionId", "required": True}
    )
    customer_name: str | None = field(
        default=None, metadata={"wire_name": "customerName", "required": True}
    )
    invoice_number: str | None = field(
        default=None, metadata={"wire_name": "invoiceNumber", "required": True}
    )
    invoice_id: str | None = field(
        default=None, metadata={"wire_name": "invoiceId", "required": True}
    )
    outcome: str | None = field(default=None, metadata={"wire_name": "outcome", "required": True})
    detail: str | None = field(default=None, metadata={"wire_name": "detail", "required": True})
    error: str | None = field(default=None, metadata={"wire_name": "error", "required": True})


@dataclass
class TestClockRun:
    id: str = field(default="", metadata={"wire_name": "id", "required": True})
    status: Literal["pending", "running", "completed", "failed"] | None = field(
        default=None, metadata={"wire_name": "status", "required": True}
    )
    started_at_time: str = field(
        default="", metadata={"wire_name": "startedAtTime", "required": True}
    )
    target_time: str = field(default="", metadata={"wire_name": "targetTime", "required": True})
    estimated_deadline_count: int = field(
        default=0, metadata={"wire_name": "estimatedDeadlineCount", "required": True}
    )
    completed_deadline_count: int = field(
        default=0, metadata={"wire_name": "completedDeadlineCount", "required": True}
    )
    failed_deadline_count: int = field(
        default=0, metadata={"wire_name": "failedDeadlineCount", "required": True}
    )
    error: str | None = field(default=None, metadata={"wire_name": "error", "required": True})
    items: list[TestClockRunItemsItem] = field(
        default_factory=list, metadata={"wire_name": "items", "required": True}
    )
    object: Literal["test_clock_run"] | None = field(
        default=None, metadata={"wire_name": "object", "required": True}
    )
    livemode: bool = field(default=False, metadata={"wire_name": "livemode", "required": True})


@dataclass
class TestClockRunItemsItem:
    kind: Literal["billing_cycle", "dunning_retry"] | None = field(
        default=None, metadata={"wire_name": "kind", "required": True}
    )
    status: Literal["pending", "processing", "completed", "failed"] | None = field(
        default=None, metadata={"wire_name": "status", "required": True}
    )
    due_at: str = field(default="", metadata={"wire_name": "dueAt", "required": True})
    subscription_id: str = field(
        default="", metadata={"wire_name": "subscriptionId", "required": True}
    )
    customer_name: str | None = field(
        default=None, metadata={"wire_name": "customerName", "required": True}
    )
    invoice_number: str | None = field(
        default=None, metadata={"wire_name": "invoiceNumber", "required": True}
    )
    invoice_id: str | None = field(
        default=None, metadata={"wire_name": "invoiceId", "required": True}
    )
    outcome: str | None = field(default=None, metadata={"wire_name": "outcome", "required": True})
    detail: str | None = field(default=None, metadata={"wire_name": "detail", "required": True})
    error: str | None = field(default=None, metadata={"wire_name": "error", "required": True})


@dataclass
class TrackUsageParamsPropertiesItem:
    property: str = field(default="", metadata={"wire_name": "property", "required": True})
    value: str = field(default="", metadata={"wire_name": "value", "required": True})


@dataclass
class Transaction:
    payment_context: TransactionPaymentContext | None = field(
        default=None, metadata={"wire_name": "paymentContext", "required": True}
    )
    id: str = field(default="", metadata={"wire_name": "id", "required": True})
    invoice_id: str | None = field(
        default=None, metadata={"wire_name": "invoiceId", "required": True}
    )
    gross_amount: int | None = field(
        default=None, metadata={"wire_name": "grossAmount", "required": True}
    )
    subtotal: int | None = field(default=None, metadata={"wire_name": "subtotal", "required": True})
    tax_amount: int | None = field(
        default=None, metadata={"wire_name": "taxAmount", "required": True}
    )
    presentment_amount: int | None = field(
        default=None, metadata={"wire_name": "presentmentAmount", "required": True}
    )
    currency: str = field(default="", metadata={"wire_name": "currency", "required": True})
    provider: PaymentProvider | None = field(
        default=None, metadata={"wire_name": "provider", "required": True}
    )
    payment_method: PaymentMethod | None = field(
        default=None, metadata={"wire_name": "paymentMethod", "required": True}
    )
    sub_payment_method: SubPaymentMethod | None = field(
        default=None, metadata={"wire_name": "subPaymentMethod", "required": True}
    )
    status: TransactionStatus | None = field(
        default=None, metadata={"wire_name": "status", "required": True}
    )
    customer_email: str | None = field(
        default=None, metadata={"wire_name": "customerEmail", "required": True}
    )
    customer_name: str | None = field(
        default=None, metadata={"wire_name": "customerName", "required": True}
    )
    paid_at: str | None = field(default=None, metadata={"wire_name": "paidAt", "required": True})
    created_at: str = field(default="", metadata={"wire_name": "createdAt", "required": True})
    updated_at: str = field(default="", metadata={"wire_name": "updatedAt", "required": True})
    available_at: str | None = field(
        default=None, metadata={"wire_name": "availableAt", "required": True}
    )
    object: Literal["transaction"] | None = field(
        default=None, metadata={"wire_name": "object", "required": True}
    )
    livemode: bool = field(default=False, metadata={"wire_name": "livemode", "required": True})


@dataclass
class TransactionListItem:
    payment_context: TransactionListItemPaymentContext | None = field(
        default=None, metadata={"wire_name": "paymentContext", "required": True}
    )
    id: str = field(default="", metadata={"wire_name": "id", "required": True})
    invoice_id: str | None = field(
        default=None, metadata={"wire_name": "invoiceId", "required": True}
    )
    gross_amount: int | None = field(
        default=None, metadata={"wire_name": "grossAmount", "required": True}
    )
    subtotal: int | None = field(default=None, metadata={"wire_name": "subtotal", "required": True})
    tax_amount: int | None = field(
        default=None, metadata={"wire_name": "taxAmount", "required": True}
    )
    presentment_amount: int | None = field(
        default=None, metadata={"wire_name": "presentmentAmount", "required": True}
    )
    currency: str = field(default="", metadata={"wire_name": "currency", "required": True})
    provider: PaymentProvider | None = field(
        default=None, metadata={"wire_name": "provider", "required": True}
    )
    payment_method: PaymentMethod | None = field(
        default=None, metadata={"wire_name": "paymentMethod", "required": True}
    )
    sub_payment_method: SubPaymentMethod | None = field(
        default=None, metadata={"wire_name": "subPaymentMethod", "required": True}
    )
    status: TransactionStatus | None = field(
        default=None, metadata={"wire_name": "status", "required": True}
    )
    customer_email: str | None = field(
        default=None, metadata={"wire_name": "customerEmail", "required": True}
    )
    customer_name: str | None = field(
        default=None, metadata={"wire_name": "customerName", "required": True}
    )
    paid_at: str | None = field(default=None, metadata={"wire_name": "paidAt", "required": True})
    created_at: str = field(default="", metadata={"wire_name": "createdAt", "required": True})
    updated_at: str = field(default="", metadata={"wire_name": "updatedAt", "required": True})
    object: Literal["transaction"] | None = field(
        default=None, metadata={"wire_name": "object", "required": True}
    )
    livemode: bool = field(default=False, metadata={"wire_name": "livemode", "required": True})


@dataclass
class TransactionListItemPaymentContext:
    reason: (
        Literal[
            "first_subscription_payment",
            "trial_conversion",
            "recurring_billing",
            "plan_change",
            "reactivation",
            "subscription_resume",
            "one_time_payment",
            "overage",
            "adjustment",
        ]
        | None
    ) = field(default=None, metadata={"wire_name": "reason", "required": True})
    payment_link_id: str | None = field(
        default=None, metadata={"wire_name": "paymentLinkId", "required": True}
    )
    recovery: TransactionListItemPaymentContextRecovery | None = field(
        default=None, metadata={"wire_name": "recovery", "required": True}
    )


@dataclass
class TransactionListItemPaymentContextRecoveryVariant1:
    type: Literal["payment_recovery"] | None = field(
        default=None, metadata={"wire_name": "type", "required": True}
    )


@dataclass
class TransactionListItemPaymentContextRecoveryVariant2:
    type: Literal["dunning_retry"] | None = field(
        default=None, metadata={"wire_name": "type", "required": True}
    )
    attempt: int = field(default=0, metadata={"wire_name": "attempt", "required": True})
    max_attempts: int = field(default=0, metadata={"wire_name": "maxAttempts", "required": True})


@dataclass
class TransactionPaymentContext:
    reason: (
        Literal[
            "first_subscription_payment",
            "trial_conversion",
            "recurring_billing",
            "plan_change",
            "reactivation",
            "subscription_resume",
            "one_time_payment",
            "overage",
            "adjustment",
        ]
        | None
    ) = field(default=None, metadata={"wire_name": "reason", "required": True})
    payment_link_id: str | None = field(
        default=None, metadata={"wire_name": "paymentLinkId", "required": True}
    )
    recovery: TransactionPaymentContextRecovery | None = field(
        default=None, metadata={"wire_name": "recovery", "required": True}
    )


@dataclass
class TransactionPaymentContextRecoveryVariant1:
    type: Literal["payment_recovery"] | None = field(
        default=None, metadata={"wire_name": "type", "required": True}
    )


@dataclass
class TransactionPaymentContextRecoveryVariant2:
    type: Literal["dunning_retry"] | None = field(
        default=None, metadata={"wire_name": "type", "required": True}
    )
    attempt: int = field(default=0, metadata={"wire_name": "attempt", "required": True})
    max_attempts: int = field(default=0, metadata={"wire_name": "maxAttempts", "required": True})


@dataclass
class TransactionRetry:
    original_transaction_id: str = field(
        default="", metadata={"wire_name": "originalTransactionId", "required": True}
    )
    invoice_id: str = field(default="", metadata={"wire_name": "invoiceId", "required": True})
    status: Literal["processing", "succeeded"] | None = field(
        default=None, metadata={"wire_name": "status", "required": True}
    )
    object: Literal["transaction_retry"] | None = field(
        default=None, metadata={"wire_name": "object", "required": True}
    )
    livemode: bool = field(default=False, metadata={"wire_name": "livemode", "required": True})


@dataclass
class TransactionsListResult:
    object: Literal["list"] | None = field(
        default=None, metadata={"wire_name": "object", "required": True}
    )
    data: list[TransactionListItem] = field(
        default_factory=list, metadata={"wire_name": "data", "required": True}
    )
    has_more: bool = field(default=False, metadata={"wire_name": "hasMore", "required": True})
    next_cursor: str | None = field(
        default=None, metadata={"wire_name": "nextCursor", "required": False}
    )


@dataclass
class UpdateCustomerParamsAddress:
    line1: str = field(default="", metadata={"wire_name": "line1", "required": True})
    line2: str | None = field(default=None, metadata={"wire_name": "line2", "required": False})
    city: str = field(default="", metadata={"wire_name": "city", "required": True})
    state: str | None = field(default=None, metadata={"wire_name": "state", "required": False})
    postal_code: str = field(default="", metadata={"wire_name": "postalCode", "required": True})
    country: str = field(default="", metadata={"wire_name": "country", "required": True})
    region: str | None = field(default=None, metadata={"wire_name": "region", "required": False})


@dataclass
class UpdateOfferParamsPhasesItemVariant1:
    type: Literal["free_trial"] | None = field(
        default=None, metadata={"wire_name": "type", "required": True}
    )
    duration_days: int = field(default=0, metadata={"wire_name": "durationDays", "required": True})


@dataclass
class UpdateOfferParamsPhasesItemVariant2:
    type: Literal["percentage"] | None = field(
        default=None, metadata={"wire_name": "type", "required": True}
    )
    duration_cycles: int | None = field(
        default=None, metadata={"wire_name": "durationCycles", "required": True}
    )
    duration_interval: Literal["weekly", "monthly", "quarterly", "yearly"] | None = field(
        default=None, metadata={"wire_name": "durationInterval", "required": False}
    )
    percentage: int = field(default=0, metadata={"wire_name": "percentage", "required": True})


@dataclass
class UpdateOfferParamsPhasesItemVariant3:
    type: Literal["amount_off"] | None = field(
        default=None, metadata={"wire_name": "type", "required": True}
    )
    duration_cycles: int | None = field(
        default=None, metadata={"wire_name": "durationCycles", "required": True}
    )
    duration_interval: Literal["weekly", "monthly", "quarterly", "yearly"] | None = field(
        default=None, metadata={"wire_name": "durationInterval", "required": False}
    )
    amounts: list[UpdateOfferParamsPhasesItemVariant3AmountsItem] = field(
        default_factory=list, metadata={"wire_name": "amounts", "required": True}
    )


@dataclass
class UpdateOfferParamsPhasesItemVariant3AmountsItem:
    currency: str = field(default="", metadata={"wire_name": "currency", "required": True})
    amount: int = field(default=0, metadata={"wire_name": "amount", "required": True})


@dataclass
class UpdateOfferParamsPhasesItemVariant4:
    type: Literal["fixed_price"] | None = field(
        default=None, metadata={"wire_name": "type", "required": True}
    )
    duration_cycles: int | None = field(
        default=None, metadata={"wire_name": "durationCycles", "required": True}
    )
    duration_interval: Literal["weekly", "monthly", "quarterly", "yearly"] | None = field(
        default=None, metadata={"wire_name": "durationInterval", "required": False}
    )
    prices: list[UpdateOfferParamsPhasesItemVariant4PricesItem] = field(
        default_factory=list, metadata={"wire_name": "prices", "required": True}
    )


@dataclass
class UpdateOfferParamsPhasesItemVariant4PricesItem:
    currency: str = field(default="", metadata={"wire_name": "currency", "required": True})
    amount: int = field(default=0, metadata={"wire_name": "amount", "required": True})


@dataclass
class UpdatePlanFeatureParamsOverage:
    enabled: bool | None = field(default=None, metadata={"wire_name": "enabled", "required": False})
    unit_price: int | None = field(
        default=None, metadata={"wire_name": "unitPrice", "required": False}
    )


@dataclass
class UpdatePlanPriceParamsMarketPricesItem:
    market_group_id: str = field(
        default="", metadata={"wire_name": "marketGroupId", "required": True}
    )
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
            "gbp",
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
    ) = field(default=None, metadata={"wire_name": "currency", "required": True})
    price: int = field(default=0, metadata={"wire_name": "price", "required": True})


@dataclass
class UpsertRegionalPricesParamsOverridesItem:
    currency: str = field(default="", metadata={"wire_name": "currency", "required": True})
    price: int = field(default=0, metadata={"wire_name": "price", "required": True})
    included_balance: int | None = field(
        default=None, metadata={"wire_name": "includedBalance", "required": False}
    )


@dataclass
class UsageAdjustment:
    id: str = field(default="", metadata={"wire_name": "id", "required": True})
    value: int = field(default=0, metadata={"wire_name": "value", "required": True})
    previous_value: int = field(
        default=0, metadata={"wire_name": "previousValue", "required": True}
    )
    adjustment: int = field(default=0, metadata={"wire_name": "adjustment", "required": True})
    customer_id: str = field(default="", metadata={"wire_name": "customerId", "required": True})
    reason: str | None = field(default=None, metadata={"wire_name": "reason", "required": True})
    ts: str = field(default="", metadata={"wire_name": "ts", "required": True})
    created_at: str = field(default="", metadata={"wire_name": "createdAt", "required": True})
    feature_code: str = field(default="", metadata={"wire_name": "featureCode", "required": True})
    object: Literal["usage_adjustment"] | None = field(
        default=None, metadata={"wire_name": "object", "required": True}
    )
    livemode: bool = field(default=False, metadata={"wire_name": "livemode", "required": True})


@dataclass
class UsageCheckVariant1:
    allowed: bool = field(default=False, metadata={"wire_name": "allowed", "required": True})
    subscription_status: str = field(
        default="", metadata={"wire_name": "subscriptionStatus", "required": True}
    )
    feature_code: str = field(default="", metadata={"wire_name": "featureCode", "required": True})
    quantity: int = field(default=0, metadata={"wire_name": "quantity", "required": True})
    reason: str | None = field(default=None, metadata={"wire_name": "reason", "required": False})
    message: str | None = field(default=None, metadata={"wire_name": "message", "required": False})
    consumption_model: Literal["metered"] | None = field(
        default=None, metadata={"wire_name": "consumptionModel", "required": True}
    )
    current: float = field(default=0.0, metadata={"wire_name": "current", "required": True})
    remaining: float = field(default=0.0, metadata={"wire_name": "remaining", "required": True})
    unlimited: bool = field(default=False, metadata={"wire_name": "unlimited", "required": True})
    included: float = field(default=0.0, metadata={"wire_name": "included", "required": True})
    overage_enabled: bool = field(
        default=False, metadata={"wire_name": "overageEnabled", "required": True}
    )
    overage_unit_price: float | None = field(
        default=None, metadata={"wire_name": "overageUnitPrice", "required": True}
    )
    object: Literal["usage_check"] | None = field(
        default=None, metadata={"wire_name": "object", "required": True}
    )
    livemode: bool = field(default=False, metadata={"wire_name": "livemode", "required": True})


@dataclass
class UsageCheckVariant2:
    allowed: bool = field(default=False, metadata={"wire_name": "allowed", "required": True})
    subscription_status: str = field(
        default="", metadata={"wire_name": "subscriptionStatus", "required": True}
    )
    feature_code: str = field(default="", metadata={"wire_name": "featureCode", "required": True})
    quantity: int = field(default=0, metadata={"wire_name": "quantity", "required": True})
    reason: str | None = field(default=None, metadata={"wire_name": "reason", "required": False})
    message: str | None = field(default=None, metadata={"wire_name": "message", "required": False})
    consumption_model: Literal["credits"] | None = field(
        default=None, metadata={"wire_name": "consumptionModel", "required": True}
    )
    credits_per_unit: int = field(
        default=0, metadata={"wire_name": "creditsPerUnit", "required": True}
    )
    estimated_credits: int = field(
        default=0, metadata={"wire_name": "estimatedCredits", "required": True}
    )
    plan_credits: int = field(default=0, metadata={"wire_name": "planCredits", "required": True})
    purchased_credits: int = field(
        default=0, metadata={"wire_name": "purchasedCredits", "required": True}
    )
    total_credits: int = field(default=0, metadata={"wire_name": "totalCredits", "required": True})
    object: Literal["usage_check"] | None = field(
        default=None, metadata={"wire_name": "object", "required": True}
    )
    livemode: bool = field(default=False, metadata={"wire_name": "livemode", "required": True})


@dataclass
class UsageCheckVariant3:
    allowed: bool = field(default=False, metadata={"wire_name": "allowed", "required": True})
    subscription_status: str = field(
        default="", metadata={"wire_name": "subscriptionStatus", "required": True}
    )
    feature_code: str = field(default="", metadata={"wire_name": "featureCode", "required": True})
    quantity: int = field(default=0, metadata={"wire_name": "quantity", "required": True})
    reason: str | None = field(default=None, metadata={"wire_name": "reason", "required": False})
    message: str | None = field(default=None, metadata={"wire_name": "message", "required": False})
    consumption_model: Literal["balance"] | None = field(
        default=None, metadata={"wire_name": "consumptionModel", "required": True}
    )
    unit_price: float = field(default=0.0, metadata={"wire_name": "unitPrice", "required": True})
    estimated_amount: float = field(
        default=0.0, metadata={"wire_name": "estimatedAmount", "required": True}
    )
    current_balance: float = field(
        default=0.0, metadata={"wire_name": "currentBalance", "required": True}
    )
    block_on_exhaustion: bool = field(
        default=False, metadata={"wire_name": "blockOnExhaustion", "required": True}
    )
    currency: str = field(default="", metadata={"wire_name": "currency", "required": True})
    object: Literal["usage_check"] | None = field(
        default=None, metadata={"wire_name": "object", "required": True}
    )
    livemode: bool = field(default=False, metadata={"wire_name": "livemode", "required": True})


@dataclass
class UsageEvent:
    id: str = field(default="", metadata={"wire_name": "id", "required": True})
    feature_code: str = field(default="", metadata={"wire_name": "featureCode", "required": True})
    value: float = field(default=0.0, metadata={"wire_name": "value", "required": True})
    customer_id: str = field(default="", metadata={"wire_name": "customerId", "required": True})
    event_id: str | None = field(default=None, metadata={"wire_name": "eventId", "required": True})
    ts: str = field(default="", metadata={"wire_name": "ts", "required": True})
    created_at: str = field(default="", metadata={"wire_name": "createdAt", "required": True})
    properties: list[UsageEventPropertiesItem] = field(
        default_factory=list, metadata={"wire_name": "properties", "required": True}
    )
    consumption: UsageEventConsumption | None = field(
        default=None, metadata={"wire_name": "consumption", "required": False}
    )
    object: Literal["usage_event"] | None = field(
        default=None, metadata={"wire_name": "object", "required": True}
    )
    livemode: bool = field(default=False, metadata={"wire_name": "livemode", "required": True})


@dataclass
class UsageEventConsumption:
    model: Literal["credits", "balance"] | None = field(
        default=None, metadata={"wire_name": "model", "required": True}
    )
    deducted: float = field(default=0.0, metadata={"wire_name": "deducted", "required": True})
    remaining: float = field(default=0.0, metadata={"wire_name": "remaining", "required": True})
    blocked: bool = field(default=False, metadata={"wire_name": "blocked", "required": True})


@dataclass
class UsageEventPropertiesItem:
    property: str = field(default="", metadata={"wire_name": "property", "required": True})
    value: str = field(default="", metadata={"wire_name": "value", "required": True})


@dataclass
class UsageQuota:
    feature_code: str = field(default="", metadata={"wire_name": "featureCode", "required": True})
    current: float = field(default=0.0, metadata={"wire_name": "current", "required": True})
    included: float = field(default=0.0, metadata={"wire_name": "included", "required": True})
    remaining: float | None = field(
        default=None, metadata={"wire_name": "remaining", "required": True}
    )
    billed_quantity: float = field(
        default=0.0, metadata={"wire_name": "billedQuantity", "required": True}
    )
    unlimited: bool = field(default=False, metadata={"wire_name": "unlimited", "required": True})
    overage_enabled: bool = field(
        default=False, metadata={"wire_name": "overageEnabled", "required": True}
    )
    as_of: str | None = field(default=None, metadata={"wire_name": "asOf", "required": True})
    object: Literal["usage_quota"] | None = field(
        default=None, metadata={"wire_name": "object", "required": True}
    )
    livemode: bool = field(default=False, metadata={"wire_name": "livemode", "required": True})


@dataclass
class UsageQuotaEvent:
    id: str = field(default="", metadata={"wire_name": "id", "required": True})
    customer_id: str = field(default="", metadata={"wire_name": "customerId", "required": True})
    feature_code: str = field(default="", metadata={"wire_name": "featureCode", "required": True})
    previous_balance: int = field(
        default=0, metadata={"wire_name": "previousBalance", "required": True}
    )
    new_balance: int = field(default=0, metadata={"wire_name": "newBalance", "required": True})
    ts: str = field(default="", metadata={"wire_name": "ts", "required": True})
    created_at: str = field(default="", metadata={"wire_name": "createdAt", "required": True})
    object: Literal["usage_quota_event"] | None = field(
        default=None, metadata={"wire_name": "object", "required": True}
    )
    livemode: bool = field(default=False, metadata={"wire_name": "livemode", "required": True})


@dataclass
class Webhook:
    id: str = field(default="", metadata={"wire_name": "id", "required": True})
    url: str = field(default="", metadata={"wire_name": "url", "required": True})
    events: list[str] = field(
        default_factory=list, metadata={"wire_name": "events", "required": True}
    )
    description: str | None = field(
        default=None, metadata={"wire_name": "description", "required": True}
    )
    is_active: bool = field(default=False, metadata={"wire_name": "isActive", "required": True})
    api_version: str | None = field(
        default=None, metadata={"wire_name": "apiVersion", "required": True}
    )
    created_at: str = field(default="", metadata={"wire_name": "createdAt", "required": True})
    object: Literal["webhook"] | None = field(
        default=None, metadata={"wire_name": "object", "required": True}
    )
    livemode: bool = field(default=False, metadata={"wire_name": "livemode", "required": True})


@dataclass
class WebhookAddonRef:
    id: str = field(default="", metadata={"wire_name": "id", "required": True})
    name: str = field(default="", metadata={"wire_name": "name", "required": True})


@dataclass
class WebhookBalance:
    current_balance: float = field(
        default=0.0, metadata={"wire_name": "currentBalance", "required": True}
    )


@dataclass
class WebhookBankRef:
    bank_name: str | None = field(
        default=None, metadata={"wire_name": "bankName", "required": True}
    )
    last4: str = field(default="", metadata={"wire_name": "last4", "required": True})


@dataclass
class WebhookCardInfo:
    brand: str = field(default="", metadata={"wire_name": "brand", "required": True})
    last4: str = field(default="", metadata={"wire_name": "last4", "required": True})
    exp_month: float = field(default=0.0, metadata={"wire_name": "expMonth", "required": True})
    exp_year: float = field(default=0.0, metadata={"wire_name": "expYear", "required": True})


@dataclass
class WebhookCreditsBalance:
    plan_credits: float = field(
        default=0.0, metadata={"wire_name": "planCredits", "required": True}
    )
    purchased_credits: float = field(
        default=0.0, metadata={"wire_name": "purchasedCredits", "required": True}
    )
    total_credits: float = field(
        default=0.0, metadata={"wire_name": "totalCredits", "required": True}
    )


@dataclass
class WebhookPlanGrantTimelineEvent:
    id: str = field(default="", metadata={"wire_name": "id", "required": True})
    type: Literal["created", "updated", "expired", "revoked"] | None = field(
        default=None, metadata={"wire_name": "type", "required": True}
    )
    reason: str = field(default="", metadata={"wire_name": "reason", "required": True})
    source: Literal["dashboard", "api", "system"] | None = field(
        default=None, metadata={"wire_name": "source", "required": True}
    )
    previous_expires_at: str | None = field(
        default=None, metadata={"wire_name": "previousExpiresAt", "required": True}
    )
    expires_at: str | None = field(
        default=None, metadata={"wire_name": "expiresAt", "required": True}
    )
    duration: Literal["cycles", "until_date", "until_revoked"] | None = field(
        default=None, metadata={"wire_name": "duration", "required": True}
    )
    duration_cycles: int | None = field(
        default=None, metadata={"wire_name": "durationCycles", "required": True}
    )
    requested_expires_at: str | None = field(
        default=None, metadata={"wire_name": "requestedExpiresAt", "required": True}
    )
    created_at: str = field(default="", metadata={"wire_name": "createdAt", "required": True})


@dataclass
class WebhookPlanRef:
    id: str = field(default="", metadata={"wire_name": "id", "required": True})
    name: str = field(default="", metadata={"wire_name": "name", "required": True})


@dataclass
class WebhookSeatSummary:
    code: str = field(default="", metadata={"wire_name": "code", "required": True})
    current: float | None = field(default=None, metadata={"wire_name": "current", "required": True})
    included: float | None = field(
        default=None, metadata={"wire_name": "included", "required": True}
    )
    remaining: float | None = field(
        default=None, metadata={"wire_name": "remaining", "required": True}
    )
    unlimited: bool | None = field(
        default=None, metadata={"wire_name": "unlimited", "required": True}
    )


@dataclass
class WebhooksListResult:
    object: Literal["list"] | None = field(
        default=None, metadata={"wire_name": "object", "required": True}
    )
    data: list[Webhook] = field(
        default_factory=list, metadata={"wire_name": "data", "required": True}
    )
    has_more: bool = field(default=False, metadata={"wire_name": "hasMore", "required": True})
    next_cursor: str | None = field(
        default=None, metadata={"wire_name": "nextCursor", "required": False}
    )


@dataclass
class WebhookTest:
    success: bool = field(default=False, metadata={"wire_name": "success", "required": True})
    delivery_id: str = field(default="", metadata={"wire_name": "deliveryId", "required": True})
    delivered_at: str = field(default="", metadata={"wire_name": "deliveredAt", "required": True})
    object: Literal["webhook_delivery"] | None = field(
        default=None, metadata={"wire_name": "object", "required": True}
    )
    livemode: bool = field(default=False, metadata={"wire_name": "livemode", "required": True})


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


TransactionListItemPaymentContextRecovery = Union[
    TransactionListItemPaymentContextRecoveryVariant1,
    TransactionListItemPaymentContextRecoveryVariant2,
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


TransactionPaymentContextRecovery = Union[
    TransactionPaymentContextRecoveryVariant1, TransactionPaymentContextRecoveryVariant2
]


FeatureAccessVariant2Consumption = Union[
    FeatureAccessVariant2ConsumptionVariant1,
    FeatureAccessVariant2ConsumptionVariant2,
    FeatureAccessVariant2ConsumptionVariant3,
]


PaymentPaymentContextRecovery = Union[
    PaymentPaymentContextRecoveryVariant1, PaymentPaymentContextRecoveryVariant2
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


CreatedSubscriptionPause = Union[CreatedSubscriptionPauseVariant1, CreatedSubscriptionPauseVariant2]


SubscriptionFeaturesItem = Union[
    SubscriptionFeaturesItemVariant1,
    SubscriptionFeaturesItemVariant2,
    SubscriptionFeaturesItemVariant3,
    SubscriptionFeaturesItemVariant4,
]


SubscriptionSummaryPause = Union[SubscriptionSummaryPauseVariant1, SubscriptionSummaryPauseVariant2]


SubscriptionPause = Union[SubscriptionPauseVariant1, SubscriptionPauseVariant2]


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
        "PaymentMethod": PaymentMethod,
        "PaymentProvider": PaymentProvider,
        "SubPaymentMethod": SubPaymentMethod,
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
        "CreateApiKeyParamsPermissions": CreateApiKeyParamsPermissions,
        "CreateCustomerParamsAddress": CreateCustomerParamsAddress,
        "CreatedApiKey": CreatedApiKey,
        "CreatedSubscription": CreatedSubscription,
        "CreatedSubscriptionCancellation": CreatedSubscriptionCancellation,
        "CreatedSubscriptionCurrentPeriod": CreatedSubscriptionCurrentPeriod,
        "CreatedSubscriptionPauseVariant1": CreatedSubscriptionPauseVariant1,
        "CreatedSubscriptionPauseVariant2": CreatedSubscriptionPauseVariant2,
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
        "PaymentPaymentContext": PaymentPaymentContext,
        "PaymentPaymentContextRecoveryVariant1": PaymentPaymentContextRecoveryVariant1,
        "PaymentPaymentContextRecoveryVariant2": PaymentPaymentContextRecoveryVariant2,
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
        "SubscriptionPauseVariant1": SubscriptionPauseVariant1,
        "SubscriptionPauseVariant2": SubscriptionPauseVariant2,
        "SubscriptionPlan": SubscriptionPlan,
        "SubscriptionPlanGrant": SubscriptionPlanGrant,
        "SubscriptionPlanGrantPlan": SubscriptionPlanGrantPlan,
        "SubscriptionResume": SubscriptionResume,
        "SubscriptionScheduledPlanChange": SubscriptionScheduledPlanChange,
        "SubscriptionsListResult": SubscriptionsListResult,
        "SubscriptionSummary": SubscriptionSummary,
        "SubscriptionSummaryCancellation": SubscriptionSummaryCancellation,
        "SubscriptionSummaryCurrentPeriod": SubscriptionSummaryCurrentPeriod,
        "SubscriptionSummaryPauseVariant1": SubscriptionSummaryPauseVariant1,
        "SubscriptionSummaryPauseVariant2": SubscriptionSummaryPauseVariant2,
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
        "TransactionListItemPaymentContext": TransactionListItemPaymentContext,
        "TransactionListItemPaymentContextRecoveryVariant1": TransactionListItemPaymentContextRecoveryVariant1,
        "TransactionListItemPaymentContextRecoveryVariant2": TransactionListItemPaymentContextRecoveryVariant2,
        "TransactionPaymentContext": TransactionPaymentContext,
        "TransactionPaymentContextRecoveryVariant1": TransactionPaymentContextRecoveryVariant1,
        "TransactionPaymentContextRecoveryVariant2": TransactionPaymentContextRecoveryVariant2,
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
        "TransactionListItemPaymentContextRecovery": (
            "type",
            {
                "payment_recovery": TransactionListItemPaymentContextRecoveryVariant1,
                "dunning_retry": TransactionListItemPaymentContextRecoveryVariant2,
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
        "TransactionPaymentContextRecovery": (
            "type",
            {
                "payment_recovery": TransactionPaymentContextRecoveryVariant1,
                "dunning_retry": TransactionPaymentContextRecoveryVariant2,
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
        "PaymentPaymentContextRecovery": (
            "type",
            {
                "payment_recovery": PaymentPaymentContextRecoveryVariant1,
                "dunning_retry": PaymentPaymentContextRecoveryVariant2,
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
        "CreatedSubscriptionPause": (
            "status",
            {
                "scheduled": CreatedSubscriptionPauseVariant1,
                "active": CreatedSubscriptionPauseVariant2,
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
        "SubscriptionSummaryPause": (
            "status",
            {
                "scheduled": SubscriptionSummaryPauseVariant1,
                "active": SubscriptionSummaryPauseVariant2,
            },
            [],
        ),
        "SubscriptionPause": (
            "status",
            {"scheduled": SubscriptionPauseVariant1, "active": SubscriptionPauseVariant2},
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
