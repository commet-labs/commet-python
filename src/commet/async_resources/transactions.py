from __future__ import annotations

from .._async_http import AsyncCommetHTTPClient
from .._http import ApiResponse
from .._resource_mixins import (
    parse_transaction_detail,
    parse_transaction_list,
    parse_transaction_refund_result,
    parse_transaction_retry_result,
)
from .._shared import build_body
from ..types import (
    TransactionDetail,
    TransactionListItem,
    TransactionRefundResult,
    TransactionRetryResult,
    TransactionStatus,
)


class AsyncTransactionsResource:
    def __init__(self, http: AsyncCommetHTTPClient) -> None:
        self._http = http

    async def list(
        self,
        *,
        status: TransactionStatus | None = None,
        customer_email: str | None = None,
        limit: int | None = None,
        cursor: str | None = None,
    ) -> ApiResponse[list[TransactionListItem]]:
        return parse_transaction_list(await self._http.get("/transactions", build_body(
            status=status, customer_email=customer_email,
            limit=limit, cursor=cursor,
        )))

    async def get(self, transaction_id: str) -> ApiResponse[TransactionDetail]:
        return parse_transaction_detail(await self._http.get(f"/transactions/{transaction_id}"))

    async def refund(
        self,
        transaction_id: str,
        *,
        idempotency_key: str | None = None,
    ) -> ApiResponse[TransactionRefundResult]:
        return parse_transaction_refund_result(await self._http.post(
            f"/transactions/{transaction_id}/refund", {}, idempotency_key=idempotency_key,
        ))

    async def retry(
        self,
        transaction_id: str,
        *,
        idempotency_key: str | None = None,
    ) -> ApiResponse[TransactionRetryResult]:
        return parse_transaction_retry_result(await self._http.post(
            f"/transactions/{transaction_id}/retry", {}, idempotency_key=idempotency_key,
        ))
