"""Define middlewares for API"""
# TBI UTILS

from fastapi import FastAPI
from starlette.middleware.base import RequestResponseEndpoint

from starlette.requests import Request
from starlette.responses import Response

from alert_notifier_service.resources.defines import logger


def setup_middlewares(app: FastAPI) -> None:
    """setups middlewares"""

    @app.middleware("http")
    async def log_headers(
        request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        logger.debug(
            f"received request - [{request.method}] - {str(request.url)}",
        )
        response = await call_next(request)
        logger.debug(
            f"returned response - [{response.status_code}] - {str(request.url)}",
        )
        return response
