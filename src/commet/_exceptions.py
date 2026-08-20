from __future__ import annotations


class CommetError(Exception):
    def __init__(
        self,
        message: str,
        *,
        code: str | None = None,
        status_code: int | None = None,
        details: object = None,
        request_id: str | None = None,
    ) -> None:
        super().__init__(message)
        self.code = code
        self.status_code = status_code
        self.details = details
        self.request_id = request_id

    def to_dict(self) -> dict[str, object]:
        return {
            "message": str(self),
            "code": self.code,
            "status_code": self.status_code,
            "details": self.details,
            "request_id": self.request_id,
        }


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
        request_id: str | None = None,
    ) -> None:
        super().__init__(
            message,
            code=code,
            status_code=status_code,
            details=details,
            request_id=request_id,
        )
        self.type = type
        self.param = param
        self.doc_url = doc_url

    def to_dict(self) -> dict[str, object]:
        return {
            **super().to_dict(),
            "type": self.type,
            "param": self.param,
            "doc_url": self.doc_url,
        }


class CommetValidationError(CommetAPIError):
    def __init__(
        self,
        message: str,
        *,
        validation_errors: dict[str, list[str]],
        status_code: int = 422,
        details: object = None,
        type: str | None = None,
        param: str | None = None,
        doc_url: str | None = None,
        request_id: str | None = None,
    ) -> None:
        super().__init__(
            message,
            status_code=status_code,
            code="validation_error",
            details=details,
            type=type,
            param=param,
            doc_url=doc_url,
            request_id=request_id,
        )
        self.validation_errors = validation_errors

    def to_dict(self) -> dict[str, object]:
        return {**super().to_dict(), "validation_errors": self.validation_errors}
