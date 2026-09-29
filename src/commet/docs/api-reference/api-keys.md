# Api Keys

API version: `2026-08-27`

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

Create a full-access or restricted API key. Provide permissions to restrict access; the full key is returned only once. A restricted key with api_key: write may only create restricted keys with the same or fewer permissions, and they expire no later than the key that creates them.

### Parameters

- `name` (`str`, required)
- `expires_in_days` (`int`, optional)
- `permissions` (`CreateApiKeyParamsPermissions`, optional)

### Request options

- `idempotency_key` (`str`, optional) — Unique key used to safely retry this write for 24 hours without applying it twice.

### Returns

`CreatedApiKey`
