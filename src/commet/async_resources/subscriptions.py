# ruff: noqa: E501

from __future__ import annotations

from typing import Literal

from .._async_http import AsyncCommetHTTPClient
from .._http import ApiResponse
from .._shared import build_body
from ..types import (
    BalanceAdjustment,
    BalanceTopup,
    BillingInterval,
    CanceledSubscription,
    CreateSubscriptionParamsIntroOffer,
    CreditGrant,
    DeletedSubscriptionAddon,
    PaymentMethodUpdateCheckout,
    PlanChange,
    PreviewChange,
    ReactivatedSubscription,
    RecoveryLink,
    Subscription,
    SubscriptionAddon,
    SubscriptionStatus,
    UncanceledSubscription,
    _parse,
    _parse_list,
)


class AsyncSubscriptionsResource:
    def __init__(self, http: AsyncCommetHTTPClient) -> None:
        self._http = http

    async def list(
        self, *, customer_id: str | None = None, status: SubscriptionStatus | None = None
    ) -> ApiResponse[list[Subscription]]:
        """List all subscriptions. Filter by customer ID or status."""
        query = build_body(customer_id=customer_id, status=status)
        return _parse_list(await self._http.get("/subscriptions", query), Subscription)

    async def create(
        self,
        *,
        customer_id: str,
        plan_id: str | None = None,
        plan_code: str | None = None,
        billing_interval: BillingInterval | None = None,
        initial_seats: dict[str, int] | None = None,
        skip_trial: bool | None = None,
        custom_trial_days: int | None = None,
        intro_offer: CreateSubscriptionParamsIntroOffer | None = None,
        name: str | None = None,
        start_date: str | None = None,
        success_url: str | None = None,
        idempotency_key: str | None = None,
    ) -> ApiResponse[Subscription]:
        """Create a subscription for a customer. Requires planId or planCode plus customerId."""
        body = build_body(
            plan_id=plan_id,
            plan_code=plan_code,
            customer_id=customer_id,
            billing_interval=billing_interval,
            initial_seats=initial_seats,
            skip_trial=skip_trial,
            custom_trial_days=custom_trial_days,
            intro_offer=intro_offer,
            name=name,
            start_date=start_date,
            success_url=success_url,
        )
        return _parse(
            await self._http.post("/subscriptions", body, idempotency_key=idempotency_key),
            Subscription,
        )

    async def get(self, id: str) -> ApiResponse[Subscription]:
        """Get a subscription by its public ID, regardless of status (including pending_payment and past_due)."""
        return _parse(await self._http.get(f"/subscriptions/{id}"), Subscription)

    async def get_active(self, *, customer_id: str) -> ApiResponse[Subscription | None]:
        """Get the active subscription for a customer. Returns null if none."""
        query = build_body(customer_id=customer_id)
        return _parse(await self._http.get("/subscriptions/active", query), Subscription)

    async def cancel(
        self,
        id: str,
        *,
        reason: str | None = None,
        immediate: bool | None = None,
        idempotency_key: str | None = None,
    ) -> ApiResponse[CanceledSubscription]:
        """Cancel immediately or at period end."""
        body = build_body(reason=reason, immediate=immediate)
        return _parse(
            await self._http.post(
                f"/subscriptions/{id}/cancel", body, idempotency_key=idempotency_key
            ),
            CanceledSubscription,
        )

    async def uncancel(
        self, id: str, *, idempotency_key: str | None = None
    ) -> ApiResponse[UncanceledSubscription]:
        """Revert a scheduled cancellation. Only works when canceledAt is set but status is not yet 'canceled'."""
        return _parse(
            await self._http.post(f"/subscriptions/{id}/uncancel", idempotency_key=idempotency_key),
            UncanceledSubscription,
        )

    async def reactivate(
        self, id: str, *, idempotency_key: str | None = None
    ) -> ApiResponse[ReactivatedSubscription]:
        """Reactivates a subscription. A past_due subscription retries its outstanding renewal charge (recovering to active on success). A canceled subscription generates a fresh invoice, charges the saved card, and resets the billing period. On a successful charge the subscription becomes active; a declined charge returns an error with a recoveryUrl in the error details that can be sent to the customer to update their card."""
        return _parse(
            await self._http.post(
                f"/subscriptions/{id}/reactivate", idempotency_key=idempotency_key
            ),
            ReactivatedSubscription,
        )

    async def create_recovery_link(
        self, id: str, *, idempotency_key: str | None = None
    ) -> ApiResponse[RecoveryLink]:
        """Generates a hosted, signed recovery link that lets the customer pay the outstanding renewal charge for a past_due subscription. Unlike reactivate, which charges server-to-server, this returns a link the merchant can deliver through their own email, SMS, or dashboard. The link carries a self-contained signed token and stays valid until the charge is paid or the subscription is no longer past due."""
        return _parse(
            await self._http.post(
                f"/subscriptions/{id}/recovery-link", idempotency_key=idempotency_key
            ),
            RecoveryLink,
        )

    async def update_payment_method(
        self, id: str, *, success_url: str | None = None, idempotency_key: str | None = None
    ) -> ApiResponse[PaymentMethodUpdateCheckout]:
        """Creates a hosted checkout session for the customer to update the subscription's default payment method."""
        body = build_body(success_url=success_url)
        return _parse(
            await self._http.post(
                f"/subscriptions/{id}/payment-method/update", body, idempotency_key=idempotency_key
            ),
            PaymentMethodUpdateCheckout,
        )

    async def change_plan(
        self,
        id: str,
        *,
        new_plan_id: str | None = None,
        new_billing_interval: Literal["weekly", "monthly", "quarterly", "yearly"] | None = None,
        success_url: str | None = None,
        idempotency_key: str | None = None,
    ) -> ApiResponse[PlanChange]:
        """Upgrade, downgrade, or change billing interval."""
        body = build_body(
            new_plan_id=new_plan_id,
            new_billing_interval=new_billing_interval,
            success_url=success_url,
        )
        return _parse(
            await self._http.post(
                f"/subscriptions/{id}/change-plan", body, idempotency_key=idempotency_key
            ),
            PlanChange,
        )

    async def preview_change(
        self,
        id: str,
        *,
        plan_id: str,
        billing_interval: BillingInterval | None = None,
        idempotency_key: str | None = None,
    ) -> ApiResponse[PreviewChange]:
        """Preview proration details for an immediate plan change (an upgrade or a longer interval) without applying it. Returns credit, charge, and net amount. The target plan must belong to the same plan group as the current plan, otherwise a 400 with code `plans_not_in_same_group` is returned. A change between two free plans has nothing to prorate and returns a zero-amount estimate. Downgrades — a cheaper plan in the same group, or a shorter interval — are scheduled for the end of the current period instead of being prorated, so they return a 400 with code `plan_change_scheduled`; apply those via the change-plan endpoint."""
        body = build_body(plan_id=plan_id, billing_interval=billing_interval)
        return _parse(
            await self._http.post(
                f"/subscriptions/{id}/preview-change", body, idempotency_key=idempotency_key
            ),
            PreviewChange,
        )

    async def activate_addon(
        self, id: str, *, addon_id: str, idempotency_key: str | None = None
    ) -> ApiResponse[SubscriptionAddon]:
        """Activate an add-on on a subscription. Charges a prorated amount for the current billing period."""
        body = build_body(addon_id=addon_id)
        return _parse(
            await self._http.post(
                f"/subscriptions/{id}/addons", body, idempotency_key=idempotency_key
            ),
            SubscriptionAddon,
        )

    async def deactivate_addon(
        self, id: str, addon_id: str
    ) -> ApiResponse[DeletedSubscriptionAddon]:
        """Deactivate an add-on from a subscription."""
        return _parse(
            await self._http.delete(f"/subscriptions/{id}/addons/{addon_id}"),
            DeletedSubscriptionAddon,
        )

    async def adjust_balance(
        self,
        id: str,
        *,
        amount: int,
        reason: str | None = None,
        type: Literal["credits", "balance"] | None = None,
        idempotency_key: str | None = None,
    ) -> ApiResponse[BalanceAdjustment]:
        """Adjust a subscription's balance or credits by a signed amount. Positive adds, negative subtracts."""
        body = build_body(amount=amount, reason=reason, type=type)
        return _parse(
            await self._http.post(
                f"/subscriptions/{id}/balance/adjust", body, idempotency_key=idempotency_key
            ),
            BalanceAdjustment,
        )

    async def topup_balance(
        self, id: str, *, amount: int, idempotency_key: str | None = None
    ) -> ApiResponse[BalanceTopup]:
        """Top up a subscription's balance. Charges the customer's payment method for the specified amount."""
        body = build_body(amount=amount)
        return _parse(
            await self._http.post(
                f"/subscriptions/{id}/balance/topup", body, idempotency_key=idempotency_key
            ),
            BalanceTopup,
        )

    async def purchase_credits(
        self, id: str, *, credit_pack_id: str, idempotency_key: str | None = None
    ) -> ApiResponse[CreditGrant]:
        """Purchase a credit pack for a subscription. Charges the customer and adds credits to their balance."""
        body = build_body(credit_pack_id=credit_pack_id)
        return _parse(
            await self._http.post(
                f"/subscriptions/{id}/credits", body, idempotency_key=idempotency_key
            ),
            CreditGrant,
        )
