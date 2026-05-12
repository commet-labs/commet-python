from ._exceptions import CommetAPIError, CommetError, CommetValidationError
from ._http import ApiResponse
from ._shared import API_VERSION
from .async_client import AsyncCommet
from .client import Commet
from .resources.webhooks import Webhooks
from .types import (
    CreditPack,
    Customer,
    Feature,
    FeatureAccess,
    Plan,
    PortalSession,
    SeatBalance,
    SeatEvent,
    Subscription,
    UsageEvent,
)

try:
    from importlib.metadata import version

    __version__ = version("commet-sdk")
except Exception:
    __version__ = "0.1.0"

__all__ = [
    "__version__",
    "API_VERSION",
    "ApiResponse",
    "AsyncCommet",
    "Commet",
    "CommetAPIError",
    "CommetError",
    "CommetValidationError",
    "CreditPack",
    "Customer",
    "Feature",
    "FeatureAccess",
    "Plan",
    "PortalSession",
    "SeatBalance",
    "SeatEvent",
    "Subscription",
    "UsageEvent",
    "Webhooks",
]
