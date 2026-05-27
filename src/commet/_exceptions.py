from __future__ import annotations


class CommetError(Exception):
    def __init__(
        self,
        message: str,
        *,
        code: str | None = None,
        status_code: int | None = None,
        details: object = None,
    ) -> None:
        super().__init__(message)
        self.code = code
        self.status_code = status_code
        self.details = details


class CommetAPIError(CommetError):
    def __init__(
        self,
        message: str,
        *,
        status_code: int,
        code: str | None = None,
        details: object = None,
        type: str | None = None,
        param: str | None = None,
        doc_url: str | None = None,
    ) -> None:
        super().__init__(message, code=code, status_code=status_code, details=details)
        self.type = type
        self.param = param
        self.doc_url = doc_url


class CommetValidationError(CommetError):
    def __init__(
        self,
        message: str,
        *,
        validation_errors: dict[str, list[str]],
    ) -> None:
        super().__init__(message)
        self.validation_errors = validation_errors
