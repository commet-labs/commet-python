from __future__ import annotations

from .._http import ApiResponse, CommetHTTPClient
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


class TransactionsResource:
    def __init__(self, http: CommetHTTPClient) -> None:
        self._http = http

    def list(
        self,
        *,
        status: TransactionStatus | None = None,
        customer_email: str | None = None,
        limit: int | None = None,
        cursor: str | None = None,
    ) -> ApiResponse[list[TransactionListItem]]:
        return parse_transaction_list(self._http.get("/transactions", build_body(
            status=status, customer_email=customer_email,
            limit=limit, cursor=cursor,
        )))

    def get(self, transaction_id: str) -> ApiResponse[TransactionDetail]:
        return parse_transaction_detail(self._http.get(f"/transactions/{transaction_id}"))

    def refund(
        self,
        transaction_id: str,
        *,
        idempotency_key: str | None = None,
    ) -> ApiResponse[TransactionRefundResult]:
        return parse_transaction_refund_result(self._http.post(
            f"/transactions/{transaction_id}/refund", {}, idempotency_key=idempotency_key,
        ))

    def retry(
        self,
        transaction_id: str,
        *,
        idempotency_key: str | None = None,
    ) -> ApiResponse[TransactionRetryResult]:
        return parse_transaction_retry_result(self._http.post(
            f"/transactions/{transaction_id}/retry", {}, idempotency_key=idempotency_key,
        ))
