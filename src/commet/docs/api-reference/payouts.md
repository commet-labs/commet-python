# Payouts

API version: `2026-07-31`

## add_bank_account

`commet.payouts.add_bank_account(...)`

`POST /payouts/bank-accounts` · operation `add-payout-bank-account`

Add an additional destination bank account to the organization's existing payout account. Country and currency are resolved from the organization. The full account number is never returned — only `last4`.

### Parameters

- `account_number` (`str`, required)
- `account_holder_name` (`str`, required)
- `routing_number` (`str`, optional)
- `account_type` (`Literal["checking", "savings"]`, optional)
- `set_default` (`bool`, optional)

### Request options

- `idempotency_key` (`str`, optional) — Unique key used to safely retry this write for 24 hours without applying it twice.

### Returns

`PayoutBankAccount`

## request

`commet.payouts.request(...)`

`POST /payouts` · operation `request-payout`

Withdraw available balance to the organization's verified payout account. `amount` is in cents (USD, minimum 1000 = $10). The payout is created in `pending` and settles to `paid` asynchronously as provider webhooks arrive.

### Parameters

- `amount` (`int`, required)
- `description` (`str`, optional)

### Request options

- `idempotency_key` (`str`, optional) — Unique key used to safely retry this write for 24 hours without applying it twice.

### Returns

`Payout`

## complete_verification

`commet.payouts.complete_verification(...)`

`POST /payouts/verification` · operation `complete-payout-verification`

Deprecated. Complete business and identity verification in the Commet dashboard. This endpoint no longer accepts or processes KYC data.

Deprecated.

### Request options

- `idempotency_key` (`str`, optional) — Unique key used to safely retry this write for 24 hours without applying it twice.

### Returns

`void`
