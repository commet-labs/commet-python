# ruff: noqa: E501


from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .types import (
    _DATACLASS_TYPES,
    WebhookAddonRef,
    WebhookBalance,
    WebhookBankRef,
    WebhookCardInfo,
    WebhookCreditsBalance,
    WebhookFeatureAccess,
    WebhookPlanRef,
    WebhookSeatSummary,
    _from_dict,
)


class WebhookEventType:
    SUBSCRIPTION_CREATED = "subscription.created"
    SUBSCRIPTION_ACTIVATED = "subscription.activated"
    SUBSCRIPTION_REACTIVATED = "subscription.reactivated"
    SUBSCRIPTION_CANCELED = "subscription.canceled"
    SUBSCRIPTION_UPDATED = "subscription.updated"
    SUBSCRIPTION_PLAN_CHANGED = "subscription.plan_changed"
    SUBSCRIPTION_CANCELLATION_SCHEDULED = "subscription.cancellation_scheduled"
    SUBSCRIPTION_CANCELLATION_REVOKED = "subscription.cancellation_revoked"
    SUBSCRIPTION_PLAN_CHANGE_SCHEDULED = "subscription.plan_change_scheduled"
    SUBSCRIPTION_PLAN_CHANGE_REVOKED = "subscription.plan_change_revoked"
    SUBSCRIPTION_PAST_DUE = "subscription.past_due"
    TRIAL_STARTED = "trial.started"
    TRIAL_CONVERTED = "trial.converted"
    TRIAL_EXPIRED = "trial.expired"
    TRIAL_WILL_END = "trial.will_end"
    TRIAL_CHECKOUT_READY = "trial.checkout_ready"
    CHECKOUT_READY = "checkout.ready"
    PAYMENT_RECEIVED = "payment.received"
    PAYMENT_FAILED = "payment.failed"
    PAYMENT_RECOVERED = "payment.recovered"
    PAYMENT_RETRY_FAILED = "payment.retry_failed"
    PAYMENT_REFUNDED = "payment.refunded"
    PAYMENT_DISPUTED = "payment.disputed"
    PAYMENT_DISPUTE_RESOLVED = "payment.dispute_resolved"
    PAYMENT_LINK_CREATED = "payment_link.created"
    PAYMENT_LINK_COMPLETED = "payment_link.completed"
    PAYMENT_LINK_FAILED = "payment_link.failed"
    PAYMENT_LINK_CANCELED = "payment_link.canceled"
    INVOICE_CREATED = "invoice.created"
    INVOICE_VOIDED = "invoice.voided"
    INVOICE_OVERDUE = "invoice.overdue"
    INVOICE_UPCOMING = "invoice.upcoming"
    PAYMENT_METHOD_ATTACHED = "payment_method.attached"
    PAYMENT_METHOD_UPDATED = "payment_method.updated"
    CUSTOMER_CREATED = "customer.created"
    CUSTOMER_UPDATED = "customer.updated"
    CUSTOMER_STATE_CHANGED = "customer.state_changed"
    CREDITS_GRANTED = "credits.granted"
    CREDITS_PURCHASED = "credits.purchased"
    CREDITS_LOW = "credits.low"
    CREDITS_DEPLETED = "credits.depleted"
    CREDITS_EXPIRED = "credits.expired"
    BALANCE_TOPPED_UP = "balance.topped_up"
    BALANCE_LOW = "balance.low"
    BALANCE_DEPLETED = "balance.depleted"
    QUOTA_THRESHOLD_REACHED = "quota.threshold_reached"
    QUOTA_EXCEEDED = "quota.exceeded"
    SEATS_UPDATED = "seats.updated"
    SEATS_LIMIT_REACHED = "seats.limit_reached"
    ADDON_ACTIVATED = "addon.activated"
    ADDON_DEACTIVATED = "addon.deactivated"
    USAGE_RECORDED = "usage.recorded"
    PAYOUT_AVAILABLE = "payout.available"
    PAYOUT_CREATED = "payout.created"
    PAYOUT_PAID = "payout.paid"
    PAYOUT_FAILED = "payout.failed"


@dataclass
class SubscriptionCreatedData:
    """Fired when a subscription record is created with status pending_payment. The first charge has not been confirmed yet — do NOT grant access here. Wait for subscription.activated."""

    subscriptionId: str = ""
    customerId: str = ""
    planId: str = ""
    planName: str = ""
    status: str = ""
    startDate: str = ""
    name: str | None = None


@dataclass
class SubscriptionActivatedData:
    """Fired when the first charge succeeds and status becomes active (or trialing if a trial is configured). This is where you grant access."""

    subscriptionId: str = ""
    customerId: str = ""
    status: str = ""
    currentPeriodStart: str | None = None
    currentPeriodEnd: str | None = None
    name: str | None = None
    invoiceId: str = ""
    invoiceNumber: str = ""
    invoiceTotal: float = 0.0
    invoiceCurrency: str = ""


@dataclass
class SubscriptionReactivatedData:
    """Fired when a canceled subscription is reactivated and its reactivation charge succeeds. The subscription returns to active with a fresh invoice and a billing period anchored to the reactivation date. Distinct from subscription.activated (first activation) and payment.recovered (past_due recovery, which keeps the original anchor)."""

    subscriptionId: str = ""
    customerId: str = ""
    status: str = ""
    currentPeriodStart: str | None = None
    currentPeriodEnd: str | None = None
    name: str | None = None
    invoiceId: str = ""
    invoiceNumber: str = ""
    invoiceTotal: float = 0.0
    invoiceCurrency: str = ""


@dataclass
class SubscriptionCanceledData:
    """Fired when a subscription is actually terminated at the end of the billing period. The status is now canceled and access should be revoked. This event is NOT fired when cancellation is scheduled — that triggers subscription.updated instead. See the cancellation lifecycle below."""

    subscriptionId: str = ""
    customerId: str = ""
    status: str = ""
    canceledAt: str | None = None
    cancelReason: str | None = None
    endDate: str | None = None


@dataclass
class SubscriptionUpdatedData:
    """Fired when subscription details change. The most common trigger is scheduling a cancellation — when a customer cancels, the status stays "active" until the billing period ends, but canceledAt and endDate are set immediately. Use this event to show "your subscription will end on {endDate}" in your UI. Access should NOT be revoked here — wait for subscription.canceled."""

    subscriptionId: str = ""
    customerId: str = ""
    status: str = ""
    canceledAt: str | None = None
    cancelReason: str | None = None
    endDate: str | None = None


@dataclass
class SubscriptionPlanChangedData:
    """Fired when a subscription changes from one plan to another, including upgrades, downgrades, and billing interval changes. Access does not change on this event — the subscription stays active."""

    subscriptionId: str = ""
    customerId: str = ""
    previousPlan: WebhookPlanRef = field(default_factory=WebhookPlanRef)
    currentPlan: WebhookPlanRef = field(default_factory=WebhookPlanRef)
    billingInterval: str | None = None
    credit: float = 0.0
    charge: float = 0.0
    totalCharged: float = 0.0


@dataclass
class SubscriptionCancellationScheduledData:
    """Fired when a cancellation is scheduled for the end of the billing period. The subscription stays active until effectiveAt — do NOT revoke access here. subscription.updated also fires for backward compatibility."""

    subscriptionId: str = ""
    customerId: str = ""
    status: str = ""
    canceledAt: str | None = None
    cancelReason: str | None = None
    effectiveAt: str = ""


@dataclass
class SubscriptionCancellationRevokedData:
    """Fired when a scheduled cancellation is reverted before it executes. The subscription continues on its current plan and billing period as if it had never been canceled."""

    subscriptionId: str = ""
    customerId: str = ""
    status: str = ""
    currentPeriodEnd: str | None = None


@dataclass
class SubscriptionPlanChangeScheduledData:
    """Fired when a plan change (downgrade or shorter interval) is scheduled for the end of the billing period. The subscription stays on the current plan until effectiveAt, when subscription.plan_changed fires."""

    subscriptionId: str = ""
    customerId: str = ""
    status: str = ""
    currentPlan: WebhookPlanRef = field(default_factory=WebhookPlanRef)
    scheduledPlan: WebhookPlanRef = field(default_factory=WebhookPlanRef)
    billingInterval: str | None = None
    scheduledBillingInterval: str | None = None
    effectiveAt: str = ""


@dataclass
class SubscriptionPlanChangeRevokedData:
    """Fired when a scheduled plan change is replaced by a different one before it executes. The replacement also fires subscription.plan_change_scheduled with the new target plan."""

    subscriptionId: str = ""
    customerId: str = ""
    status: str = ""
    currentPlan: WebhookPlanRef = field(default_factory=WebhookPlanRef)
    revokedPlan: WebhookPlanRef = field(default_factory=WebhookPlanRef)
    billingInterval: str | None = None
    revokedBillingInterval: str | None = None


@dataclass
class SubscriptionPastDueData:
    """Fired when a recurring payment fails on a previously paid subscription and its status becomes past_due. Access is cut immediately for past_due subscriptions — use this to notify the customer and recover the payment."""

    subscriptionId: str = ""
    customerId: str = ""
    status: str = ""
    invoiceId: str = ""
    invoiceNumber: str = ""


@dataclass
class TrialStartedData:
    """Fired when a subscription enters its trial period after checkout. Grant access here — trialing subscriptions have full access until trialEndsAt."""

    subscriptionId: str = ""
    customerId: str = ""
    status: str = ""
    planId: str = ""
    planName: str = ""
    trialEndsAt: str = ""


@dataclass
class TrialConvertedData:
    """Fired when a trialing customer converts to a paid subscription before the trial ends — today this happens when they change plan during the trial, which charges the full new plan price immediately. Trials that simply run out fire trial.expired instead."""

    subscriptionId: str = ""
    customerId: str = ""
    status: str = ""
    planId: str = ""
    planName: str = ""


@dataclass
class TrialExpiredData:
    """Fired when a trial period runs out and the billing cycle activates the subscription. The first regular invoice is generated right after — this is the natural trial-to-paid transition."""

    subscriptionId: str = ""
    customerId: str = ""
    status: str = ""
    planId: str = ""
    planName: str = ""
    trialEndsAt: str = ""


@dataclass
class TrialWillEndData:
    """Predictive event fired once, 3 days before a trial ends. Use it to remind the customer that billing starts soon. Emitted by a daily scan with a deterministic idempotency key, so it never fires twice for the same trial end date."""

    subscriptionId: str = ""
    customerId: str = ""
    status: str = ""
    planId: str = ""
    planName: str = ""
    trialEndsAt: str = ""


@dataclass
class TrialCheckoutReadyData:
    """Fired when a trial checkout link is ready to share with the customer. Completing this checkout saves a payment method and starts the trial (trial.started) — the customer is not charged until the trial ends."""

    subscriptionId: str = ""
    customerId: str = ""
    planName: str = ""
    trialDays: float = 0.0
    checkoutUrl: str = ""


@dataclass
class CheckoutReadyData:
    """Fired when a checkout link for a subscription's first invoice is ready to share with the customer. Commet also emails the link — use this event to deliver it through your own channels."""

    subscriptionId: str = ""
    customerId: str = ""
    invoiceId: str = ""
    invoiceNumber: str = ""
    invoiceTotal: float = 0.0
    invoiceCurrency: str = ""
    checkoutUrl: str = ""


@dataclass
class PaymentReceivedData:
    """Fired when a recurring payment is successfully processed. This event is for recurring charges only — the first checkout payment triggers subscription.activated instead."""

    invoiceId: str = ""
    invoiceNumber: str = ""
    invoiceTotal: float = 0.0
    customerId: str = ""
    subscriptionId: str | None = None
    paymentTransactionId: str | None = None
    grossAmount: float | None = None
    currency: str | None = None
    orgNetAmount: float | None = None
    customerEmail: str | None = None
    paidAt: str | None = None


@dataclass
class PaymentFailedData:
    """Fired when a recurring charge fails. This event is for recurring charge failures only — card declines during initial checkout do not trigger this event."""

    invoiceId: str = ""
    invoiceNumber: str = ""
    customerId: str = ""
    subscriptionId: str | None = None
    failureCode: str = ""
    failureMessage: str = ""


@dataclass
class PaymentRecoveredData:
    """Fired when an outstanding invoice that previously failed is successfully paid — automatically on retry or by the customer through the portal. The subscription returns to active at the same time; use this event to close the dunning flow you opened on payment.failed."""

    invoiceId: str = ""
    invoiceNumber: str = ""
    invoiceTotal: float = 0.0
    customerId: str = ""
    subscriptionId: str | None = None


@dataclass
class PaymentRetryFailedData:
    """Fired when all dunning retries are exhausted and the subscription is canceled. This is the terminal event of the dunning flow — payment.recovered will not follow. Revoke access when you receive this."""

    invoiceId: str = ""
    invoiceNumber: str = ""
    customerId: str = ""
    subscriptionId: str = ""
    reason: str = ""


@dataclass
class PaymentRefundedData:
    """Fired when a payment is refunded, fully or partially. A full refund of a subscription invoice also cancels the subscription immediately (subscription.canceled fires with reason refund); partial refunds leave the subscription untouched."""

    paymentTransactionId: str = ""
    paymentLinkId: str | None = None
    invoiceId: str | None = None
    invoiceNumber: str | None = None
    customerId: str | None = None
    subscriptionId: str | None = None
    refundAmount: float = 0.0
    currency: str = ""


@dataclass
class PaymentDisputedData:
    """Fired when a cardholder opens a dispute (chargeback) against a payment. The disputed amount is frozen from your payout balance while the dispute is open; Commet, as the Merchant of Record, handles the resolution process. payment.dispute_resolved fires with the outcome."""

    paymentTransactionId: str = ""
    paymentLinkId: str | None = None
    invoiceId: str | None = None
    invoiceNumber: str | None = None
    customerId: str | None = None
    subscriptionId: str | None = None
    disputeAmount: float = 0.0
    currency: str = ""
    disputeReason: str | None = None


@dataclass
class PaymentDisputeResolvedData:
    """Fired when a dispute is closed. Carries the same identifiers as payment.disputed plus the outcome: won restores the frozen amount to your balance, lost keeps the chargeback deducted."""

    paymentTransactionId: str = ""
    paymentLinkId: str | None = None
    invoiceId: str | None = None
    invoiceNumber: str | None = None
    customerId: str | None = None
    subscriptionId: str | None = None
    disputeAmount: float = 0.0
    currency: str = ""
    disputeReason: str | None = None
    outcome: str = ""


@dataclass
class PaymentLinkCreatedData:
    """Fired when a payment link is created. The link is pending — the customer has not paid yet. Do NOT fulfill here; wait for payment_link.completed."""

    paymentId: str = ""
    status: str = ""
    amount: float = 0.0
    currency: str = ""
    description: str = ""
    customerId: str | None = None


@dataclass
class PaymentLinkCompletedData:
    """Fired when a payment link is paid. The charge settled and a one-time invoice was generated. Fulfill the purchase on this event."""

    paymentId: str = ""
    status: str = ""
    amount: float = 0.0
    currency: str = ""
    description: str = ""
    customerId: str | None = None
    invoiceId: str = ""
    invoiceNumber: str = ""
    paymentTransactionId: str | None = None


@dataclass
class PaymentLinkFailedData:
    """Fired when a payment link charge attempt is declined. The link stays open and can be paid again — a failed link is retryable."""

    paymentId: str = ""
    status: str = ""
    amount: float = 0.0
    currency: str = ""
    description: str = ""
    customerId: str | None = None
    failureCode: str = ""
    failureMessage: str = ""


@dataclass
class PaymentLinkCanceledData:
    """Fired when a pending payment link is canceled before being paid. A canceled link can no longer be paid."""

    paymentId: str = ""
    status: str = ""
    amount: float = 0.0
    currency: str = ""
    description: str = ""
    customerId: str | None = None


@dataclass
class InvoiceCreatedData:
    """Fired when a new invoice is generated for a subscription, typically at the start of a billing period."""

    invoiceId: str = ""
    invoiceNumber: str = ""
    invoiceStatus: str = ""
    periodStart: str = ""
    periodEnd: str = ""
    issueDate: str = ""
    dueDate: str = ""
    currency: str = ""
    subtotal: float = 0.0
    total: float = 0.0
    customerId: str = ""
    subscriptionId: str | None = None


@dataclass
class InvoiceVoidedData:
    """Fired when an invoice is voided — nullified before collection, either manually or automatically when its subscription is canceled. Voiding is terminal: a void invoice is never retried or collected."""

    invoiceId: str = ""
    invoiceNumber: str = ""
    invoiceStatus: str = ""
    periodStart: str = ""
    periodEnd: str = ""
    issueDate: str = ""
    dueDate: str = ""
    currency: str = ""
    subtotal: float = 0.0
    total: float = 0.0
    customerId: str = ""
    subscriptionId: str | None = None


@dataclass
class InvoiceOverdueData:
    """Fired once when an outstanding invoice passes its due date without payment. The invoice keeps its outstanding status — overdue is a fact about the due date, not a new status. Use it to start your own dunning flow."""

    invoiceId: str = ""
    invoiceNumber: str = ""
    invoiceStatus: str = ""
    periodStart: str = ""
    periodEnd: str = ""
    issueDate: str = ""
    dueDate: str = ""
    currency: str = ""
    subtotal: float = 0.0
    total: float = 0.0
    customerId: str = ""
    subscriptionId: str | None = None


@dataclass
class InvoiceUpcomingData:
    """Predictive event fired once, 3 days before an active subscription renews. Use it to notify the customer before they are charged. Carries no amount — usage-based charges are only final at renewal, when invoice.created delivers the actual invoice."""

    subscriptionId: str = ""
    customerId: str = ""
    status: str = ""
    planId: str = ""
    planName: str = ""
    billingInterval: str | None = None
    currentPeriodEnd: str = ""


@dataclass
class PaymentMethodAttachedData:
    """Fired when Commet records a payment method for a subscription: after a paid checkout, when a trial starts with a card on file, or when a zero-total checkout completes. The card object carries display metadata only — full numbers never leave the payment provider."""

    subscriptionId: str = ""
    customerId: str = ""
    card: WebhookCardInfo | None = None


@dataclass
class PaymentMethodUpdatedData:
    """Fired when a customer replaces their default payment method through the customer portal. The new method applies to all of the customer's subscriptions. A payment method update is also a strong recovery signal for past-due subscriptions."""

    customerId: str = ""
    card: WebhookCardInfo | None = None


@dataclass
class CustomerCreatedData:
    """Fired when a customer is created, via the API (including batch create), SDK, or dashboard. The payload is the customer resource exactly as GET /customers returns it."""

    id: str = ""
    externalId: str | None = None
    fullName: str | None = None
    email: str = ""
    taxDocument: str | None = None
    documentType: str | None = None
    timezone: str | None = None
    metadata: dict[str, Any] | None = None
    createdAt: str = ""
    updatedAt: str = ""


@dataclass
class CustomerUpdatedData:
    """Fired when a customer's details change (email, name, timezone, externalId, or metadata). Carries the same customer resource shape as customer.created with the current values."""

    id: str = ""
    externalId: str | None = None
    fullName: str | None = None
    email: str = ""
    taxDocument: str | None = None
    documentType: str | None = None
    timezone: str | None = None
    metadata: dict[str, Any] | None = None
    createdAt: str = ""
    updatedAt: str = ""


@dataclass
class CustomerStateChangedData:
    """Aggregate entitlement event answering one question: what can this customer access right now? Fired on every entitlement transition (subscription lifecycle, plan changes, trials, past due, scheduled cancellations) with the customer's CURRENT subscription, plan, features, seats, and credits or balance. Handle this single event to keep access in sync instead of wiring every lifecycle event."""

    customerId: str = ""
    trigger: str = ""
    status: str = ""
    subscriptionId: str | None = None
    plan: WebhookPlanRef | None = None
    billingInterval: str | None = None
    consumptionModel: str | None = None
    features: list[WebhookFeatureAccess] = field(default_factory=list)
    seats: list[WebhookSeatSummary] = field(default_factory=list)
    credits: WebhookCreditsBalance | None = None
    balance: WebhookBalance | None = None


@dataclass
class CreditsGrantedData:
    """Fired when non-purchase credits are granted to a subscription: plan-included credits at the start of each billing period, or a manual adjustment from the dashboard. Credit pack purchases fire credits.purchased instead."""

    subscriptionId: str = ""
    customerId: str = ""
    credits: float = 0.0
    reason: str = ""


@dataclass
class CreditsPurchasedData:
    """Fired when a customer buys a credit pack through the customer portal and the payment succeeds. Purchased credits never expire — unlike plan credits, they survive period resets. Plan-included credit grants fire credits.granted instead."""

    subscriptionId: str = ""
    customerId: str = ""
    invoiceId: str = ""
    invoiceNumber: str = ""
    creditPackName: str = ""
    credits: float = 0.0


@dataclass
class CreditsLowData:
    """Fired when a subscription's remaining credits cross below 10% of the credits granted for the current period. Emitted once per billing period, when the crossing happens."""

    subscriptionId: str = ""
    customerId: str = ""
    remainingCredits: float = 0.0
    thresholdCredits: float = 0.0
    periodCredits: float = 0.0


@dataclass
class CreditsDepletedData:
    """Fired when a subscription's credits hit zero. Usage requests that need more credits than remain are rejected from this point. Also fires customer.state_changed with trigger credits_depleted."""

    subscriptionId: str = ""
    customerId: str = ""
    remainingCredits: float = 0.0


@dataclass
class CreditsExpiredData:
    """Fired at the period reset when unused plan credits from the previous period are discarded. Plan credits expire at period end; purchased credits never expire and are not affected."""

    subscriptionId: str = ""
    customerId: str = ""
    expiredCredits: float = 0.0


@dataclass
class BalanceToppedUpData:
    """Fired when a customer on a balance plan tops up their prepaid balance through the customer portal and the payment succeeds."""

    subscriptionId: str = ""
    customerId: str = ""
    invoiceId: str = ""
    invoiceNumber: str = ""
    amount: float = 0.0
    currency: str = ""


@dataclass
class BalanceLowData:
    """Fired when a subscription's prepaid balance crosses below 10% of its last refill (period reset, top-up, or manual adjustment). Emitted once per crossing."""

    subscriptionId: str = ""
    customerId: str = ""
    currentBalance: float = 0.0
    thresholdBalance: float = 0.0
    currency: str = ""


@dataclass
class BalanceDepletedData:
    """Fired when a subscription's prepaid balance crosses to zero or below. With block-on-exhaustion plans further usage is rejected; otherwise the balance can go negative. Also fires customer.state_changed with trigger balance_depleted."""

    subscriptionId: str = ""
    customerId: str = ""
    currentBalance: float = 0.0
    currency: str = ""


@dataclass
class QuotaThresholdReachedData:
    """Fired when a metered feature's usage crosses 80% of its included quantity for the current period. Emitted once per feature per billing period, when the crossing happens."""

    subscriptionId: str = ""
    customerId: str = ""
    featureCode: str = ""
    currentUsage: float = 0.0
    includedAmount: float = 0.0
    periodStart: str = ""


@dataclass
class QuotaExceededData:
    """Fired when a metered feature passes its included quantity. With overage enabled it means overage billing began; with overage disabled it means the hard limit was hit and further usage is rejected (this case also fires customer.state_changed with trigger quota_exceeded). Emitted once per feature per billing period."""

    subscriptionId: str = ""
    customerId: str = ""
    featureCode: str = ""
    currentUsage: float = 0.0
    includedAmount: float = 0.0
    overageEnabled: bool = False
    periodStart: str = ""


@dataclass
class SeatsUpdatedData:
    """Fired when a customer's seat count changes for a seats-type feature — via the SDK seats endpoints or the dashboard. Also fires customer.state_changed with trigger seats_updated."""

    customerId: str = ""
    subscriptionId: str | None = None
    featureCode: str = ""
    previousSeats: float = 0.0
    currentSeats: float = 0.0


@dataclass
class SeatsLimitReachedData:
    """Fired when a seat change reaches or passes the included seat limit of the customer's plan. Emitted once per crossing — only when the count moves from below the limit to at or above it."""

    customerId: str = ""
    subscriptionId: str = ""
    featureCode: str = ""
    currentSeats: float = 0.0
    includedSeats: float = 0.0


@dataclass
class AddonActivatedData:
    """Fired when an add-on is activated on a subscription — via the API or a customer portal purchase. The prorated activation charge, if any, has already succeeded. Also fires customer.state_changed with trigger addon_activated."""

    subscriptionId: str = ""
    customerId: str = ""
    addon: WebhookAddonRef = field(default_factory=WebhookAddonRef)
    featureCode: str = ""
    proratedPrice: float = 0.0
    currency: str = ""


@dataclass
class AddonDeactivatedData:
    """Fired when an active add-on is deactivated from a subscription. Also fires customer.state_changed with trigger addon_deactivated."""

    subscriptionId: str = ""
    customerId: str = ""
    addon: WebhookAddonRef = field(default_factory=WebhookAddonRef)
    featureCode: str = ""


@dataclass
class UsageRecordedData:
    """Fired for every processed usage event. HIGH VOLUME: this fires once per tracked event, so it is excluded from family select-all in the dashboard — subscribe to it explicitly and make sure your endpoint can absorb your own ingest rate."""

    subscriptionId: str = ""
    customerId: str = ""
    usageEventId: str = ""
    featureCode: str = ""
    value: float = 0.0
    ts: str = ""


@dataclass
class PayoutAvailableData:
    """Organization-level event about YOUR money as the merchant. Fired when payment funds the provider was holding become available to pay out to your bank."""

    availableAmount: float = 0.0
    currency: str = ""


@dataclass
class PayoutCreatedData:
    """Fired when a payout of your available balance is requested and the transfer toward your bank is initiated. The lifecycle continues with payout.paid or payout.failed."""

    payoutId: str = ""
    amount: float = 0.0
    fee: float = 0.0
    netAmount: float = 0.0
    currency: str = ""
    status: str = ""
    destinationBank: WebhookBankRef | None = None
    createdAt: str = ""


@dataclass
class PayoutPaidData:
    """Fired when the bank settlement of a payout completes — the moment the money actually reaches your bank account, confirmed by the payment provider. Fires exactly once per payout."""

    payoutId: str = ""
    amount: float = 0.0
    fee: float = 0.0
    netAmount: float = 0.0
    currency: str = ""
    status: str = ""
    destinationBank: WebhookBankRef | None = None
    paidAt: str | None = None


@dataclass
class PayoutFailedData:
    """Fired when the provider reports a payout could not be completed — most commonly a bank rejection (closed account, invalid details). The funds return to your available balance."""

    payoutId: str = ""
    amount: float = 0.0
    fee: float = 0.0
    netAmount: float = 0.0
    currency: str = ""
    status: str = ""
    destinationBank: WebhookBankRef | None = None
    failedAt: str | None = None
    failureCode: str | None = None
    failureMessage: str | None = None


@dataclass
class WebhookEvent:
    event: str
    timestamp: str = ""
    organizationId: str = ""
    mode: str = ""
    apiVersion: str = ""
    data: dict[str, Any] = field(default_factory=dict)

    def as_subscription_created(self) -> SubscriptionCreatedData:
        return _from_dict(SubscriptionCreatedData, self.data)

    def as_subscription_activated(self) -> SubscriptionActivatedData:
        return _from_dict(SubscriptionActivatedData, self.data)

    def as_subscription_reactivated(self) -> SubscriptionReactivatedData:
        return _from_dict(SubscriptionReactivatedData, self.data)

    def as_subscription_canceled(self) -> SubscriptionCanceledData:
        return _from_dict(SubscriptionCanceledData, self.data)

    def as_subscription_updated(self) -> SubscriptionUpdatedData:
        return _from_dict(SubscriptionUpdatedData, self.data)

    def as_subscription_plan_changed(self) -> SubscriptionPlanChangedData:
        return _from_dict(SubscriptionPlanChangedData, self.data)

    def as_subscription_cancellation_scheduled(self) -> SubscriptionCancellationScheduledData:
        return _from_dict(SubscriptionCancellationScheduledData, self.data)

    def as_subscription_cancellation_revoked(self) -> SubscriptionCancellationRevokedData:
        return _from_dict(SubscriptionCancellationRevokedData, self.data)

    def as_subscription_plan_change_scheduled(self) -> SubscriptionPlanChangeScheduledData:
        return _from_dict(SubscriptionPlanChangeScheduledData, self.data)

    def as_subscription_plan_change_revoked(self) -> SubscriptionPlanChangeRevokedData:
        return _from_dict(SubscriptionPlanChangeRevokedData, self.data)

    def as_subscription_past_due(self) -> SubscriptionPastDueData:
        return _from_dict(SubscriptionPastDueData, self.data)

    def as_trial_started(self) -> TrialStartedData:
        return _from_dict(TrialStartedData, self.data)

    def as_trial_converted(self) -> TrialConvertedData:
        return _from_dict(TrialConvertedData, self.data)

    def as_trial_expired(self) -> TrialExpiredData:
        return _from_dict(TrialExpiredData, self.data)

    def as_trial_will_end(self) -> TrialWillEndData:
        return _from_dict(TrialWillEndData, self.data)

    def as_trial_checkout_ready(self) -> TrialCheckoutReadyData:
        return _from_dict(TrialCheckoutReadyData, self.data)

    def as_checkout_ready(self) -> CheckoutReadyData:
        return _from_dict(CheckoutReadyData, self.data)

    def as_payment_received(self) -> PaymentReceivedData:
        return _from_dict(PaymentReceivedData, self.data)

    def as_payment_failed(self) -> PaymentFailedData:
        return _from_dict(PaymentFailedData, self.data)

    def as_payment_recovered(self) -> PaymentRecoveredData:
        return _from_dict(PaymentRecoveredData, self.data)

    def as_payment_retry_failed(self) -> PaymentRetryFailedData:
        return _from_dict(PaymentRetryFailedData, self.data)

    def as_payment_refunded(self) -> PaymentRefundedData:
        return _from_dict(PaymentRefundedData, self.data)

    def as_payment_disputed(self) -> PaymentDisputedData:
        return _from_dict(PaymentDisputedData, self.data)

    def as_payment_dispute_resolved(self) -> PaymentDisputeResolvedData:
        return _from_dict(PaymentDisputeResolvedData, self.data)

    def as_payment_link_created(self) -> PaymentLinkCreatedData:
        return _from_dict(PaymentLinkCreatedData, self.data)

    def as_payment_link_completed(self) -> PaymentLinkCompletedData:
        return _from_dict(PaymentLinkCompletedData, self.data)

    def as_payment_link_failed(self) -> PaymentLinkFailedData:
        return _from_dict(PaymentLinkFailedData, self.data)

    def as_payment_link_canceled(self) -> PaymentLinkCanceledData:
        return _from_dict(PaymentLinkCanceledData, self.data)

    def as_invoice_created(self) -> InvoiceCreatedData:
        return _from_dict(InvoiceCreatedData, self.data)

    def as_invoice_voided(self) -> InvoiceVoidedData:
        return _from_dict(InvoiceVoidedData, self.data)

    def as_invoice_overdue(self) -> InvoiceOverdueData:
        return _from_dict(InvoiceOverdueData, self.data)

    def as_invoice_upcoming(self) -> InvoiceUpcomingData:
        return _from_dict(InvoiceUpcomingData, self.data)

    def as_payment_method_attached(self) -> PaymentMethodAttachedData:
        return _from_dict(PaymentMethodAttachedData, self.data)

    def as_payment_method_updated(self) -> PaymentMethodUpdatedData:
        return _from_dict(PaymentMethodUpdatedData, self.data)

    def as_customer_created(self) -> CustomerCreatedData:
        return _from_dict(CustomerCreatedData, self.data)

    def as_customer_updated(self) -> CustomerUpdatedData:
        return _from_dict(CustomerUpdatedData, self.data)

    def as_customer_state_changed(self) -> CustomerStateChangedData:
        return _from_dict(CustomerStateChangedData, self.data)

    def as_credits_granted(self) -> CreditsGrantedData:
        return _from_dict(CreditsGrantedData, self.data)

    def as_credits_purchased(self) -> CreditsPurchasedData:
        return _from_dict(CreditsPurchasedData, self.data)

    def as_credits_low(self) -> CreditsLowData:
        return _from_dict(CreditsLowData, self.data)

    def as_credits_depleted(self) -> CreditsDepletedData:
        return _from_dict(CreditsDepletedData, self.data)

    def as_credits_expired(self) -> CreditsExpiredData:
        return _from_dict(CreditsExpiredData, self.data)

    def as_balance_topped_up(self) -> BalanceToppedUpData:
        return _from_dict(BalanceToppedUpData, self.data)

    def as_balance_low(self) -> BalanceLowData:
        return _from_dict(BalanceLowData, self.data)

    def as_balance_depleted(self) -> BalanceDepletedData:
        return _from_dict(BalanceDepletedData, self.data)

    def as_quota_threshold_reached(self) -> QuotaThresholdReachedData:
        return _from_dict(QuotaThresholdReachedData, self.data)

    def as_quota_exceeded(self) -> QuotaExceededData:
        return _from_dict(QuotaExceededData, self.data)

    def as_seats_updated(self) -> SeatsUpdatedData:
        return _from_dict(SeatsUpdatedData, self.data)

    def as_seats_limit_reached(self) -> SeatsLimitReachedData:
        return _from_dict(SeatsLimitReachedData, self.data)

    def as_addon_activated(self) -> AddonActivatedData:
        return _from_dict(AddonActivatedData, self.data)

    def as_addon_deactivated(self) -> AddonDeactivatedData:
        return _from_dict(AddonDeactivatedData, self.data)

    def as_usage_recorded(self) -> UsageRecordedData:
        return _from_dict(UsageRecordedData, self.data)

    def as_payout_available(self) -> PayoutAvailableData:
        return _from_dict(PayoutAvailableData, self.data)

    def as_payout_created(self) -> PayoutCreatedData:
        return _from_dict(PayoutCreatedData, self.data)

    def as_payout_paid(self) -> PayoutPaidData:
        return _from_dict(PayoutPaidData, self.data)

    def as_payout_failed(self) -> PayoutFailedData:
        return _from_dict(PayoutFailedData, self.data)


_DATACLASS_TYPES.update(
    {
        "SubscriptionCreatedData": SubscriptionCreatedData,
        "SubscriptionActivatedData": SubscriptionActivatedData,
        "SubscriptionReactivatedData": SubscriptionReactivatedData,
        "SubscriptionCanceledData": SubscriptionCanceledData,
        "SubscriptionUpdatedData": SubscriptionUpdatedData,
        "SubscriptionPlanChangedData": SubscriptionPlanChangedData,
        "SubscriptionCancellationScheduledData": SubscriptionCancellationScheduledData,
        "SubscriptionCancellationRevokedData": SubscriptionCancellationRevokedData,
        "SubscriptionPlanChangeScheduledData": SubscriptionPlanChangeScheduledData,
        "SubscriptionPlanChangeRevokedData": SubscriptionPlanChangeRevokedData,
        "SubscriptionPastDueData": SubscriptionPastDueData,
        "TrialStartedData": TrialStartedData,
        "TrialConvertedData": TrialConvertedData,
        "TrialExpiredData": TrialExpiredData,
        "TrialWillEndData": TrialWillEndData,
        "TrialCheckoutReadyData": TrialCheckoutReadyData,
        "CheckoutReadyData": CheckoutReadyData,
        "PaymentReceivedData": PaymentReceivedData,
        "PaymentFailedData": PaymentFailedData,
        "PaymentRecoveredData": PaymentRecoveredData,
        "PaymentRetryFailedData": PaymentRetryFailedData,
        "PaymentRefundedData": PaymentRefundedData,
        "PaymentDisputedData": PaymentDisputedData,
        "PaymentDisputeResolvedData": PaymentDisputeResolvedData,
        "PaymentLinkCreatedData": PaymentLinkCreatedData,
        "PaymentLinkCompletedData": PaymentLinkCompletedData,
        "PaymentLinkFailedData": PaymentLinkFailedData,
        "PaymentLinkCanceledData": PaymentLinkCanceledData,
        "InvoiceCreatedData": InvoiceCreatedData,
        "InvoiceVoidedData": InvoiceVoidedData,
        "InvoiceOverdueData": InvoiceOverdueData,
        "InvoiceUpcomingData": InvoiceUpcomingData,
        "PaymentMethodAttachedData": PaymentMethodAttachedData,
        "PaymentMethodUpdatedData": PaymentMethodUpdatedData,
        "CustomerCreatedData": CustomerCreatedData,
        "CustomerUpdatedData": CustomerUpdatedData,
        "CustomerStateChangedData": CustomerStateChangedData,
        "CreditsGrantedData": CreditsGrantedData,
        "CreditsPurchasedData": CreditsPurchasedData,
        "CreditsLowData": CreditsLowData,
        "CreditsDepletedData": CreditsDepletedData,
        "CreditsExpiredData": CreditsExpiredData,
        "BalanceToppedUpData": BalanceToppedUpData,
        "BalanceLowData": BalanceLowData,
        "BalanceDepletedData": BalanceDepletedData,
        "QuotaThresholdReachedData": QuotaThresholdReachedData,
        "QuotaExceededData": QuotaExceededData,
        "SeatsUpdatedData": SeatsUpdatedData,
        "SeatsLimitReachedData": SeatsLimitReachedData,
        "AddonActivatedData": AddonActivatedData,
        "AddonDeactivatedData": AddonDeactivatedData,
        "UsageRecordedData": UsageRecordedData,
        "PayoutAvailableData": PayoutAvailableData,
        "PayoutCreatedData": PayoutCreatedData,
        "PayoutPaidData": PayoutPaidData,
        "PayoutFailedData": PayoutFailedData,
    }
)
