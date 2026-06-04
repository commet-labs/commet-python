from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Literal, TypeVar

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


class AddonConsumptionModel(str, Enum):
    BOOLEAN = "boolean"
    METERED = "metered"
    CREDITS = "credits"
    BALANCE = "balance"


class DiscountType(str, Enum):
    PERCENTAGE = "percentage"
    AMOUNT = "amount"


class InvoiceStatus(str, Enum):
    DRAFT = "draft"
    UPCOMING = "upcoming"
    OUTSTANDING = "outstanding"
    PAID = "paid"
    VOID = "void"
    UNCOLLECTIBLE = "uncollectible"


class InvoiceType(str, Enum):
    RECURRING = "recurring"
    OVERAGE = "overage"
    PLAN_CHANGE = "plan_change"
    ADJUSTMENT = "adjustment"
    CREDIT_PURCHASE = "credit_purchase"
    BALANCE_TOPUP = "balance_topup"
    ADDON_ACTIVATION = "addon_activation"


class InvoiceLineType(str, Enum):
    PLAN_BASE = "plan_base"
    FEATURE_OVERAGE = "feature_overage"
    FEATURE_SEATS = "feature_seats"
    FEATURE_QUOTA = "feature_quota"
    DISCOUNT = "discount"
    CREDIT = "credit"
    ADDON_BASE = "addon_base"


class ChargeType(str, Enum):
    STANDARD = "standard"
    ADVANCE = "advance"
    TRUE_UP = "true_up"


class TransactionStatus(str, Enum):
    PENDING = "pending"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    REFUNDED = "refunded"
    DISPUTED = "disputed"


class UsageCheckDenialReason(str, Enum):
    INCLUDED_LIMIT_REACHED = "included_limit_reached"
    INSUFFICIENT_CREDITS = "insufficient_credits"
    INSUFFICIENT_BALANCE = "insufficient_balance"


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


_ALL_ENUMS: list[type[Enum]] = [
    FeatureType,
    BillingInterval,
    SubscriptionStatus,
    ConsumptionModel,
    AddonConsumptionModel,
    DiscountType,
    InvoiceStatus,
    InvoiceType,
    InvoiceLineType,
    ChargeType,
    TransactionStatus,
    UsageCheckDenialReason,
    SeatEventType,
    OverageModel,
    Currency,
    PricingMode,
]

_ENUM_TYPES: dict[str, type[Enum]] = {cls.__name__: cls for cls in _ALL_ENUMS}

# Registry of nested dataclasses, populated at the end of the module once every
# dataclass is defined. Lets the parser resolve string annotations like
# "list[InvoiceLineItem]" or "CreditsSummary | None" into typed objects.
_DATACLASS_TYPES: dict[str, type[Any]] = {}


def _coerce_field(annotation: str, value: Any) -> Any:
    base = annotation.replace(" | None", "").strip()

    enum_cls = _ENUM_TYPES.get(base)
    if enum_cls is not None:
        try:
            return enum_cls(value)
        except ValueError:
            return value

    if base.startswith("list[") and base.endswith("]"):
        inner = base[len("list[") : -1].strip()
        nested_cls = _DATACLASS_TYPES.get(inner)
        if nested_cls is not None and isinstance(value, list):
            return [_from_dict(nested_cls, item) for item in value]
        return value

    nested_cls = _DATACLASS_TYPES.get(base)
    if nested_cls is not None and isinstance(value, dict):
        return _from_dict(nested_cls, value)

    return value


def _coerce_enums(cls: type[T], kwargs: dict[str, Any]) -> dict[str, Any]:
    fields_map = cls.__dataclass_fields__  # type: ignore[attr-defined]
    result = {}
    for k, v in kwargs.items():
        if k in fields_map and v is not None:
            annotation = fields_map[k].type
            if isinstance(annotation, str):
                v = _coerce_field(annotation, v)
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
class ChangePlanResult:
    id: str
    scheduled: bool = False
    customer_id: str | None = None
    previous_plan: dict[str, Any] | None = None
    current_plan: dict[str, Any] | None = None
    billing_interval: str | None = None
    billing: dict[str, Any] | None = None
    invoice_id: str | None = None
    scheduled_for: str | None = None
    change_type: str | None = None
    requires_checkout: bool | None = None
    checkout_url: str | None = None


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
    billed_quantity: int | None = None
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
    billed_quantity: int | None = None
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
    status: InvoiceStatus = InvoiceStatus.DRAFT
    invoice_type: InvoiceType = InvoiceType.RECURRING
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
    status: InvoiceStatus = InvoiceStatus.DRAFT
    invoice_type: InvoiceType = InvoiceType.RECURRING
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
    line_items: list[InvoiceLineItem] = field(default_factory=list)
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
    status: TransactionStatus = TransactionStatus.PENDING
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
    status: TransactionStatus = TransactionStatus.PENDING
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
    consumption_model: ConsumptionModel | None = None
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
    object: str = "webhook"
    livemode: bool = False
    url: str = ""
    events: list[str] = field(default_factory=list)
    description: str | None = None
    is_active: bool = True
    api_version: str | None = None
    created_at: str = ""


@dataclass
class WebhookEndpointCreated:
    id: str
    object: str = "webhook"
    livemode: bool = False
    url: str = ""
    events: list[str] = field(default_factory=list)
    description: str | None = None
    is_active: bool = True
    api_version: str | None = None
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
    feature_type: FeatureType = FeatureType.BOOLEAN
    consumption_model: AddonConsumptionModel | None = None
    activated_at: str = ""


@dataclass
class CustomerAddress:
    line1: str = ""
    line2: str | None = None
    city: str = ""
    state: str | None = None
    postal_code: str = ""
    country: str = ""


@dataclass
class CustomersBatchResult:
    successful: list[Customer] = field(default_factory=list)
    failed: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class CanUseResult:
    allowed: bool = False
    will_be_charged: bool = False
    reason: str | None = None


@dataclass
class InvoiceLineItem:
    line_type: InvoiceLineType = InvoiceLineType.PLAN_BASE
    feature_name: str | None = None
    description: str | None = None
    quantity: int = 0
    unit_amount: int = 0
    amount: int = 0
    included_amount: int | None = None
    used_amount: int | None = None
    overage_amount: int | None = None
    discount_type: DiscountType | None = None
    discount_value: int | None = None
    discount_name: str | None = None
    charge_type: ChargeType | None = None


@dataclass
class InvoiceDownloadResult:
    url: str = ""
    expires_at: str = ""


@dataclass
class InvoiceSendResult:
    sent: bool = False
    sent_at: str = ""


@dataclass
class InvoiceStatusResult:
    id: str
    status: Literal["paid", "void"] = "paid"
    updated_at: str = ""


@dataclass
class CreateAdjustmentResult:
    id: str
    object: str = "invoice"
    livemode: bool = False
    customer_id: str = ""
    invoice_number: str = ""
    status: Literal["outstanding", "paid"] = "outstanding"
    invoice_type: InvoiceType = InvoiceType.ADJUSTMENT
    currency: str = ""
    subtotal: int = 0
    tax_amount: int = 0
    total: int = 0
    issue_date: str = ""
    due_date: str | None = None
    memo: str | None = None
    metadata: dict[str, Any] | None = None
    created_at: str = ""
    updated_at: str = ""


@dataclass
class TransactionRefundResult:
    id: str
    status: Literal["refunded"] = "refunded"


@dataclass
class TransactionRetryResult:
    id: str
    status: Literal["processing"] = "processing"
    retry_invoice_number: str = ""


@dataclass
class UsageEventProperty:
    id: str
    usage_event_id: str = ""
    property: str = ""
    value: str = ""
    created_at: str = ""


@dataclass
class UsageCheckResult:
    allowed: bool = False
    consumption_model: ConsumptionModel = ConsumptionModel.METERED
    feature: str = ""
    quantity: int = 0
    current: int | None = None
    remaining: int | None = None
    unlimited: bool | None = None
    included: int | None = None
    overage_enabled: bool | None = None
    overage_unit_price: int | None = None
    credits_per_unit: int | None = None
    estimated_credits: int | None = None
    plan_credits: int | None = None
    purchased_credits: int | None = None
    total_credits: int | None = None
    unit_price: int | None = None
    estimated_amount: int | None = None
    current_balance: int | None = None
    block_on_exhaustion: bool | None = None
    currency: str | None = None
    reason: UsageCheckDenialReason | None = None
    message: str | None = None


@dataclass
class PlanPrice:
    billing_interval: BillingInterval = BillingInterval.MONTHLY
    price: int = 0
    is_default: bool = False
    trial_days: int = 0
    intro_offer: dict[str, Any] | None = None


@dataclass
class PlanFeature:
    code: str = ""
    name: str = ""
    type: FeatureType = FeatureType.BOOLEAN
    unit_name: str | None = None
    enabled: bool | None = None
    included_amount: int | None = None
    unlimited: bool | None = None
    overage_enabled: bool | None = None
    overage_unit_price: int | None = None
    overage: dict[str, Any] | None = None


@dataclass
class PlanDetail:
    id: str
    object: str = "plan"
    livemode: bool = False
    code: str = ""
    name: str = ""
    description: str | None = None
    is_public: bool = True
    is_default: bool = False
    sort_order: int = 0
    prices: list[PlanPrice] = field(default_factory=list)
    features: list[PlanFeature] = field(default_factory=list)
    created_at: str = ""
    updated_at: str = ""


@dataclass
class PlanFeatureManage:
    plan_id: str = ""
    feature_id: str = ""
    enabled: bool = False
    included_amount: int | None = None
    unlimited: bool = False
    overage_enabled: bool = False
    credits_per_unit: int | None = None
    pricing_mode: PricingMode = PricingMode.FIXED
    overage_unit_price: int | None = None
    margin: int | None = None


@dataclass
class RegionalPriceResult:
    price_id: str = ""
    overrides: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class DeleteResult:
    id: str
    deleted: bool = True


@dataclass
class RemoveResult:
    id: str
    removed: bool = True


@dataclass
class FeatureSummary:
    code: str = ""
    name: str = ""
    type: FeatureType = FeatureType.BOOLEAN
    enabled: bool | None = None
    usage: dict[str, Any] | None = None


@dataclass
class CreditsSummary:
    remaining: int = 0
    included: int = 0
    purchased: int = 0


@dataclass
class BalanceSummary:
    remaining: int = 0
    included: int = 0
    currency: str = ""


@dataclass
class CancellationSummary:
    scheduled_at: str = ""
    reason: str | None = None
    effective_at: str = ""


@dataclass
class DiscountSummary:
    type: DiscountType = DiscountType.PERCENTAGE
    value: int = 0
    name: str | None = None
    ends_at: str | None = None


@dataclass
class ActiveSubscription:
    id: str
    object: str = "subscription"
    livemode: bool = False
    customer_id: str = ""
    plan: dict[str, Any] | None = None
    name: str = ""
    description: str | None = None
    status: SubscriptionStatus = SubscriptionStatus.ACTIVE
    consumption_model: ConsumptionModel | None = None
    trial_ends_at: str | None = None
    current_period: dict[str, Any] | None = None
    features: list[FeatureSummary] = field(default_factory=list)
    credits: CreditsSummary | None = None
    balance: BalanceSummary | None = None
    cancellation: CancellationSummary | None = None
    discount: DiscountSummary | None = None
    start_date: str = ""
    end_date: str | None = None
    billing_day_of_month: int = 1
    next_billing_date: str = ""
    checkout_url: str | None = None
    created_at: str = ""
    updated_at: str = ""


@dataclass
class CreatedSubscription:
    id: str
    object: str = "subscription"
    livemode: bool = False
    customer_id: str = ""
    plan_id: str = ""
    plan_name: str = ""
    name: str = ""
    status: SubscriptionStatus = SubscriptionStatus.DRAFT
    billing_interval: BillingInterval | None = None
    trial_ends_at: str | None = None
    start_date: str = ""
    end_date: str | None = None
    current_period_start: str | None = None
    current_period_end: str | None = None
    billing_day_of_month: int = 1
    checkout_url: str | None = None
    created_at: str = ""
    updated_at: str = ""
    intro_offer_ends_at: str | None = None
    intro_offer_discount_type: DiscountType | None = None
    intro_offer_discount_value: int | None = None


@dataclass
class SubscriptionListItem:
    id: str
    object: str = "subscription"
    livemode: bool = False
    customer_id: str = ""
    plan_id: str = ""
    plan_name: str = ""
    name: str = ""
    status: SubscriptionStatus = SubscriptionStatus.DRAFT
    start_date: str = ""
    end_date: str = ""
    billing_day_of_month: int = 1
    created_at: str = ""
    updated_at: str = ""


@dataclass
class PreviewChangeResult:
    current_plan_credit: int = 0
    new_plan_charge: int = 0
    estimated_total: int = 0
    effective_date: str = ""
    days_remaining: int = 0
    total_days: int = 0
    is_upgrade: bool = False


@dataclass
class ActivateAddonResult:
    addon_id: str = ""
    status: str = ""
    prorated_charge: int = 0


@dataclass
class DeactivateAddonResult:
    id: str
    status: str = ""
    deactivated_at: str = ""


@dataclass
class AdjustBalanceResult:
    amount: int = 0
    new_balance: int = 0
    reason: str | None = None


@dataclass
class TopupBalanceResult:
    amount: int = 0


@dataclass
class PurchaseCreditsResult:
    credits: int = 0


@dataclass
class WebhookTestResult:
    success: bool = False
    delivery_id: str = ""
    delivered_at: str = ""


# Dataclasses that appear as nested fields of other dataclasses. Registered so
# the parser can resolve their string annotations (e.g. "list[InvoiceLineItem]",
# "CreditsSummary | None") into typed objects when constructing the parent.
_NESTED_DATACLASSES: list[type[Any]] = [
    Customer,
    InvoiceLineItem,
    PlanPrice,
    PlanFeature,
    FeatureSummary,
    CreditsSummary,
    BalanceSummary,
    CancellationSummary,
    DiscountSummary,
]

_DATACLASS_TYPES.update({cls.__name__: cls for cls in _NESTED_DATACLASSES})
