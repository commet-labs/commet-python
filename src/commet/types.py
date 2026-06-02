from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, TypeVar

T = TypeVar("T")


class FeatureType(str, Enum):
    BOOLEAN = "boolean"
    USAGE = "usage"
    SEATS = "seats"
    QUOTA = "quota"


class BillingInterval(str, Enum):
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    YEARLY = "yearly"
    ONE_TIME = "one_time"


class SubscriptionStatus(str, Enum):
    DRAFT = "draft"
    PENDING_PAYMENT = "pending_payment"
    TRIALING = "trialing"
    ACTIVE = "active"
    PAUSED = "paused"
    PAST_DUE = "past_due"
    CANCELED = "canceled"
    EXPIRED = "expired"


class ConsumptionModel(str, Enum):
    METERED = "metered"
    CREDITS = "credits"
    BALANCE = "balance"


class DiscountType(str, Enum):
    PERCENTAGE = "percentage"
    AMOUNT = "amount"


class SeatEventType(str, Enum):
    ADD = "add"
    REMOVE = "remove"
    SET = "set"


class OverageModel(str, Enum):
    PER_UNIT = "per_unit"


class Currency(str, Enum):
    USD = "USD"
    EUR = "EUR"
    GBP = "GBP"
    CAD = "CAD"
    AUD = "AUD"
    JPY = "JPY"
    ARS = "ARS"
    BRL = "BRL"
    MXN = "MXN"
    CLP = "CLP"


class PricingMode(str, Enum):
    FIXED = "fixed"
    AI_MODEL = "ai_model"


_ENUM_TYPES: dict[str, type[Enum]] = {
    cls.__name__: cls
    for cls in [
        FeatureType,
        BillingInterval,
        SubscriptionStatus,
        ConsumptionModel,
        DiscountType,
        SeatEventType,
        OverageModel,
        Currency,
        PricingMode,
    ]
}


def _coerce_enums(cls: type[T], kwargs: dict[str, Any]) -> dict[str, Any]:
    fields_map = cls.__dataclass_fields__  # type: ignore[attr-defined]
    result = {}
    for k, v in kwargs.items():
        if k in fields_map and v is not None:
            annotation = fields_map[k].type
            if isinstance(annotation, str):
                base = annotation.replace(" | None", "").strip()
                enum_cls = _ENUM_TYPES.get(base)
                if enum_cls is not None:
                    try:
                        v = enum_cls(v)
                    except ValueError:
                        pass
        result[k] = v
    return result


def _from_dict(cls: type[T], data: dict[str, Any]) -> T:
    if not isinstance(data, dict):
        return data  # type: ignore[return-value]
    fields = {f.name for f in cls.__dataclass_fields__.values()}  # type: ignore[attr-defined]
    filtered = {k: v for k, v in data.items() if k in fields}
    return cls(**_coerce_enums(cls, filtered))


def _from_list(cls: type[T], data: list[dict[str, Any]]) -> list[T]:
    return [_from_dict(cls, item) for item in data]


@dataclass
class Customer:
    id: str
    object: str = "customer"
    livemode: bool = False
    organization_id: str = ""
    full_name: str | None = None
    domain: str | None = None
    website: str | None = None
    billing_email: str = ""
    timezone: str | None = None
    language: str | None = None
    industry: str | None = None
    employee_count: str | None = None
    metadata: dict[str, Any] | None = None
    created_at: str = ""
    updated_at: str = ""


@dataclass
class Plan:
    id: str
    object: str = "plan"
    livemode: bool = False
    code: str = ""
    name: str = ""
    description: str | None = None
    is_public: bool = True
    is_free: bool = False
    is_default: bool = False
    sort_order: int = 0
    prices: list[dict[str, Any]] = field(default_factory=list)
    features: list[dict[str, Any]] = field(default_factory=list)
    created_at: str = ""
    updated_at: str | None = None


@dataclass
class Subscription:
    id: str
    object: str = "subscription"
    livemode: bool = False
    customer_id: str = ""
    plan_id: str | None = None
    plan_name: str | None = None
    name: str = ""
    description: str | None = None
    status: SubscriptionStatus = SubscriptionStatus.DRAFT
    consumption_model: ConsumptionModel | None = None
    billing_interval: BillingInterval | None = None
    trial_ends_at: str | None = None
    start_date: str = ""
    end_date: str | None = None
    current_period_start: str | None = None
    current_period_end: str | None = None
    billing_day_of_month: int = 1
    checkout_url: str | None = None
    plan: dict[str, Any] | None = None
    current_period: dict[str, Any] | None = None
    features: list[dict[str, Any]] = field(default_factory=list)
    credits: dict[str, Any] | None = None
    balance: dict[str, Any] | None = None
    cancellation: dict[str, Any] | None = None
    discount: dict[str, Any] | None = None
    next_billing_date: str | None = None
    intro_offer_ends_at: str | None = None
    intro_offer_discount_type: DiscountType | None = None
    intro_offer_discount_value: int | None = None
    created_at: str = ""
    updated_at: str = ""


@dataclass
class Feature:
    code: str
    name: str = ""
    type: FeatureType = FeatureType.BOOLEAN
    unit_name: str | None = None
    enabled: bool | None = None
    included_amount: int | None = None
    unlimited: bool | None = None
    overage_enabled: bool | None = None
    overage_unit_price: int | None = None


@dataclass
class FeatureManage:
    id: str
    object: str = "feature"
    livemode: bool = False
    name: str = ""
    code: str = ""
    type: FeatureType = FeatureType.BOOLEAN
    description: str | None = None
    unit_name: str | None = None
    created_at: str = ""
    updated_at: str = ""


@dataclass
class FeatureAccess:
    code: str
    object: str = "feature"
    livemode: bool = False
    name: str = ""
    type: FeatureType = FeatureType.BOOLEAN
    allowed: bool = False
    enabled: bool | None = None
    current: int | None = None
    included: int | None = None
    remaining: int | None = None
    overage: int | None = None
    overage_unit_price: int | None = None
    unlimited: bool | None = None
    overage_enabled: bool | None = None


@dataclass
class SeatBalance:
    current: int = 0
    as_of: str = ""


@dataclass
class SeatEvent:
    id: str
    object: str = "seat"
    livemode: bool = False
    organization_id: str = ""
    customer_id: str = ""
    feature_code: str = ""
    event_type: SeatEventType = SeatEventType.ADD
    quantity: int = 0
    previous_balance: int | None = None
    new_balance: int = 0
    ts: str = ""
    created_at: str = ""


@dataclass
class QuotaEvent:
    id: str
    customer_id: str = ""
    feature_code: str = ""
    previous_balance: int = 0
    new_balance: int = 0
    ts: str = ""
    created_at: str = ""


@dataclass
class QuotaAllowance:
    feature_code: str = ""
    current: int = 0
    included: int = 0
    remaining: int | None = None
    unlimited: bool = False
    overage_enabled: bool = False
    as_of: str | None = None


@dataclass
class CreditPack:
    id: str
    object: str = "credit_pack"
    livemode: bool = False
    name: str = ""
    description: str | None = None
    credits: int = 0
    price: int = 0
    currency: Currency = Currency.USD


@dataclass
class CreditPackDetail:
    id: str
    object: str = "credit_pack"
    livemode: bool = False
    name: str = ""
    description: str | None = None
    credits: int = 0
    price: int = 0
    is_active: bool = True
    created_at: str = ""
    updated_at: str = ""


@dataclass
class PortalSession:
    success: bool = False
    message: str = ""
    portal_url: str = ""


@dataclass
class UsageEvent:
    id: str
    object: str = "usage_event"
    livemode: bool = False
    organization_id: str = ""
    customer_id: str = ""
    feature: str = ""
    idempotency_key: str | None = None
    ts: str = ""
    properties: list[dict[str, str]] | None = None
    created_at: str = ""


@dataclass
class ApiKeyData:
    id: str
    object: str = "api_key"
    livemode: bool = False
    name: str = ""
    prefix: str = ""
    expires_at: str | None = None
    last_used_at: str | None = None
    created_at: str = ""


@dataclass
class ApiKeyCreated:
    id: str
    object: str = "api_key"
    livemode: bool = False
    name: str = ""
    prefix: str = ""
    api_key: str = ""
    expires_at: str | None = None
    last_used_at: str | None = None
    created_at: str = ""


@dataclass
class InvoiceListItem:
    id: str
    object: str = "invoice"
    livemode: bool = False
    customer_id: str = ""
    subscription_id: str | None = None
    invoice_number: str = ""
    status: str = ""
    invoice_type: str = ""
    currency: str = ""
    subtotal: int = 0
    discount_amount: int = 0
    tax_amount: int = 0
    total: int = 0
    period_start: str | None = None
    period_end: str | None = None
    issue_date: str = ""
    due_date: str | None = None
    memo: str | None = None
    metadata: dict[str, Any] | None = None
    created_at: str = ""
    updated_at: str = ""


@dataclass
class InvoiceDetail:
    id: str
    object: str = "invoice"
    livemode: bool = False
    customer_id: str = ""
    subscription_id: str | None = None
    invoice_number: str = ""
    status: str = ""
    invoice_type: str = ""
    currency: str = ""
    subtotal: int = 0
    discount_amount: int = 0
    tax_amount: int = 0
    total: int = 0
    credit_applied: int = 0
    period_start: str | None = None
    period_end: str | None = None
    issue_date: str = ""
    due_date: str | None = None
    memo: str | None = None
    plan_name: str | None = None
    po_number: str | None = None
    reference: str | None = None
    metadata: dict[str, Any] | None = None
    line_items: list[dict[str, Any]] = field(default_factory=list)
    created_at: str = ""
    updated_at: str = ""


@dataclass
class TransactionListItem:
    id: str
    object: str = "transaction"
    livemode: bool = False
    invoice_id: str = ""
    gross_amount: int = 0
    subtotal: int = 0
    tax_amount: int = 0
    currency: str = ""
    status: str = ""
    customer_email: str = ""
    customer_name: str | None = None
    paid_at: str | None = None
    created_at: str = ""
    updated_at: str = ""


@dataclass
class TransactionDetail:
    id: str
    object: str = "transaction"
    livemode: bool = False
    invoice_id: str = ""
    gross_amount: int = 0
    subtotal: int = 0
    tax_amount: int = 0
    currency: str = ""
    status: str = ""
    customer_email: str = ""
    customer_name: str | None = None
    paid_at: str | None = None
    available_at: str | None = None
    created_at: str = ""
    updated_at: str = ""


@dataclass
class PromoCode:
    id: str
    object: str = "promo_code"
    livemode: bool = False
    code: str = ""
    discount_type: DiscountType = DiscountType.PERCENTAGE
    discount_value: int = 0
    duration_cycles: int | None = None
    max_redemptions: int | None = None
    expires_at: str | None = None
    active: bool = True
    redemption_count: int = 0
    created_at: str = ""


@dataclass
class PromoCodeDetail:
    id: str
    object: str = "promo_code"
    livemode: bool = False
    code: str = ""
    discount_type: DiscountType = DiscountType.PERCENTAGE
    discount_value: int = 0
    duration_cycles: int | None = None
    max_redemptions: int | None = None
    expires_at: str | None = None
    active: bool = True
    redemption_count: int = 0
    created_at: str = ""
    updated_at: str = ""


@dataclass
class PlanGroup:
    id: str
    object: str = "plan_group"
    livemode: bool = False
    name: str = ""
    description: str | None = None
    is_public: bool = True
    created_at: str = ""
    updated_at: str = ""


@dataclass
class PlanGroupDetail:
    id: str
    object: str = "plan_group"
    livemode: bool = False
    name: str = ""
    description: str | None = None
    is_public: bool = True
    plans: list[dict[str, Any]] = field(default_factory=list)
    created_at: str = ""
    updated_at: str = ""


@dataclass
class PlanManage:
    id: str
    object: str = "plan"
    livemode: bool = False
    name: str = ""
    code: str = ""
    description: str | None = None
    consumption_model: str | None = None
    is_public: bool = True
    is_default: bool = False
    is_free: bool = False
    block_on_exhaustion: bool = False
    sort_order: int = 0
    plan_group_id: str | None = None
    metadata: dict[str, Any] | None = None
    created_at: str = ""
    updated_at: str = ""


@dataclass
class PlanPriceManage:
    id: str
    object: str = "plan_price"
    livemode: bool = False
    plan_id: str = ""
    billing_interval: BillingInterval = BillingInterval.MONTHLY
    price: int = 0
    is_default: bool = False
    trial_days: int = 0
    included_balance: int | None = None
    included_credits: int | None = None
    intro_offer_enabled: bool = False
    intro_offer_discount_type: str | None = None
    intro_offer_discount_value: int | None = None
    intro_offer_duration_cycles: int | None = None
    created_at: str = ""
    updated_at: str = ""


@dataclass
class WebhookEndpoint:
    id: str
    object: str = "webhook_endpoint"
    livemode: bool = False
    url: str = ""
    events: list[str] = field(default_factory=list)
    description: str | None = None
    is_active: bool = True
    created_at: str = ""


@dataclass
class WebhookEndpointCreated:
    id: str
    object: str = "webhook_endpoint"
    livemode: bool = False
    url: str = ""
    events: list[str] = field(default_factory=list)
    description: str | None = None
    is_active: bool = True
    secret_key: str = ""
    created_at: str = ""


@dataclass
class Addon:
    id: str
    object: str = "addon"
    livemode: bool = False
    name: str = ""
    slug: str = ""
    description: str | None = None
    base_price: int = 0
    feature_code: str = ""
    feature_name: str = ""
    consumption_model: str | None = None
    included_units: int | None = None
    overage_rate: int | None = None
    credit_cost: int | None = None
    created_at: str = ""
    updated_at: str = ""


@dataclass
class ActiveAddon:
    object: str = "addon"
    livemode: bool = False
    slug: str = ""
    name: str = ""
    base_price: int = 0
    feature_code: str = ""
    feature_name: str = ""
    feature_type: str = ""
    consumption_model: str | None = None
    activated_at: str = ""
