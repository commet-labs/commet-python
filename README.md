# Commet Python SDK

Billing and usage tracking for SaaS applications.

## Installation

```bash
pip install commet-sdk
```

## Quick start

```python
from commet import Commet

commet = Commet(api_key="ck_xxx")

# Create a customer
commet.customers.create(email="user@example.com")

# Create a subscription
commet.subscriptions.create(customer_id="cus_123", plan_code="pro")

# Track usage
commet.usage.track(feature="api_calls", customer_id="cus_123")

# Track AI token usage
commet.usage.track(
    feature="ai_generation",
    customer_id="cus_123",
    model="claude-sonnet-4-20250514",
    input_tokens=1000,
    output_tokens=500,
)
```

## Customer context

Scope all operations to a customer to avoid repeating `customer_id`:

```python
customer = commet.customer("user_123")

customer.usage.track("api_calls")
customer.features.check("custom_branding")
customer.seats.add(feature_code="editor", count=3)
customer.portal.get_url()
```

## Quota

```python
# Add to the quota balance (count defaults to 1)
commet.quota.add(feature_code="storage", customer_id="cus_123")

# Set the quota balance to an exact value
commet.quota.set(feature_code="storage", count=10, customer_id="cus_123")

# Remove from the quota balance (count defaults to 1)
commet.quota.remove(feature_code="storage", customer_id="cus_123")

# Read a single allowance
commet.quota.get(feature_code="storage", customer_id="cus_123")

# Read every allowance for a customer
commet.quota.get_all(customer_id="cus_123")
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
    commet.usage.track(feature="api_calls", customer_id="cus_123")
# connection pool is automatically closed
```

## License

MIT
