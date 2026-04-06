from __future__ import annotations

from .._http import ApiResponse, CommetHTTPClient


class CreditPacksResource:
    def __init__(self, http: CommetHTTPClient) -> None:
        self._http = http

    def list(self) -> ApiResponse:
        return self._http.get("/credit-packs")
