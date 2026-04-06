from ._exceptions import CommetAPIError, CommetError, CommetValidationError
from ._http import ApiResponse
from .client import Commet
from .resources.webhooks import Webhooks

try:
    from importlib.metadata import version

    __version__ = version("commet")
except Exception:
    __version__ = "0.1.0"

__all__ = [
    "__version__",
    "ApiResponse",
    "Commet",
    "CommetAPIError",
    "CommetError",
    "CommetValidationError",
    "Webhooks",
]
