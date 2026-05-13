from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, TypeVar

T = TypeVar("T")


def _from_dict(cls: type[T], data: dict[str, Any]) -> T:
    if not isinstance(data, dict):
        return data  # type: ignore[return-value]
    fields = {f.name for f in cls.__dataclass_fields__.values()}  # type: ignore[attr-defined]
    return cls(**{k: v for k, v in data.items() if k in fields})


def _from_list(cls: type[T], data: list[dict[str, Any]]) -> list[T]:
    return [_from_dict(cls, item) for item in data]


@dataclass
class Customer:
    id: str
    organization_id: str = ""
    external_id: str | None = None
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
    customer_id: str = ""
    plan_id: str | None = None
    plan_name: str | None = None
    name: str = ""
    description: str | None = None
    status: str = ""
    consumption_model: str | None = None
    billing_interval: str | None = None
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
    next_billing_date: str | None = None
    created_at: str = ""
    updated_at: str = ""


@dataclass
class Feature:
    code: str
    name: str = ""
    type: str = ""
    unit_name: str | None = None
    enabled: bool | None = None
    included_amount: int | None = None
    unlimited: bool | None = None
    overage_enabled: bool | None = None
    overage_unit_price: int | None = None


@dataclass
class FeatureAccess:
    code: str
    name: str = ""
    type: str = ""
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
    organization_id: str = ""
    customer_id: str = ""
    seat_type: str = ""
    event_type: str = ""
    quantity: int = 0
    previous_balance: int | None = None
    new_balance: int = 0
    ts: str = ""
    created_at: str = ""


@dataclass
class CreditPack:
    id: str
    name: str = ""
    description: str | None = None
    credits: int = 0
    price: int = 0
    currency: str = ""


@dataclass
class PortalSession:
    success: bool = False
    message: str = ""
    portal_url: str = ""


@dataclass
class UsageEvent:
    id: str
    organization_id: str = ""
    customer_id: str = ""
    feature: str = ""
    idempotency_key: str | None = None
    ts: str = ""
    properties: list[dict[str, str]] | None = None
    created_at: str = ""
