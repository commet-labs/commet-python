from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ._http import ApiResponse
    from .async_resources.features import AsyncFeaturesResource
    from .async_resources.portal import AsyncPortalResource
    from .async_resources.seats import AsyncSeatsResource
    from .async_resources.subscriptions import AsyncSubscriptionsResource
    from .async_resources.usage import AsyncUsageResource
    from .types import (
        FeatureAccess,
        PortalSession,
        SeatBalance,
        SeatEvent,
        Subscription,
        UsageEvent,
    )


class AsyncCustomerContext:
    def __init__(
        self,
        customer_id: str,
        *,
        features: AsyncFeaturesResource,
        seats: AsyncSeatsResource,
        usage: AsyncUsageResource,
        subscriptions: AsyncSubscriptionsResource,
        portal: AsyncPortalResource,
    ) -> None:
        self._customer_id = customer_id
        self.features = _AsyncCustomerFeatures(customer_id, features)
        self.seats = _AsyncCustomerSeats(customer_id, seats)
        self.usage = _AsyncCustomerUsage(customer_id, usage)
        self.subscription = _AsyncCustomerSubscription(customer_id, subscriptions)
        self.portal = _AsyncCustomerPortal(customer_id, portal)


class _AsyncCustomerFeatures:
    def __init__(self, customer_id: str, resource: AsyncFeaturesResource) -> None:
        self._customer_id = customer_id
        self._resource = resource

    async def get(self, code: str) -> ApiResponse[FeatureAccess]:
        return await self._resource.get(code=code, customer_id=self._customer_id)

    async def check(self, code: str) -> ApiResponse[dict[str, bool]]:
        return await self._resource.check(code=code, customer_id=self._customer_id)

    async def can_use(self, code: str) -> ApiResponse[dict[str, bool | str | None]]:
        return await self._resource.can_use(code=code, customer_id=self._customer_id)

    async def list(self) -> ApiResponse[list[FeatureAccess]]:
        return await self._resource.list(self._customer_id)


class _AsyncCustomerSeats:
    def __init__(self, customer_id: str, resource: AsyncSeatsResource) -> None:
        self._customer_id = customer_id
        self._resource = resource

    async def add(self, seat_type: str, count: int = 1) -> ApiResponse[SeatEvent]:
        return await self._resource.add(
            seat_type=seat_type, count=count, customer_id=self._customer_id
        )

    async def remove(self, seat_type: str, count: int = 1) -> ApiResponse[SeatEvent]:
        return await self._resource.remove(
            seat_type=seat_type, count=count, customer_id=self._customer_id
        )

    async def set(self, seat_type: str, count: int) -> ApiResponse[SeatEvent]:
        return await self._resource.set(
            seat_type=seat_type, count=count, customer_id=self._customer_id
        )

    async def get_balance(self, seat_type: str) -> ApiResponse[SeatBalance]:
        return await self._resource.get_balance(
            seat_type=seat_type, customer_id=self._customer_id
        )


class _AsyncCustomerUsage:
    def __init__(self, customer_id: str, resource: AsyncUsageResource) -> None:
        self._customer_id = customer_id
        self._resource = resource

    async def track(
        self,
        feature: str,
        value: int | None = None,
        properties: dict[str, str] | None = None,
    ) -> ApiResponse[UsageEvent]:
        return await self._resource.track(
            feature=feature, customer_id=self._customer_id, value=value, properties=properties
        )


class _AsyncCustomerSubscription:
    def __init__(self, customer_id: str, resource: AsyncSubscriptionsResource) -> None:
        self._customer_id = customer_id
        self._resource = resource

    async def get(self) -> ApiResponse[Subscription]:
        return await self._resource.get(self._customer_id)


class _AsyncCustomerPortal:
    def __init__(self, customer_id: str, resource: AsyncPortalResource) -> None:
        self._customer_id = customer_id
        self._resource = resource

    async def get_url(self) -> ApiResponse[PortalSession]:
        return await self._resource.get_url(customer_id=self._customer_id)
