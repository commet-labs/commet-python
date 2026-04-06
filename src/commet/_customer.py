from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ._http import ApiResponse
    from .resources.features import FeaturesResource
    from .resources.portal import PortalResource
    from .resources.seats import SeatsResource
    from .resources.subscriptions import SubscriptionsResource
    from .resources.usage import UsageResource


class CustomerContext:
    """Customer-scoped API context.

    All operations are automatically scoped to the customer's external_id.

    Usage::

        customer = commet.customer("user_123")

        customer.features.get("team_members")
        customer.seats.add("editor")
        customer.usage.track("api_calls")
    """

    def __init__(
        self,
        external_id: str,
        *,
        features: FeaturesResource,
        seats: SeatsResource,
        usage: UsageResource,
        subscriptions: SubscriptionsResource,
        portal: PortalResource,
    ) -> None:
        self._external_id = external_id
        self.features = _CustomerFeatures(external_id, features)
        self.seats = _CustomerSeats(external_id, seats)
        self.usage = _CustomerUsage(external_id, usage)
        self.subscription = _CustomerSubscription(external_id, subscriptions)
        self.portal = _CustomerPortal(external_id, portal)


class _CustomerFeatures:
    def __init__(self, external_id: str, resource: FeaturesResource) -> None:
        self._external_id = external_id
        self._resource = resource

    def get(self, code: str) -> ApiResponse:
        return self._resource.get(code=code, external_id=self._external_id)

    def check(self, code: str) -> ApiResponse:
        return self._resource.check(code=code, external_id=self._external_id)

    def can_use(self, code: str) -> ApiResponse:
        return self._resource.can_use(code=code, external_id=self._external_id)

    def list(self) -> ApiResponse:
        return self._resource.list(self._external_id)


class _CustomerSeats:
    def __init__(self, external_id: str, resource: SeatsResource) -> None:
        self._external_id = external_id
        self._resource = resource

    def add(self, seat_type: str, count: int = 1) -> ApiResponse:
        return self._resource.add(
            seat_type=seat_type, count=count, external_id=self._external_id
        )

    def remove(self, seat_type: str, count: int = 1) -> ApiResponse:
        return self._resource.remove(
            seat_type=seat_type, count=count, external_id=self._external_id
        )

    def set(self, seat_type: str, count: int) -> ApiResponse:
        return self._resource.set(
            seat_type=seat_type, count=count, external_id=self._external_id
        )

    def get_balance(self, seat_type: str) -> ApiResponse:
        return self._resource.get_balance(seat_type=seat_type, external_id=self._external_id)


class _CustomerUsage:
    def __init__(self, external_id: str, resource: UsageResource) -> None:
        self._external_id = external_id
        self._resource = resource

    def track(
        self,
        feature: str,
        value: int | None = None,
        properties: dict[str, str] | None = None,
    ) -> ApiResponse:
        return self._resource.track(
            feature=feature, external_id=self._external_id, value=value, properties=properties
        )


class _CustomerSubscription:
    def __init__(self, external_id: str, resource: SubscriptionsResource) -> None:
        self._external_id = external_id
        self._resource = resource

    def get(self) -> ApiResponse:
        return self._resource.get(self._external_id)


class _CustomerPortal:
    def __init__(self, external_id: str, resource: PortalResource) -> None:
        self._external_id = external_id
        self._resource = resource

    def get_url(self) -> ApiResponse:
        return self._resource.get_url(external_id=self._external_id)
