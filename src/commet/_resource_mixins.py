from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from ._http import ApiResponse
from ._shared import build_body
from .types import (
    ActivateAddonResult,
    ActiveAddon,
    ActiveSubscription,
    Addon,
    AdjustBalanceResult,
    ApiKeyCreated,
    ApiKeyData,
    CanUseResult,
    ChangePlanResult,
    CreateAdjustmentResult,
    CreatedSubscription,
    CreditPack,
    CreditPackDetail,
    Customer,
    CustomersBatchResult,
    DeactivateAddonResult,
    DeleteResult,
    FeatureAccess,
    FeatureManage,
    InvoiceDetail,
    InvoiceDownloadResult,
    InvoiceListItem,
    InvoiceSendResult,
    InvoiceStatusResult,
    Plan,
    PlanDetail,
    PlanFeatureManage,
    PlanGroup,
    PlanGroupDetail,
    PlanManage,
    PlanPriceManage,
    PortalSession,
    PreviewChangeResult,
    PromoCode,
    PromoCodeDetail,
    PurchaseCreditsResult,
    QuotaAllowance,
    QuotaEvent,
    RegionalPriceResult,
    RemoveResult,
    SeatBalance,
    SeatEvent,
    Subscription,
    SubscriptionListItem,
    TopupBalanceResult,
    TransactionDetail,
    TransactionListItem,
    TransactionRefundResult,
    TransactionRetryResult,
    UsageCheckResult,
    UsageEvent,
    WebhookEndpoint,
    WebhookEndpointCreated,
    WebhookTestResult,
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
    id: str | None = None,
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
        id=id,
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
            id=c.get("id"),
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


def parse_change_plan_result(response: ApiResponse[Any]) -> ApiResponse[ChangePlanResult]:
    if response.data and isinstance(response.data, dict):
        response.data = _from_dict(ChangePlanResult, response.data)
    return response


def build_subscription_create_body(
    *,
    customer_id: str | None = None,
    plan_code: str | None = None,
    plan_id: str | None = None,
    billing_interval: str | None = None,
    initial_seats: dict[str, int] | None = None,
    skip_trial: bool | None = None,
    custom_intro_offer: dict[str, Any] | None = None,
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
        custom_intro_offer=custom_intro_offer,
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


def parse_seat_event_list(response: ApiResponse[Any]) -> ApiResponse[list[SeatEvent]]:
    if response.data and isinstance(response.data, list):
        response.data = _from_list(SeatEvent, response.data)
    return response


def parse_seat_balance_map(response: ApiResponse[Any]) -> ApiResponse[dict[str, SeatBalance]]:
    if response.data and isinstance(response.data, dict):
        response.data = {
            key: _from_dict(SeatBalance, value) if isinstance(value, dict) else value
            for key, value in response.data.items()
        }
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


def parse_credit_pack_detail(response: ApiResponse[Any]) -> ApiResponse[CreditPackDetail]:
    if response.data and isinstance(response.data, dict):
        response.data = _from_dict(CreditPackDetail, response.data)
    return response


def parse_customers_batch_result(response: ApiResponse[Any]) -> ApiResponse[CustomersBatchResult]:
    if response.data and isinstance(response.data, dict):
        response.data = _from_dict(CustomersBatchResult, response.data)
    return response


def parse_can_use_result(response: ApiResponse[Any]) -> ApiResponse[CanUseResult]:
    if response.data and isinstance(response.data, dict):
        response.data = _from_dict(CanUseResult, response.data)
    return response


def parse_feature_manage(response: ApiResponse[Any]) -> ApiResponse[FeatureManage]:
    if response.data and isinstance(response.data, dict):
        response.data = _from_dict(FeatureManage, response.data)
    return response


def parse_delete_result(response: ApiResponse[Any]) -> ApiResponse[DeleteResult]:
    if response.data and isinstance(response.data, dict):
        response.data = _from_dict(DeleteResult, response.data)
    return response


def parse_remove_result(response: ApiResponse[Any]) -> ApiResponse[RemoveResult]:
    if response.data and isinstance(response.data, dict):
        response.data = _from_dict(RemoveResult, response.data)
    return response


def parse_invoice_list(response: ApiResponse[Any]) -> ApiResponse[list[InvoiceListItem]]:
    if response.data and isinstance(response.data, list):
        response.data = _from_list(InvoiceListItem, response.data)
    return response


def parse_invoice_detail(response: ApiResponse[Any]) -> ApiResponse[InvoiceDetail]:
    if response.data and isinstance(response.data, dict):
        response.data = _from_dict(InvoiceDetail, response.data)
    return response


def parse_create_adjustment_result(
    response: ApiResponse[Any],
) -> ApiResponse[CreateAdjustmentResult]:
    if response.data and isinstance(response.data, dict):
        response.data = _from_dict(CreateAdjustmentResult, response.data)
    return response


def parse_invoice_download_result(
    response: ApiResponse[Any],
) -> ApiResponse[InvoiceDownloadResult]:
    if response.data and isinstance(response.data, dict):
        response.data = _from_dict(InvoiceDownloadResult, response.data)
    return response


def parse_invoice_send_result(response: ApiResponse[Any]) -> ApiResponse[InvoiceSendResult]:
    if response.data and isinstance(response.data, dict):
        response.data = _from_dict(InvoiceSendResult, response.data)
    return response


def parse_invoice_status_result(response: ApiResponse[Any]) -> ApiResponse[InvoiceStatusResult]:
    if response.data and isinstance(response.data, dict):
        response.data = _from_dict(InvoiceStatusResult, response.data)
    return response


def parse_transaction_list(response: ApiResponse[Any]) -> ApiResponse[list[TransactionListItem]]:
    if response.data and isinstance(response.data, list):
        response.data = _from_list(TransactionListItem, response.data)
    return response


def parse_transaction_detail(response: ApiResponse[Any]) -> ApiResponse[TransactionDetail]:
    if response.data and isinstance(response.data, dict):
        response.data = _from_dict(TransactionDetail, response.data)
    return response


def parse_transaction_refund_result(
    response: ApiResponse[Any],
) -> ApiResponse[TransactionRefundResult]:
    if response.data and isinstance(response.data, dict):
        response.data = _from_dict(TransactionRefundResult, response.data)
    return response


def parse_transaction_retry_result(
    response: ApiResponse[Any],
) -> ApiResponse[TransactionRetryResult]:
    if response.data and isinstance(response.data, dict):
        response.data = _from_dict(TransactionRetryResult, response.data)
    return response


def parse_usage_check_result(response: ApiResponse[Any]) -> ApiResponse[UsageCheckResult]:
    if response.data and isinstance(response.data, dict):
        response.data = _from_dict(UsageCheckResult, response.data)
    return response


def parse_plan_detail(response: ApiResponse[Any]) -> ApiResponse[PlanDetail]:
    if response.data and isinstance(response.data, dict):
        response.data = _from_dict(PlanDetail, response.data)
    return response


def parse_plan_manage(response: ApiResponse[Any]) -> ApiResponse[PlanManage]:
    if response.data and isinstance(response.data, dict):
        response.data = _from_dict(PlanManage, response.data)
    return response


def parse_plan_feature_manage(response: ApiResponse[Any]) -> ApiResponse[PlanFeatureManage]:
    if response.data and isinstance(response.data, dict):
        response.data = _from_dict(PlanFeatureManage, response.data)
    return response


def parse_plan_price_manage(response: ApiResponse[Any]) -> ApiResponse[PlanPriceManage]:
    if response.data and isinstance(response.data, dict):
        response.data = _from_dict(PlanPriceManage, response.data)
    return response


def parse_regional_price_result(response: ApiResponse[Any]) -> ApiResponse[RegionalPriceResult]:
    if response.data and isinstance(response.data, dict):
        response.data = _from_dict(RegionalPriceResult, response.data)
    return response


def parse_plan_group(response: ApiResponse[Any]) -> ApiResponse[PlanGroup]:
    if response.data and isinstance(response.data, dict):
        response.data = _from_dict(PlanGroup, response.data)
    return response


def parse_plan_group_detail(response: ApiResponse[Any]) -> ApiResponse[PlanGroupDetail]:
    if response.data and isinstance(response.data, dict):
        response.data = _from_dict(PlanGroupDetail, response.data)
    return response


def parse_plan_group_list(response: ApiResponse[Any]) -> ApiResponse[list[PlanGroup]]:
    if response.data and isinstance(response.data, list):
        response.data = _from_list(PlanGroup, response.data)
    return response


def parse_promo_code(response: ApiResponse[Any]) -> ApiResponse[PromoCode]:
    if response.data and isinstance(response.data, dict):
        response.data = _from_dict(PromoCode, response.data)
    return response


def parse_promo_code_detail(response: ApiResponse[Any]) -> ApiResponse[PromoCodeDetail]:
    if response.data and isinstance(response.data, dict):
        response.data = _from_dict(PromoCodeDetail, response.data)
    return response


def parse_promo_code_list(response: ApiResponse[Any]) -> ApiResponse[list[PromoCode]]:
    if response.data and isinstance(response.data, list):
        response.data = _from_list(PromoCode, response.data)
    return response


def parse_addon(response: ApiResponse[Any]) -> ApiResponse[Addon]:
    if response.data and isinstance(response.data, dict):
        response.data = _from_dict(Addon, response.data)
    return response


def parse_addon_list(response: ApiResponse[Any]) -> ApiResponse[list[Addon]]:
    if response.data and isinstance(response.data, list):
        response.data = _from_list(Addon, response.data)
    return response


def parse_active_addon_list(response: ApiResponse[Any]) -> ApiResponse[list[ActiveAddon]]:
    if response.data and isinstance(response.data, list):
        response.data = _from_list(ActiveAddon, response.data)
    return response


def parse_api_key(response: ApiResponse[Any]) -> ApiResponse[ApiKeyData]:
    if response.data and isinstance(response.data, dict):
        response.data = _from_dict(ApiKeyData, response.data)
    return response


def parse_api_key_created(response: ApiResponse[Any]) -> ApiResponse[ApiKeyCreated]:
    if response.data and isinstance(response.data, dict):
        response.data = _from_dict(ApiKeyCreated, response.data)
    return response


def parse_api_key_list(response: ApiResponse[Any]) -> ApiResponse[list[ApiKeyData]]:
    if response.data and isinstance(response.data, list):
        response.data = _from_list(ApiKeyData, response.data)
    return response


def parse_created_subscription(response: ApiResponse[Any]) -> ApiResponse[CreatedSubscription]:
    if response.data and isinstance(response.data, dict):
        response.data = _from_dict(CreatedSubscription, response.data)
    return response


def parse_active_subscription(response: ApiResponse[Any]) -> ApiResponse[ActiveSubscription]:
    if response.data and isinstance(response.data, dict):
        response.data = _from_dict(ActiveSubscription, response.data)
    return response


def parse_subscription_list(response: ApiResponse[Any]) -> ApiResponse[list[SubscriptionListItem]]:
    if response.data and isinstance(response.data, list):
        response.data = _from_list(SubscriptionListItem, response.data)
    return response


def parse_preview_change_result(response: ApiResponse[Any]) -> ApiResponse[PreviewChangeResult]:
    if response.data and isinstance(response.data, dict):
        response.data = _from_dict(PreviewChangeResult, response.data)
    return response


def parse_activate_addon_result(response: ApiResponse[Any]) -> ApiResponse[ActivateAddonResult]:
    if response.data and isinstance(response.data, dict):
        response.data = _from_dict(ActivateAddonResult, response.data)
    return response


def parse_deactivate_addon_result(
    response: ApiResponse[Any],
) -> ApiResponse[DeactivateAddonResult]:
    if response.data and isinstance(response.data, dict):
        response.data = _from_dict(DeactivateAddonResult, response.data)
    return response


def parse_adjust_balance_result(response: ApiResponse[Any]) -> ApiResponse[AdjustBalanceResult]:
    if response.data and isinstance(response.data, dict):
        response.data = _from_dict(AdjustBalanceResult, response.data)
    return response


def parse_topup_balance_result(response: ApiResponse[Any]) -> ApiResponse[TopupBalanceResult]:
    if response.data and isinstance(response.data, dict):
        response.data = _from_dict(TopupBalanceResult, response.data)
    return response


def parse_purchase_credits_result(
    response: ApiResponse[Any],
) -> ApiResponse[PurchaseCreditsResult]:
    if response.data and isinstance(response.data, dict):
        response.data = _from_dict(PurchaseCreditsResult, response.data)
    return response


def parse_webhook_endpoint(response: ApiResponse[Any]) -> ApiResponse[WebhookEndpoint]:
    if response.data and isinstance(response.data, dict):
        response.data = _from_dict(WebhookEndpoint, response.data)
    return response


def parse_webhook_endpoint_created(
    response: ApiResponse[Any],
) -> ApiResponse[WebhookEndpointCreated]:
    if response.data and isinstance(response.data, dict):
        response.data = _from_dict(WebhookEndpointCreated, response.data)
    return response


def parse_webhook_endpoint_list(response: ApiResponse[Any]) -> ApiResponse[list[WebhookEndpoint]]:
    if response.data and isinstance(response.data, list):
        response.data = _from_list(WebhookEndpoint, response.data)
    return response


def parse_webhook_test_result(response: ApiResponse[Any]) -> ApiResponse[WebhookTestResult]:
    if response.data and isinstance(response.data, dict):
        response.data = _from_dict(WebhookTestResult, response.data)
    return response
