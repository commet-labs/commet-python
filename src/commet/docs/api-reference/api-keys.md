# Api Keys

API version: `2026-07-31`

## delete

`commet.api_keys.delete(...)`

`DELETE /api-keys/{id}` · operation `delete-api-key`

Permanently revoke and delete an API key.

### Parameters

- `id` (`str`, required)

### Returns

`DeletedObject`

## list

`commet.api_keys.list(...)`

`GET /api-keys` · operation `list-api-keys`

List API keys with cursor-based pagination. Keys are returned without the full secret.

### Parameters

- `cursor` (`str`, optional)
- `limit` (`int`, optional)

### Returns

`ApiKeysListResult`

## create

`commet.api_keys.create(...)`

`POST /api-keys` · operation `create-api-key`

Create a new API key. The full key is only returned once in the response.

### Parameters

- `name` (`str`, required)
- `expires_in_days` (`int`, optional)

### Request options

- `idempotency_key` (`str`, optional) — Unique key used to safely retry this write for 24 hours without applying it twice.

### Returns

`CreatedApiKey`
