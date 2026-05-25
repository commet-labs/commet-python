from __future__ import annotations

from typing import Any

from .._http import ApiResponse, CommetHTTPClient


class AddonsResource:
    def __init__(self, http: CommetHTTPClient) -> None:
        self._http = http

    def get_active(self, customer_id: str) -> ApiResponse[list[dict[str, Any]]]:
        return self._http.get("/addons/active", {"customer_id": customer_id})
