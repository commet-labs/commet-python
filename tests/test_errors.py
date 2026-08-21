from __future__ import annotations

import pytest

from commet._exceptions import CommetAPIError, CommetValidationError
from commet._shared import handle_error


class TestAPIErrorParsing:
    def test_api_error_from_dict(self) -> None:
        data = {
            "error": {
                "message": "Customer not found",
                "code": "not_found",
                "type": "invalid_request_error",
            }
        }
        with pytest.raises(CommetAPIError) as exc_info:
            handle_error(404, data)
        assert str(exc_info.value) == "Customer not found"
        assert exc_info.value.status_code == 404
        assert exc_info.value.code == "not_found"
        assert exc_info.value.type == "invalid_request_error"

    def test_api_error_from_non_dict(self) -> None:
        with pytest.raises(CommetAPIError) as exc_info:
            handle_error(500, "Internal Server Error")
        assert exc_info.value.status_code == 500

    def test_api_error_with_details(self) -> None:
        data = {
            "error": {
                "message": "Rate limit exceeded",
                "code": "rate_limit",
                "details": {"retry_after": 30},
            }
        }
        with pytest.raises(CommetAPIError) as exc_info:
            handle_error(429, data)
        assert exc_info.value.code == "rate_limit"
        assert exc_info.value.details == {"retry_after": 30}

    def test_api_error_fallback_message(self) -> None:
        with pytest.raises(CommetAPIError) as exc_info:
            handle_error(502, {})
        assert "502" in str(exc_info.value)

    def test_api_error_with_param_and_doc_url(self) -> None:
        data = {
            "error": {
                "message": "Invalid parameter",
                "code": "invalid_param",
                "type": "invalid_request_error",
                "param": "email",
                "doc_url": "https://docs.commet.co/errors/invalid_param",
            }
        }
        with pytest.raises(CommetAPIError) as exc_info:
            handle_error(400, data, "req_server_123")
        assert exc_info.value.param == "email"
        assert exc_info.value.doc_url == "https://docs.commet.co/errors/invalid_param"
        assert exc_info.value.type == "invalid_request_error"
        assert exc_info.value.request_id == "req_server_123"
        assert exc_info.value.to_dict() == {
            "message": "Invalid parameter",
            "code": "invalid_param",
            "status_code": 400,
            "details": None,
            "request_id": "req_server_123",
            "type": "invalid_request_error",
            "param": "email",
            "doc_url": "https://docs.commet.co/errors/invalid_param",
        }

    def test_api_error_falls_back_to_top_level_keys(self) -> None:
        data = {
            "message": "Legacy error format",
            "code": "legacy_error",
        }
        with pytest.raises(CommetAPIError) as exc_info:
            handle_error(400, data)
        assert str(exc_info.value) == "Legacy error format"
        assert exc_info.value.code == "legacy_error"


class TestValidationErrorParsing:
    def test_validation_error_with_fields(self) -> None:
        data = {
            "error": {
                "message": "Validation failed",
                "code": "validation_error",
                "details": [
                    {"field": "email", "message": "Email is required"},
                    {"field": "email", "message": "Must be a valid email"},
                    {"field": "plan_code", "message": "Plan not found"},
                ],
            }
        }
        with pytest.raises(CommetValidationError) as exc_info:
            handle_error(422, data)
        assert str(exc_info.value) == "Validation failed"
        assert exc_info.value.validation_errors["email"] == [
            "Email is required",
            "Must be a valid email",
        ]
        assert exc_info.value.validation_errors["plan_code"] == ["Plan not found"]

    def test_validation_error_missing_field_defaults_to_unknown(self) -> None:
        data = {
            "error": {
                "message": "Validation failed",
                "code": "validation_error",
                "details": [
                    {"message": "Something is wrong"},
                ],
            }
        }
        with pytest.raises(CommetValidationError) as exc_info:
            handle_error(422, data)
        assert "unknown" in exc_info.value.validation_errors

    def test_non_validation_error_code_raises_api_error(self) -> None:
        data = {
            "error": {
                "message": "Unauthorized",
                "code": "unauthorized",
            }
        }
        with pytest.raises(CommetAPIError):
            handle_error(401, data)
