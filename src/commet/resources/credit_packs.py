from __future__ import annotations

from .._http import ApiResponse, CommetHTTPClient
from .._resource_mixins import parse_credit_pack_list
from ..types import CreditPack


class CreditPacksResource:
    def __init__(self, http: CommetHTTPClient) -> None:
        self._http = http

    def list(self) -> ApiResponse[list[CreditPack]]:
        return parse_credit_pack_list(self._http.get("/credit-packs"))
