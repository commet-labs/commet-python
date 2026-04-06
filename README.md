# Commet Python SDK

Billing and usage tracking for SaaS applications.

## Installation

```bash
pip install commet
```

## Quick start

```python
from commet import Commet

commet = Commet(api_key="ck_xxx", environment="production")

# Create a customer
commet.customers.create(email="user@example.com", external_id="user_123")

# Create a subscription
commet.subscriptions.create(external_id="user_123", plan_code="pro")

# Track usage
commet.usage.track(feature="api_calls", external_id="user_123")

# Track AI token usage
commet.usage.track(
    feature="ai_generation",
    external_id="user_123",
    model="claude-sonnet-4-20250514",
    input_tokens=1000,
    output_tokens=500,
)
```

## Customer context

Scope all operations to a customer to avoid repeating `external_id`:

```python
customer = commet.customer("user_123")

customer.usage.track("api_calls")
customer.features.check("custom_branding")
customer.seats.add("editor", count=3)
customer.portal.get_url()
```

## Webhook verification

```python
from commet import Webhooks

webhooks = Webhooks()

payload = webhooks.verify_and_parse(
    raw_body=request_body,
    signature=request.headers["x-commet-signature"],
    secret="whsec_xxx",
)

if payload is None:
    raise ValueError("Invalid webhook signature")

if payload["event"] == "subscription.activated":
    # handle activation
    pass
```

## Context manager

```python
with Commet(api_key="ck_xxx") as commet:
    commet.usage.track(feature="api_calls", external_id="user_123")
# connection pool is automatically closed
```

## Environments

The SDK defaults to `sandbox`. Set `environment="production"` for live operations:

```python
commet = Commet(api_key="ck_xxx", environment="production")
```

## License

MIT
