# Plan Groups

API version: `2026-07-31`

## remove_plan

`commet.plan_groups.remove_plan(...)`

`DELETE /plan-groups/{id}/plans/{planId}` · operation `remove-plan-from-group`

Remove a plan from a plan group.

### Parameters

- `id` (`str`, required)
- `plan_id` (`str`, required)

### Returns

`RemovedPlanFromGroup`

## reorder_plans

`commet.plan_groups.reorder_plans(...)`

`PUT /plan-groups/{id}/plans/reorder` · operation `reorder-plans-in-group`

Set the display order of plans within a group. All plan IDs in the group must be provided.

### Parameters

- `id` (`str`, required)
- `plan_ids` (`list[str]`, required)

### Request options

- `idempotency_key` (`str`, optional) — Unique key used to safely retry this write for 24 hours without applying it twice.

### Returns

`ReorderedPlans`

## add_plan

`commet.plan_groups.add_plan(...)`

`POST /plan-groups/{id}/plans` · operation `add-plan-to-group`

Add an existing plan to a plan group with optional sort order.

### Parameters

- `id` (`str`, required)
- `plan_id` (`str`, required)
- `sort_order` (`int`, optional)

### Request options

- `idempotency_key` (`str`, optional) — Unique key used to safely retry this write for 24 hours without applying it twice.

### Returns

`AddedPlanToGroup`

## get

`commet.plan_groups.get(...)`

`GET /plan-groups/{id}` · operation `get-plan-group`

Retrieve a plan group by ID, including its plans ordered by sortOrder.

### Parameters

- `id` (`str`, required)

### Returns

`PlanGroupDetail`

## update

`commet.plan_groups.update(...)`

`PATCH /plan-groups/{id}` · operation `update-plan-group`

Update a plan group's name, description, or visibility.

### Parameters

- `id` (`str`, required)
- `name` (`str`, optional)
- `description` (`str | null`, optional)
- `is_public` (`bool`, optional)

### Request options

- `idempotency_key` (`str`, optional) — Unique key used to safely retry this write for 24 hours without applying it twice.

### Returns

`PlanGroup`

## delete

`commet.plan_groups.delete(...)`

`DELETE /plan-groups/{id}` · operation `delete-plan-group`

Delete a plan group. Plans in the group are unlinked, not deleted.

### Parameters

- `id` (`str`, required)

### Returns

`DeletedObject`

## list

`commet.plan_groups.list(...)`

`GET /plan-groups` · operation `list-plan-groups`

List plan groups with cursor-based pagination.

### Parameters

- `cursor` (`str`, optional)
- `limit` (`int`, optional)

### Returns

`PlanGroupsListResult`

## create

`commet.plan_groups.create(...)`

`POST /plan-groups` · operation `create-plan-group`

Create a new plan group for organizing plans.

### Parameters

- `name` (`str`, required)
- `description` (`str`, optional)
- `is_public` (`bool`, optional)

### Request options

- `idempotency_key` (`str`, optional) — Unique key used to safely retry this write for 24 hours without applying it twice.

### Returns

`PlanGroup`
