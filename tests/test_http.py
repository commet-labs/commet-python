from __future__ import annotations

from commet._shared import convert_keys, to_camel, to_snake


class TestToSnake:
    def test_simple_camel_case(self) -> None:
        assert to_snake("customerId") == "customer_id"

    def test_multiple_words(self) -> None:
        assert to_snake("billingDayOfMonth") == "billing_day_of_month"

    def test_already_snake_case(self) -> None:
        assert to_snake("customer_id") == "customer_id"

    def test_single_word(self) -> None:
        assert to_snake("name") == "name"

    def test_consecutive_capitals(self) -> None:
        assert to_snake("APIKey") == "api_key"

    def test_upper_after_lower(self) -> None:
        assert to_snake("createdAt") == "created_at"


class TestToCamel:
    def test_simple_snake_case(self) -> None:
        assert to_camel("customer_id") == "customerId"

    def test_multiple_words(self) -> None:
        assert to_camel("billing_day_of_month") == "billingDayOfMonth"

    def test_already_camel_case(self) -> None:
        assert to_camel("customerId") == "customerId"

    def test_single_word(self) -> None:
        assert to_camel("name") == "name"


class TestConvertKeys:
    def test_dict_snake_to_camel(self) -> None:
        result = convert_keys({"customer_id": "123", "full_name": "John"}, to_camel)
        assert result == {"customerId": "123", "fullName": "John"}

    def test_dict_camel_to_snake(self) -> None:
        result = convert_keys({"customerId": "123", "fullName": "John"}, to_snake)
        assert result == {"customer_id": "123", "full_name": "John"}

    def test_nested_dict(self) -> None:
        data = {"currentPeriod": {"startDate": "2024-01-01", "endDate": "2024-02-01"}}
        result = convert_keys(data, to_snake)
        assert result == {"current_period": {"start_date": "2024-01-01", "end_date": "2024-02-01"}}

    def test_list_of_dicts(self) -> None:
        data = [{"customerId": "1"}, {"customerId": "2"}]
        result = convert_keys(data, to_snake)
        assert result == [{"customer_id": "1"}, {"customer_id": "2"}]

    def test_non_dict_passthrough(self) -> None:
        assert convert_keys("hello", to_snake) == "hello"
        assert convert_keys(42, to_snake) == 42
        assert convert_keys(None, to_snake) is None
