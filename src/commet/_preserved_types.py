from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, TypeVar

from ._http import ApiResponse

_T = TypeVar("_T")

# Hand-written types for the preserved resources (usage, webhooks). These are NOT
# generated from the contract because usage and webhooks carry custom client
# logic (usage batching shapes, webhook HMAC verification) and are intentionally
# kept out of the codegen RESOURCES config. The shapes here mirror the API
# responses those endpoints return.


class UsageCheckDenialReason(str, Enum):
    INCLUDED_LIMIT_REACHED = "included_limit_reached"
    INSUFFICIENT_CREDITS = "insufficient_credits"
    INSUFFICIENT_BALANCE = "insufficient_balance"


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
class UsageCheckResult:
    allowed: bool = False
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
class WebhookTestResult:
    success: bool = False
    delivery_id: str = ""
    delivered_at: str = ""


@dataclass
class DeleteResult:
    id: str
    deleted: bool = True


# Register the preserved dataclasses so the shared deserializer (_from_dict) can
# resolve any nested refs by name, exactly like the generated dataclasses.
def _register() -> None:
    from .types import _DATACLASS_TYPES, _ENUM_TYPES

    _ENUM_TYPES.setdefault("UsageCheckDenialReason", UsageCheckDenialReason)
    for cls in (
        UsageEvent,
        UsageCheckResult,
        WebhookEndpoint,
        WebhookEndpointCreated,
        WebhookTestResult,
        DeleteResult,
    ):
        _DATACLASS_TYPES.setdefault(cls.__name__, cls)


_register()

__all__ = [
    "DeleteResult",
    "UsageCheckDenialReason",
    "UsageCheckResult",
    "UsageEvent",
    "WebhookEndpoint",
    "WebhookEndpointCreated",
    "WebhookTestResult",
]


# Re-export the shared deserializer helpers from the generated types module so
# preserved resources can parse responses without importing the wire converter.
def _parse(response: ApiResponse[Any], cls: type[_T]) -> ApiResponse[_T]:
    from .types import _parse as _shared_parse

    return _shared_parse(response, cls)


def _parse_list(response: ApiResponse[Any], cls: type[_T]) -> ApiResponse[list[_T]]:
    from .types import _parse_list as _shared_parse_list

    return _shared_parse_list(response, cls)
