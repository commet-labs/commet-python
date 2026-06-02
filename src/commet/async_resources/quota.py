from __future__ import annotations

from .._async_http import AsyncCommetHTTPClient
from .._http import ApiResponse
from .._resource_mixins import (
    parse_quota_allowance,
    parse_quota_allowance_list,
    parse_quota_event,
)
from .._shared import build_body
from ..types import QuotaAllowance, QuotaEvent


class AsyncQuotaResource:
    def __init__(self, http: AsyncCommetHTTPClient) -> None:
        self._http = http

    async def add(
        self,
        *,
        feature_code: str,
        count: int = 1,
        customer_id: str,
        idempotency_key: str | None = None,
    ) -> ApiResponse[QuotaEvent]:
        return parse_quota_event(await self._http.post(
            "/usage/quota",
            build_body(featureCode=feature_code, count=count, customerId=customer_id),
            idempotency_key=idempotency_key,
        ))

    async def set(
        self,
        *,
        feature_code: str,
        count: int,
        customer_id: str,
        idempotency_key: str | None = None,
    ) -> ApiResponse[QuotaEvent]:
        return parse_quota_event(await self._http.put(
            "/usage/quota",
            build_body(featureCode=feature_code, count=count, customerId=customer_id),
            idempotency_key=idempotency_key,
        ))

    async def remove(
        self,
        *,
        feature_code: str,
        count: int = 1,
        customer_id: str,
        idempotency_key: str | None = None,
    ) -> ApiResponse[QuotaEvent]:
        return parse_quota_event(await self._http.delete(
            "/usage/quota",
            build_body(featureCode=feature_code, count=count, customerId=customer_id),
            idempotency_key=idempotency_key,
        ))

    async def get(
        self,
        *,
        feature_code: str,
        customer_id: str,
    ) -> ApiResponse[QuotaAllowance]:
        return parse_quota_allowance(await self._http.get(
            "/usage/quota",
            build_body(featureCode=feature_code, customerId=customer_id),
        ))

    async def get_all(
        self,
        *,
        customer_id: str,
    ) -> ApiResponse[list[QuotaAllowance]]:
        return parse_quota_allowance_list(await self._http.get(
            "/usage/quota/all",
            build_body(customerId=customer_id),
        ))
