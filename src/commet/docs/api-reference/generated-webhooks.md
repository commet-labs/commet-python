# Webhooks

API version: `2026-07-31`

## get

`commet.webhooks.get(...)`

`GET /webhooks/{id}` · operation `get-webhook-endpoint`

Retrieve a webhook endpoint by its public ID.

### Parameters

- `id` (`str`, required)

### Returns

`Webhook`

## update

`commet.webhooks.update(...)`

`PATCH /webhooks/{id}` · operation `update-webhook-endpoint`

Update a webhook endpoint. Only the provided fields change.

### Parameters

- `id` (`str`, required)
- `url` (`str`, optional)
- `events` (`list[Literal["subscription.created", "subscription.activated", "subscription.reactivated", "subscription.canceled", "subscription.updated", "subscription.plan_changed", "subscription.cancellation_scheduled", "subscription.cancellation_revoked", "subscription.plan_change_scheduled", "subscription.plan_change_revoked", "subscription.past_due", "trial.started", "trial.converted", "trial.expired", "trial.will_end", "trial.checkout_ready", "checkout.ready", "payment.received", "payment.failed", "payment.recovered", "payment.retry_failed", "payment.refunded", "payment.disputed", "payment.dispute_resolved", "payment_link.created", "payment_link.completed", "payment_link.failed", "payment_link.canceled", "invoice.created", "invoice.voided", "invoice.overdue", "invoice.upcoming", "payment_method.attached", "payment_method.updated", "customer.created", "customer.updated", "customer.state_changed", "plan_grant.created", "plan_grant.updated", "plan_grant.expired", "plan_grant.revoked", "credits.granted", "credits.purchased", "credits.low", "credits.depleted", "credits.expired", "balance.topped_up", "balance.low", "balance.depleted", "quota.threshold_reached", "quota.exceeded", "seats.updated", "seats.limit_reached", "addon.activated", "addon.deactivated", "usage.recorded", "payout.available", "payout.created", "payout.paid", "payout.failed"]]`, optional)
- `description` (`str | null`, optional)
- `is_active` (`bool`, optional)
- `api_version` (`str`, optional)

### Request options

- `idempotency_key` (`str`, optional) — Unique key used to safely retry this write for 24 hours without applying it twice.

### Returns

`Webhook`

## delete

`commet.webhooks.delete(...)`

`DELETE /webhooks/{id}` · operation `delete-webhook-endpoint`

Permanently delete a webhook endpoint.

### Parameters

- `id` (`str`, required)

### Returns

`DeletedObject`

## test

`commet.webhooks.test(...)`

`POST /webhooks/{id}/test` · operation `test-webhook-endpoint`

Send a test event to a webhook endpoint to verify connectivity.

### Parameters

- `id` (`str`, required)

### Request options

- `idempotency_key` (`str`, optional) — Unique key used to safely retry this write for 24 hours without applying it twice.

### Returns

`WebhookTest`

## list

`commet.webhooks.list(...)`

`GET /webhooks` · operation `list-webhook-endpoints`

List webhook endpoints with cursor-based pagination.

### Parameters

- `cursor` (`str`, optional)
- `limit` (`int`, optional)

### Returns

`WebhooksListResult`

## create

`commet.webhooks.create(...)`

`POST /webhooks` · operation `create-webhook-endpoint`

Create a new webhook endpoint. The response includes the signing secret which is only returned once.

### Parameters

- `url` (`str`, required)
- `events` (`list[Literal["subscription.created", "subscription.activated", "subscription.reactivated", "subscription.canceled", "subscription.updated", "subscription.plan_changed", "subscription.cancellation_scheduled", "subscription.cancellation_revoked", "subscription.plan_change_scheduled", "subscription.plan_change_revoked", "subscription.past_due", "trial.started", "trial.converted", "trial.expired", "trial.will_end", "trial.checkout_ready", "checkout.ready", "payment.received", "payment.failed", "payment.recovered", "payment.retry_failed", "payment.refunded", "payment.disputed", "payment.dispute_resolved", "payment_link.created", "payment_link.completed", "payment_link.failed", "payment_link.canceled", "invoice.created", "invoice.voided", "invoice.overdue", "invoice.upcoming", "payment_method.attached", "payment_method.updated", "customer.created", "customer.updated", "customer.state_changed", "plan_grant.created", "plan_grant.updated", "plan_grant.expired", "plan_grant.revoked", "credits.granted", "credits.purchased", "credits.low", "credits.depleted", "credits.expired", "balance.topped_up", "balance.low", "balance.depleted", "quota.threshold_reached", "quota.exceeded", "seats.updated", "seats.limit_reached", "addon.activated", "addon.deactivated", "usage.recorded", "payout.available", "payout.created", "payout.paid", "payout.failed"]]`, required)
- `description` (`str`, optional)
- `api_version` (`str`, optional)

### Request options

- `idempotency_key` (`str`, optional) — Unique key used to safely retry this write for 24 hours without applying it twice.

### Returns

`CreatedWebhook`
