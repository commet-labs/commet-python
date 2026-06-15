from __future__ import annotations

from dataclasses import dataclass


@dataclass
class WebhookPlanRef:
    id: str = ""
    name: str = ""


@dataclass
class WebhookAddonRef:
    id: str = ""
    name: str = ""


@dataclass
class WebhookCardInfo:
    brand: str = ""
    last4: str = ""
    expMonth: int = 0
    expYear: int = 0


@dataclass
class WebhookBankRef:
    bankName: str = ""
    last4: str = ""


@dataclass
class WebhookFeatureAccess:
    code: str = ""
    name: str = ""
    type: str = ""
    allowed: bool = False
    enabled: bool | None = None
    current: float | None = None
    included: float | None = None
    remaining: float | None = None
    overageQuantity: float | None = None
    overageUnitPrice: float | None = None
    unlimited: bool | None = None
    overageEnabled: bool | None = None
    billedQuantity: float | None = None


@dataclass
class WebhookSeatSummary:
    code: str = ""
    current: float | None = None
    included: float | None = None
    remaining: float | None = None
    unlimited: bool | None = None


@dataclass
class WebhookCreditsBalance:
    planCredits: float = 0.0
    purchasedCredits: float = 0.0
    totalCredits: float = 0.0


@dataclass
class WebhookBalance:
    currentBalance: float = 0.0


_AUX_TYPES = (
    WebhookPlanRef,
    WebhookAddonRef,
    WebhookCardInfo,
    WebhookBankRef,
    WebhookFeatureAccess,
    WebhookSeatSummary,
    WebhookCreditsBalance,
    WebhookBalance,
)


def _register() -> None:
    from .types import _DATACLASS_TYPES

    for cls in _AUX_TYPES:
        _DATACLASS_TYPES.setdefault(cls.__name__, cls)


_register()


__all__ = [
    "WebhookAddonRef",
    "WebhookBalance",
    "WebhookBankRef",
    "WebhookCardInfo",
    "WebhookCreditsBalance",
    "WebhookFeatureAccess",
    "WebhookPlanRef",
    "WebhookSeatSummary",
]
