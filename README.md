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
customer = commet.customers.create(email="user@example.com")

# Create a subscription
commet.subscriptions.create(customer_id=customer.id, plan_code="pro")

# Track usage
commet.usage.track(
    feature_code="api_calls",
    customer_id=customer.id,
    value=1,
)

# Track AI token usage
commet.usage.track(
    feature_code="ai_generation",
    customer_id=customer.id,
    model="claude-sonnet-4-20250514",
    input_tokens=1000,
    output_tokens=500,
)
```

## Offers and pricing Markets

SDK v8 exposes reusable Offers, country Market Groups, and selectable `price_id` variants:

```python
market = commet.pricing.create_market_group(
    name="Argentina",
    country_codes=["AR"],
)

offer = commet.offers.create(
    name="First three months at 25% off",
    purpose="promotional",
    plan_price_ids=["pp_monthly"],
    phases=[{"type": "percentage", "percentage": 2500, "duration_cycles": 3}],
)
```

Promo Codes reference Promotional Offers. Omitting `price_id` during subscription creation keeps normal default-price resolution.

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
    commet.usage.track(
        feature_code="api_calls",
        customer_id="cus_123",
        value=1,
    )
# connection pool is automatically closed
```

## License

MIT
