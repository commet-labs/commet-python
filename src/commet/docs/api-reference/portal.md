# Portal

API version: `2026-07-31`

## get_url

`commet.portal.get_url(...)`

`POST /portal/sessions` · operation `request-portal-access`

Generate a customer portal URL. Exactly one identifier (email or customerId) is required.

### Parameters

- `email` (`str`, optional)
- `return_url` (`str`, optional)
- `customer_id` (`str`, optional)

### Request options

- `idempotency_key` (`str`, optional) — Unique key used to safely retry this write for 24 hours without applying it twice.

### Returns

`PortalAccess`
