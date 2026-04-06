from __future__ import annotations

from .._http import ApiResponse, CommetHTTPClient, build_body


class PortalResource:
    def __init__(self, http: CommetHTTPClient) -> None:
        self._http = http

    def get_url(
        self,
        *,
        customer_id: str | None = None,
        external_id: str | None = None,
        email: str | None = None,
        idempotency_key: str | None = None,
    ) -> ApiResponse:
        return self._http.post(
            "/portal/request-access",
            build_body(customer_id=customer_id, external_id=external_id, email=email),
            idempotency_key=idempotency_key,
        )
