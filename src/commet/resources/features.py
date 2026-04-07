from __future__ import annotations

from .._http import ApiResponse, CommetHTTPClient


class FeaturesResource:
    def __init__(self, http: CommetHTTPClient) -> None:
        self._http = http

    def get(
        self,
        *,
        code: str,
        customer_id: str,
    ) -> ApiResponse:
        return self._http.get(f"/features/{code}", {"customer_id": customer_id})

    def check(
        self,
        *,
        code: str,
        customer_id: str,
    ) -> ApiResponse:
        result = self._http.get(f"/features/{code}", {"customer_id": customer_id})

        if not result.success or not result.data:
            return ApiResponse(
                success=False,
                data={"allowed": False},
                message=result.message,
            )

        return ApiResponse(
            success=True,
            data={"allowed": result.data.get("allowed", False)},
            message=result.message,
        )

    def can_use(
        self,
        *,
        code: str,
        customer_id: str,
    ) -> ApiResponse:
        return self._http.get(
            f"/features/{code}", {"customer_id": customer_id, "action": "canUse"}
        )

    def list(self, customer_id: str) -> ApiResponse:
        return self._http.get("/features", {"customer_id": customer_id})
