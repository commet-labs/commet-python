# ruff: noqa: E501

from __future__ import annotations

from typing import Literal

from .._async_http import AsyncCommetHTTPClient
from .._shared import build_body
from ..types import (
    BalanceAdjustment,
    BalanceTopup,
    CreatedSubscription,
    CreditGrant,
    DeletedSubscriptionAddon,
    PaymentMethodUpdateCheckout,
    PlanChange,
    PreviewChange,
    ReactivatedSubscription,
    RecoveryLink,
    Subscription,
    SubscriptionAddon,
    SubscriptionsListResult,
    SubscriptionStatus,
    _parse_data,
    _parse_union_data,
)


class AsyncSubscriptionsResource:
    def __init__(self, http: AsyncCommetHTTPClient) -> None:
        self._http = http

    async def deactivate_addon(self, id: str, addon_id: str) -> DeletedSubscriptionAddon:
        """Deactivate an add-on from a subscription."""
        return _parse_data(
            await self._http.delete(f"/subscriptions/{id}/addons/{addon_id}"),
            DeletedSubscriptionAddon,
        )

    async def activate_addon(
        self, id: str, *, addon_id: str, idempotency_key: str | None = None
    ) -> SubscriptionAddon:
        """Activate an add-on on a subscription. Charges a prorated amount for the current billing period."""
        body = build_body(addon_id=addon_id)
        return _parse_data(
            await self._http.post(
                f"/subscriptions/{id}/addons", body, idempotency_key=idempotency_key
            ),
            SubscriptionAddon,
        )

    async def adjust_balance(
        self,
        id: str,
        *,
        amount: int,
        reason: str | None = None,
        type: Literal["credits", "balance"] | None = None,
        idempotency_key: str | None = None,
    ) -> BalanceAdjustment:
        """Adjust a subscription's balance or credits by a signed amount. Positive adds, negative subtracts."""
        body = build_body(amount=amount, reason=reason, type=type)
        return _parse_data(
            await self._http.post(
                f"/subscriptions/{id}/balance/adjust", body, idempotency_key=idempotency_key
            ),
            BalanceAdjustment,
        )

    async def topup_balance(
        self, id: str, *, amount: int, idempotency_key: str | None = None
    ) -> BalanceTopup:
        """Top up a subscription's balance. Charges the customer's payment method for the specified amount."""
        body = build_body(amount=amount)
        return _parse_data(
            await self._http.post(
                f"/subscriptions/{id}/balance/topup", body, idempotency_key=idempotency_key
            ),
            BalanceTopup,
        )

    async def cancel(
        self,
        id: str,
        *,
        reason: str | None = None,
        immediate: bool | None = None,
        idempotency_key: str | None = None,
    ) -> Subscription:
        """Cancel immediately or at period end and return the updated subscription."""
        body = build_body(reason=reason, immediate=immediate)
        return _parse_data(
            await self._http.post(
                f"/subscriptions/{id}/cancel", body, idempotency_key=idempotency_key
            ),
            Subscription,
        )

    async def change_plan(
        self,
        id: str,
        *,
        new_plan_id: str | None = None,
        new_billing_interval: Literal["weekly", "monthly", "quarterly", "yearly"] | None = None,
        success_url: str | None = None,
        offer_id: str | None = None,
        idempotency_key: str | None = None,
    ) -> PlanChange:
        """Upgrade or change billing interval immediately, optionally applying a quoted Promotional Offer. Scheduled changes do not accept offers."""
        body = build_body(
            new_plan_id=new_plan_id,
            new_billing_interval=new_billing_interval,
            success_url=success_url,
            offer_id=offer_id,
        )
        return _parse_union_data(
            await self._http.post(
                f"/subscriptions/{id}/change-plan", body, idempotency_key=idempotency_key
            ),
            "PlanChange",
        )

    async def purchase_credits(
        self, id: str, *, credit_pack_id: str, idempotency_key: str | None = None
    ) -> CreditGrant:
        """Purchase a credit pack for a subscription. Charges the customer and adds credits to their balance."""
        body = build_body(credit_pack_id=credit_pack_id)
        return _parse_data(
            await self._http.post(
                f"/subscriptions/{id}/credits", body, idempotency_key=idempotency_key
            ),
            CreditGrant,
        )

    async def update_payment_method(
        self, id: str, *, success_url: str | None = None, idempotency_key: str | None = None
    ) -> PaymentMethodUpdateCheckout:
        """Creates a hosted checkout session for the customer to update the subscription's default payment method."""
        body = build_body(success_url=success_url)
        return _parse_data(
            await self._http.post(
                f"/subscriptions/{id}/payment-method/update", body, idempotency_key=idempotency_key
            ),
            PaymentMethodUpdateCheckout,
        )

    async def preview_change(
        self,
        id: str,
        *,
        plan_id: str,
        billing_interval: Literal["weekly", "monthly", "quarterly", "yearly", "one_time"]
        | None = None,
        offer_id: str | None = None,
        idempotency_key: str | None = None,
    ) -> PreviewChange:
        """Preview proration details for an immediate plan change (a higher-sort-order plan or a longer interval) without applying it. Returns credit, charge, and net amount. The target plan must belong to the same plan group as the current plan, otherwise a 400 with code `plans_not_in_same_group` is returned. A change between two free plans has nothing to prorate and returns a zero-amount estimate. Downgrades — a lower-sort-order plan in the same group, or a shorter interval — are scheduled for the end of the current period instead of being prorated, so they return a 400 with code `plan_change_scheduled`; apply those via the change-plan endpoint. Pass offerId to quote the destination plan with a Promotional Offer."""
        body = build_body(plan_id=plan_id, billing_interval=billing_interval, offer_id=offer_id)
        return _parse_data(
            await self._http.post(
                f"/subscriptions/{id}/preview-change", body, idempotency_key=idempotency_key
            ),
            PreviewChange,
        )

    async def reactivate(
        self, id: str, *, offer_id: str | None = None, idempotency_key: str | None = None
    ) -> ReactivatedSubscription:
        """Reactivates a subscription. A past_due subscription retries its outstanding renewal charge (recovering to active on success). A canceled subscription generates a fresh invoice, charges the saved card, and resets the billing period. On a successful charge the subscription becomes active; a declined charge returns an error with a recoveryUrl in the error details that can be sent to the customer to update their card. A canceled subscription may apply a Promotional Offer by offerId; past-due recovery cannot."""
        body = build_body(offer_id=offer_id)
        return _parse_data(
            await self._http.post(
                f"/subscriptions/{id}/reactivate", body, idempotency_key=idempotency_key
            ),
            ReactivatedSubscription,
        )

    async def create_recovery_link(
        self, id: str, *, idempotency_key: str | None = None
    ) -> RecoveryLink:
        """Generates a hosted, signed recovery link that lets the customer pay the outstanding renewal charge for a past_due subscription. Unlike reactivate, which charges server-to-server, this returns a link the merchant can deliver through their own email, SMS, or dashboard. The link carries a self-contained signed token and stays valid until the charge is paid or the subscription is no longer past due."""
        return _parse_data(
            await self._http.post(
                f"/subscriptions/{id}/recovery-links", idempotency_key=idempotency_key
            ),
            RecoveryLink,
        )

    async def get(self, id: str) -> Subscription:
        """Get a subscription by its public ID, regardless of status (including pending_payment and past_due)."""
        return _parse_data(await self._http.get(f"/subscriptions/{id}"), Subscription)

    async def uncancel(self, id: str, *, idempotency_key: str | None = None) -> Subscription:
        """Revert a scheduled cancellation and return the updated subscription. Only works before cancellation takes effect."""
        return _parse_data(
            await self._http.post(f"/subscriptions/{id}/uncancel", idempotency_key=idempotency_key),
            Subscription,
        )

    async def get_active(self, *, customer_id: str) -> Subscription | None:
        """Get the active subscription for a customer. Returns null if none."""
        query = build_body(customer_id=customer_id)
        return _parse_data(await self._http.get("/subscriptions/active", query), Subscription)

    async def list(
        self, *, customer_id: str | None = None, status: SubscriptionStatus | None = None
    ) -> SubscriptionsListResult:
        """List all subscriptions. Filter by customer ID or status."""
        query = build_body(customer_id=customer_id, status=status)
        return _parse_data(await self._http.get("/subscriptions", query), SubscriptionsListResult)

    async def create(
        self,
        *,
        customer_id: str,
        billing_interval: Literal["weekly", "monthly", "quarterly", "yearly", "one_time"]
        | None = None,
        price_id: str | None = None,
        initial_seats: dict[str, int] | None = None,
        provider: Literal["stripe", "commet", "dlocal"] | None = None,
        name: str | None = None,
        start_date: str | None = None,
        success_url: str | None = None,
        offer_id: str | None = None,
        promo_code: str | None = None,
        custom_trial_days: int | None = None,
        skip_trial: bool | None = None,
        plan_id: str | None = None,
        plan_code: str | None = None,
        idempotency_key: str | None = None,
    ) -> CreatedSubscription:
        """Create a subscription for a customer. Commet selects the default price when priceId is omitted and resolves its market from the customer's billing country. Without an offer override, Commet applies the price's automatic introductory offer. Pass one Promotional Offer through offerId to override it. Experiment assignment remains external."""
        body = build_body(
            customer_id=customer_id,
            billing_interval=billing_interval,
            price_id=price_id,
            initial_seats=initial_seats,
            provider=provider,
            name=name,
            start_date=start_date,
            success_url=success_url,
            offer_id=offer_id,
            promo_code=promo_code,
            custom_trial_days=custom_trial_days,
            skip_trial=skip_trial,
            plan_id=plan_id,
            plan_code=plan_code,
        )
        return _parse_data(
            await self._http.post("/subscriptions", body, idempotency_key=idempotency_key),
            CreatedSubscription,
        )
