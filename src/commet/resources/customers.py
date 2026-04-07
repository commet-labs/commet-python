from __future__ import annotations

from typing import Any

from .._http import ApiResponse, CommetHTTPClient, build_body


class CustomersResource:
    def __init__(self, http: CommetHTTPClient) -> None:
        self._http = http

    def create(
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
    ) -> ApiResponse:
        return self._http.post(
            "/customers",
            build_body(
                billing_email=email,
                external_id=id,
                full_name=full_name,
                domain=domain,
                website=website,
                timezone=timezone,
                language=language,
                industry=industry,
                metadata=metadata,
                address=address,
            ),
            idempotency_key=idempotency_key,
        )

    def create_batch(
        self,
        customers: list[dict[str, Any]],
        *,
        idempotency_key: str | None = None,
    ) -> ApiResponse:
        mapped = [
            build_body(
                billing_email=c.get("email"),
                external_id=c.get("id"),
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
        return self._http.post(
            "/customers/batch", {"customers": mapped}, idempotency_key=idempotency_key
        )

    def get(self, customer_id: str) -> ApiResponse:
        return self._http.get(f"/customers/{customer_id}")

    def update(
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
    ) -> ApiResponse:
        return self._http.put(
            f"/customers/{customer_id}",
            build_body(
                billing_email=email,
                full_name=full_name,
                domain=domain,
                website=website,
                timezone=timezone,
                language=language,
                industry=industry,
                metadata=metadata,
                address=address,
            ),
            idempotency_key=idempotency_key,
        )

    def list(
        self,
        *,
        is_active: bool | None = None,
        search: str | None = None,
        limit: int | None = None,
        cursor: str | None = None,
    ) -> ApiResponse:
        return self._http.get(
            "/customers",
            build_body(
                is_active=is_active,
                search=search,
                limit=limit,
                cursor=cursor,
            ),
        )

    def archive(self, customer_id: str, *, idempotency_key: str | None = None) -> ApiResponse:
        return self._http.put(
            f"/customers/{customer_id}",
            {"is_active": False},
            idempotency_key=idempotency_key,
        )
