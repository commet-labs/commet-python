from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from ._http import ApiResponse
from ._shared import build_body
from .types import (
    CreditPack,
    Customer,
    FeatureAccess,
    Plan,
    PortalSession,
    QuotaAllowance,
    QuotaEvent,
    SeatBalance,
    SeatEvent,
    Subscription,
    UsageEvent,
    _from_dict,
    _from_list,
)


def parse_customer(response: ApiResponse[Any]) -> ApiResponse[Customer]:
    if response.data and isinstance(response.data, dict):
        response.data = _from_dict(Customer, response.data)
    return response


def parse_customer_list(response: ApiResponse[Any]) -> ApiResponse[list[Customer]]:
    if response.data and isinstance(response.data, list):
        response.data = _from_list(Customer, response.data)
    return response


def build_customer_create_body(
    *,
    email: str,
    full_name: str | None = None,
    domain: str | None = None,
    website: str | None = None,
    timezone: str | None = None,
    language: str | None = None,
    industry: str | None = None,
    metadata: dict[str, Any] | None = None,
    address: dict[str, str] | None = None,
) -> dict[str, Any]:
    return build_body(
        billing_email=email,
        full_name=full_name,
        domain=domain,
        website=website,
        timezone=timezone,
        language=language,
        industry=industry,
        metadata=metadata,
        address=address,
    )


def build_customer_batch_body(customers: list[dict[str, Any]]) -> dict[str, Any]:
    mapped = [
        build_body(
            billing_email=c.get("email"),
            full_name=c.get("full_name"),
            domain=c.get("domain"),
            website=c.get("website"),
            timezone=c.get("timezone"),
            language=c.get("language"),
            industry=c.get("industry"),
            metadata=c.get("metadata"),
            address=c.get("address"),
        )
        for c in customers
    ]
    return {"customers": mapped}


def build_customer_update_body(
    *,
    email: str | None = None,
    full_name: str | None = None,
    domain: str | None = None,
    website: str | None = None,
    timezone: str | None = None,
    language: str | None = None,
    industry: str | None = None,
    metadata: dict[str, Any] | None = None,
    address: dict[str, str] | None = None,
) -> dict[str, Any]:
    return build_body(
        billing_email=email,
        full_name=full_name,
        domain=domain,
        website=website,
        timezone=timezone,
        language=language,
        industry=industry,
        metadata=metadata,
        address=address,
    )


def parse_feature_access(response: ApiResponse[Any]) -> ApiResponse[FeatureAccess]:
    if response.data and isinstance(response.data, dict):
        response.data = _from_dict(FeatureAccess, response.data)
    return response


def parse_feature_access_list(response: ApiResponse[Any]) -> ApiResponse[list[FeatureAccess]]:
    if response.data and isinstance(response.data, list):
        response.data = _from_list(FeatureAccess, response.data)
    return response


def parse_plan(response: ApiResponse[Any]) -> ApiResponse[Plan]:
    if response.data and isinstance(response.data, dict):
        response.data = _from_dict(Plan, response.data)
    return response


def parse_plan_list(response: ApiResponse[Any]) -> ApiResponse[list[Plan]]:
    if response.data and isinstance(response.data, list):
        response.data = _from_list(Plan, response.data)
    return response


def parse_subscription(response: ApiResponse[Any]) -> ApiResponse[Subscription]:
    if response.data and isinstance(response.data, dict):
        response.data = _from_dict(Subscription, response.data)
    return response


def build_subscription_create_body(
    *,
    customer_id: str | None = None,
    plan_code: str | None = None,
    plan_id: str | None = None,
    billing_interval: str | None = None,
    initial_seats: dict[str, int] | None = None,
    skip_trial: bool | None = None,
    name: str | None = None,
    start_date: str | None = None,
    success_url: str | None = None,
) -> dict[str, Any]:
    return build_body(
        customer_id=customer_id,
        plan_code=plan_code,
        plan_id=plan_id,
        billing_interval=billing_interval,
        initial_seats=initial_seats,
        skip_trial=skip_trial,
        name=name,
        start_date=start_date,
        success_url=success_url,
    )


def parse_seat_event(response: ApiResponse[Any]) -> ApiResponse[SeatEvent]:
    if response.data and isinstance(response.data, dict):
        response.data = _from_dict(SeatEvent, response.data)
    return response


def parse_seat_balance(response: ApiResponse[Any]) -> ApiResponse[SeatBalance]:
    if response.data and isinstance(response.data, dict):
        response.data = _from_dict(SeatBalance, response.data)
    return response


def parse_quota_event(response: ApiResponse[Any]) -> ApiResponse[QuotaEvent]:
    if response.data and isinstance(response.data, dict):
        response.data = _from_dict(QuotaEvent, response.data)
    return response


def parse_quota_allowance(response: ApiResponse[Any]) -> ApiResponse[QuotaAllowance]:
    if response.data and isinstance(response.data, dict):
        response.data = _from_dict(QuotaAllowance, response.data)
    return response


def parse_quota_allowance_list(response: ApiResponse[Any]) -> ApiResponse[list[QuotaAllowance]]:
    if response.data and isinstance(response.data, list):
        response.data = _from_list(QuotaAllowance, response.data)
    return response


def build_usage_track_body(
    *,
    feature: str,
    customer_id: str,
    value: int | None = None,
    model: str | None = None,
    input_tokens: int | None = None,
    output_tokens: int | None = None,
    cache_read_tokens: int | None = None,
    cache_write_tokens: int | None = None,
    idempotency_key: str | None = None,
    timestamp: str | None = None,
    properties: dict[str, str] | None = None,
) -> dict[str, Any]:
    props = (
        [{"property": k, "value": v} for k, v in properties.items()] if properties else None
    )

    body = build_body(
        feature=feature,
        customer_id=customer_id,
        idempotency_key=idempotency_key,
        timestamp=timestamp or datetime.now(timezone.utc).isoformat(),
        properties=props,
    )

    if model:
        body.update(build_body(
            model=model,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            cache_read_tokens=cache_read_tokens,
            cache_write_tokens=cache_write_tokens,
        ))
    else:
        if value is not None:
            body["value"] = value

    return body


def parse_usage_event(response: ApiResponse[Any]) -> ApiResponse[UsageEvent]:
    if response.data and isinstance(response.data, dict):
        response.data = _from_dict(UsageEvent, response.data)
    return response


def parse_portal_session(response: ApiResponse[Any]) -> ApiResponse[PortalSession]:
    if response.data and isinstance(response.data, dict):
        response.data = _from_dict(PortalSession, response.data)
    return response


def parse_credit_pack_list(response: ApiResponse[Any]) -> ApiResponse[list[CreditPack]]:
    if response.data and isinstance(response.data, list):
        response.data = _from_list(CreditPack, response.data)
    return response
