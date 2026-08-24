# Customers

API version: `2026-07-31`

## revoke_credit

`commet.customers.revoke_credit(...)`

`POST /customers/{id}/credits/{creditId}/revoke` · operation `revoke-customer-credit`

Revoke the unallocated remainder of a customer credit grant. Applied invoice history is unchanged.

### Parameters

- `id` (`str`, required)
- `credit_id` (`str`, required)

### Request options

- `idempotency_key` (`str`, optional) — Unique key used to safely retry this write for 24 hours without applying it twice.

### Returns

`CustomerCreditRevocation`

## list_credits

`commet.customers.list_credits(...)`

`GET /customers/{id}/credits` · operation `list-customer-credits`

List currency-specific invoice credit grants and their remaining balances for a customer.

### Parameters

- `id` (`str`, required)

### Returns

`CustomersListCreditsResult`

## create_credit

`commet.customers.create_credit(...)`

`POST /customers/{id}/credits` · operation `create-customer-credit`

Grant monetary credit in one currency. Credit is applied FIFO before tax to eligible recurring invoices.

### Parameters

- `id` (`str`, required)
- `amount` (`int`, required) — Amount in the currency's smallest unit.
- `currency` (`Literal["usd", "ars", "brl", "clp", "cop", "pen", "uyu", "pyg", "bob", "mxn", "cad", "eur", "gbp", "jpy", "cny", "krw", "hkd", "sgd", "twd", "inr", "thb"]`, required)
- `reason` (`str`, required)
- `expires_at` (`str | null`, optional)

### Request options

- `idempotency_key` (`str`, optional) — Unique key used to safely retry this write for 24 hours without applying it twice.

### Returns

`CustomerCredit`

## revoke_plan_grant

`commet.customers.revoke_plan_grant(...)`

`POST /customers/{id}/plan-grants/{grantId}/revoke` · operation `revoke-plan-grant`

End expanded access immediately and restore the base plan's limits. The subscription, billing cycle, invoices, and payment state remain unchanged.

### Parameters

- `id` (`str`, required)
- `grant_id` (`str`, required)
- `reason` (`str`, required)

### Request options

- `idempotency_key` (`str`, optional) — Unique key used to safely retry this write for 24 hours without applying it twice.

### Returns

`PlanGrant`

## update_plan_grant

`commet.customers.update_plan_grant(...)`

`PATCH /customers/{id}/plan-grants/{grantId}` · operation `update-plan-grant`

Keep the overlay for a number of the subscription's existing billing cycles, set an exact deadline, or leave it active until revoked. The billing anchor is never reset.

### Parameters

- `id` (`str`, required)
- `grant_id` (`str`, required)
- `reason` (`str`, required)
- `duration` (`Literal["cycles", "until_date", "until_revoked"]`, required)
- `duration_cycles` (`int`, optional)
- `expires_at` (`str`, optional)

### Valid parameter combinations

- `reason` + `duration` + `duration_cycles`
- `reason` + `duration` + `expires_at`
- `reason` + `duration`

### Request options

- `idempotency_key` (`str`, optional) — Unique key used to safely retry this write for 24 hours without applying it twice.

### Returns

`PlanGrant`

## list_plan_grants

`commet.customers.list_plan_grants(...)`

`GET /customers/{id}/plan-grants` · operation `list-plan-grants`

List the independent audit timeline for paid-plan access granted without checkout or payment credentials.

### Parameters

- `id` (`str`, required)

### Returns

`CustomersListPlanGrantsResult`

## create_plan_grant

`commet.customers.create_plan_grant(...)`

`POST /customers/{id}/plan-grants` · operation `create-plan-grant`

Temporarily expand an active subscription's feature access using a higher plan in the same plan group. Billing, prices, periods, invoices, and the base subscription remain unchanged.

### Parameters

- `id` (`str`, required)
- `subscription_id` (`str`, required)
- `plan_id` (`str`, required)
- `reason` (`str`, required)
- `duration` (`Literal["cycles", "until_date", "until_revoked"]`, required)
- `duration_cycles` (`int`, optional)
- `expires_at` (`str`, optional)

### Valid parameter combinations

- `subscription_id` + `plan_id` + `reason` + `duration` + `duration_cycles`
- `subscription_id` + `plan_id` + `reason` + `duration` + `expires_at`
- `subscription_id` + `plan_id` + `reason` + `duration`

### Request options

- `idempotency_key` (`str`, optional) — Unique key used to safely retry this write for 24 hours without applying it twice.

### Returns

`PlanGrant`

## get

`commet.customers.get(...)`

`GET /customers/{id}` · operation `get-customer`

Retrieve a customer by their public ID, including subscription status and metadata.

### Parameters

- `id` (`str`, required)

### Returns

`Customer`

## update

`commet.customers.update(...)`

`PATCH /customers/{id}` · operation `update-customer`

Update a customer's name, external ID, or metadata.

### Parameters

- `id` (`str`, required)
- `email` (`str`, optional)
- `full_name` (`str`, optional)
- `tax_document` (`str`, optional)
- `external_id` (`str`, optional)
- `timezone` (`Timezone`, optional)
- `metadata` (`dict[str, Any]`, optional)
- `address` (`UpdateCustomerParamsAddress`, optional)

### Request options

- `idempotency_key` (`str`, optional) — Unique key used to safely retry this write for 24 hours without applying it twice.

### Returns

`Customer`

## create_batch

`commet.customers.create_batch(...)`

`POST /customers/batch` · operation `batch-create-customers`

Create up to 100 customers in a single request.

### Parameters

- `customers` (`list[BatchCreateCustomersParamsCustomersItem]`, required)

### Request options

- `idempotency_key` (`str`, optional) — Unique key used to safely retry this write for 24 hours without applying it twice.

### Returns

`CustomerBatch`

## list

`commet.customers.list(...)`

`GET /customers` · operation `list-customers`

List customers with cursor-based pagination.

### Parameters

- `cursor` (`str`, optional)
- `limit` (`int`, optional)
- `external_id` (`str`, optional)

### Returns

`CustomersListResult`

## create

`commet.customers.create(...)`

`POST /customers` · operation `create-customer`

Create a new customer. Idempotent when customerId is provided.

### Parameters

- `id` (`str`, optional)
- `external_id` (`str`, optional)
- `full_name` (`str`, optional)
- `tax_document` (`str`, optional)
- `address` (`CreateCustomerParamsAddress`, optional)
- `address_id` (`str`, optional)
- `email` (`str`, required)
- `timezone` (`Timezone`, optional)
- `metadata` (`dict[str, Any]`, optional)

### Request options

- `idempotency_key` (`str`, optional) — Unique key used to safely retry this write for 24 hours without applying it twice.

### Returns

`Customer`
