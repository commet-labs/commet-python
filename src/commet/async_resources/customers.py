from __future__ import annotations

from typing import Any

from .._async_http import AsyncCommetHTTPClient
from .._http import ApiResponse
from .._resource_mixins import (
    build_customer_batch_body,
    build_customer_create_body,
    build_customer_update_body,
    parse_customer,
    parse_customer_list,
)
from .._shared import build_body
from ..types import Customer


class AsyncCustomersResource:
    def __init__(self, http: AsyncCommetHTTPClient) -> None:
        self._http = http

    async def create(
        self,
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
        idempotency_key: str | None = None,
    ) -> ApiResponse[Customer]:
        body = build_customer_create_body(
            email=email, id=id, full_name=full_name, domain=domain,
            website=website, timezone=timezone, language=language,
            industry=industry, metadata=metadata, address=address,
        )
        return parse_customer(
            await self._http.post("/customers", body, idempotency_key=idempotency_key)
        )

    async def create_batch(
        self,
        customers: list[dict[str, Any]],
        *,
        idempotency_key: str | None = None,
    ) -> ApiResponse[Any]:
        body = build_customer_batch_body(customers)
        return await self._http.post("/customers/batch", body, idempotency_key=idempotency_key)

    async def get(self, customer_id: str) -> ApiResponse[Customer]:
        return parse_customer(await self._http.get(f"/customers/{customer_id}"))

    async def update(
        self,
        customer_id: str,
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
        idempotency_key: str | None = None,
    ) -> ApiResponse[Customer]:
        body = build_customer_update_body(
            email=email, full_name=full_name, domain=domain, website=website,
            timezone=timezone, language=language, industry=industry,
            metadata=metadata, address=address,
        )
        return parse_customer(
            await self._http.put(
                f"/customers/{customer_id}", body, idempotency_key=idempotency_key
            )
        )

    async def list(
        self,
        *,
        is_active: bool | None = None,
        search: str | None = None,
        limit: int | None = None,
        cursor: str | None = None,
    ) -> ApiResponse[list[Customer]]:
        return parse_customer_list(
            await self._http.get("/customers", build_body(
                is_active=is_active, search=search, limit=limit, cursor=cursor,
            ))
        )

    async def archive(
        self, customer_id: str, *, idempotency_key: str | None = None
    ) -> ApiResponse[Customer]:
        return parse_customer(
            await self._http.put(
                f"/customers/{customer_id}", {"is_active": False},
                idempotency_key=idempotency_key,
            )
        )
