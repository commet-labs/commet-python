from __future__ import annotations

import pytest
import respx
from httpx import Response

from commet import Commet, CommetAPIError


@pytest.fixture
def mock_api() -> respx.MockRouter:
    with respx.mock(base_url="https://commet.co/api/v1") as mock:
        yield mock


class TestInvalidJsonResponse:
    def test_404_with_invalid_json_raises_error(self, mock_api: respx.MockRouter) -> None:
        mock_api.get("/customers/cus_missing").mock(
            return_value=Response(404, text="Not Found")
        )
        with Commet(api_key="ck_test_123") as client:
            with pytest.raises(CommetAPIError) as exc_info:
                client.customers.get("cus_missing")
            assert exc_info.value.status_code == 404
            assert exc_info.value.code == "INVALID_JSON"

    def test_500_with_invalid_json_raises_error(self, mock_api: respx.MockRouter) -> None:
        mock_api.get("/customers/cus_1").mock(
            return_value=Response(500, text="Internal Server Error")
        )
        with Commet(api_key="ck_test_123") as client:
            with pytest.raises(CommetAPIError) as exc_info:
                client.customers.get("cus_1")
            assert exc_info.value.status_code == 500
            assert exc_info.value.code == "INVALID_JSON"

    def test_200_with_invalid_json_raises_error(self, mock_api: respx.MockRouter) -> None:
        mock_api.get("/customers/cus_1").mock(
            return_value=Response(200, text="not json at all")
        )
        with Commet(api_key="ck_test_123") as client:
            with pytest.raises(CommetAPIError) as exc_info:
                client.customers.get("cus_1")
            assert exc_info.value.code == "INVALID_JSON"
