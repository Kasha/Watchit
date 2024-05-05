"""! @brief Defines the common required project defines (shared imports, logger, exceptions)"""
# @file defines.py
#
# @section author_configuration Author(s)
# - Created by Liad Kashanovsky on 29/04/2024.
#
# Copyright (c) 2024 Liad Kashanovsky.  All rights reserved.


from abc import ABC, abstractmethod
from typing import Any
from enum import Enum
import logging
from fastapi import FastAPI, Request, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ValidationError
from alert_notifier_service.resources.settings import app_settings
from starlette import status

logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s',
                    filename=app_settings.LOG_FILE_NAME, encoding='utf-8',
                    level=app_settings.LOGGING_LEVEL, datefmt='%Y-%m-%d %H:%M:%S')


class ErrorCode(Enum):
    ALERT_HTTP_INTERNAL_SERVER = 0,
    ALERT_HTTP_PAGE_NOT_FOUND = 1,
    ALERT_HTTP_BAD_REQUEST = 3,
    ALERT_HTTP_UNAUTHORIZED_REQUEST = 4,
    ALERT_RUNTIME_INTERNAL = 5,
    ALERT_RUNTIME_FAILED_TO_OPEN_CONFIG_FILE = 6,
    ALERT_RUNTIME_EMPTY_VALUES_IN_CONFIG = 7,
    ALERT_RUNTIME_FAILED_PUBLISHING_NOTIFICATION = 8


class ClientErrorBase(ABC, Exception):
    def __init__(
            self,
            details: str | None = None,
    ):
        if not details:
            self.details = details

    @property
    @abstractmethod
    def error_code(self) -> int:
        pass

    @property
    @abstractmethod
    def details(self) -> str:
        pass

    def dictionary(self) -> dict[str, Any]:
        return {
            "error_code": self.error_code,
            "details": self.details,
        }

    @classmethod
    def dict(cls) -> dict[str, Any]:
        return cls().dictionary()


class ClientError(BaseModel):
    """Base error response"""

    details: str
    error_code: int


class ServerError(BaseModel):
    details: str
    error_code: int


# HTTP Errors
class AlertInternalServerError(ClientErrorBase):
    error_code: int = ErrorCode.ALERT_HTTP_INTERNAL_SERVER.value
    details: str = "Alert Internal Server Error"
    http_status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR


class AlertNotFoundError(ClientErrorBase):
    error_code: int = ErrorCode.ALERT_HTTP_PAGE_NOT_FOUND.value
    details: str = "Alert not found"
    http_status_code: int = status.HTTP_404_NOT_FOUND


class AlertBadRequestError(ClientErrorBase):
    error_code: int = ErrorCode.ALERT_HTTP_BAD_REQUEST.value
    details: str = "Alert Invalid Data"
    http_status_code: int = status.HTTP_400_BAD_REQUEST


class AlertNotAuthorizedtError(ClientErrorBase):
    error_code: int = ErrorCode.ALERT_HTTP_UNAUTHORIZED_REQUEST.value
    details: str = "Alert, Un Authorized Access"
    http_status_code: int = status.HTTP_401_UNAUTHORIZED


# Server runtime errors
class AlertRuntimeInternalServerError(ClientErrorBase):
    error_code: int = ErrorCode.ALERT_RUNTIME_INTERNAL.value
    details: str = "Internal Runtime Sensor Error"


class AlertRuntimeFailedToReadConfigFileError(ClientErrorBase):
    error_code: int = ErrorCode.ALERT_RUNTIME_FAILED_TO_OPEN_CONFIG_FILE.value
    details: str = "Failed To Read Config File, Runtime Error"


class AlertRuntimeFailedToReadConfigFileError(ClientErrorBase):
    error_code: int = ErrorCode.ALERT_RUNTIME_EMPTY_VALUES_IN_CONFIG.value
    details: str = "Failed To Read Alert Values from Config, Runtime Error"


class AlertRuntimeFailedToPublishNotificationError(ClientErrorBase):
    error_code: int = ErrorCode.ALERT_RUNTIME_FAILED_PUBLISHING_NOTIFICATION.value
    details: str = "Failed Publishing Notification"


def _error_to_json_response(e: ClientErrorBase) -> JSONResponse:
    err_payload = {"details": e.details, "error_code": e.error_code}

    logger.info(f"{err_payload}")
    return JSONResponse(
        status_code=e.http_status_code,
        content=err_payload,
    )


def register_exceptions_handlers(app: FastAPI) -> None:
    """register all custom exceptions handlers to the fastAPI instance"""

    @app.exception_handler(Exception)
    async def server_exception_handler(_request: Request, e: Exception) -> JSONResponse:
        """Handler for all exceptions"""
        message: str = f"{AlertInternalServerError.details} Error:{e}"
        logger.error(message)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "details": message,
            },
        )

    @app.exception_handler(ValidationError)
    async def validation_exception_handler(
            _request: Request, e: ValidationError
    ) -> JSONResponse:
        """Handler for all exceptions"""
        message: str = f"Sensor Monitor, Internal server error - Validation exception handler. Error:{e}"
        logger.error(message)

        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content=e.errors()
        )

    @app.exception_handler(ClientErrorBase)
    async def sensor_exception_handler(
            _request: Request, e: ClientErrorBase
    ) -> JSONResponse:
        return _error_to_json_response(e)

    logger.info("registered exception handlers")

    @app.exception_handler(AlertInternalServerError)
    async def internal_server_error_exception_handler(
            _request: Request, e: AlertInternalServerError
    ) -> JSONResponse:
        """Handler for all exceptions"""
        logger.error(e.details)
        return JSONResponse(
            status_code=e.http_status_code,
            content={"details": e.details, "error_code": e.error_code},
        )

    @app.exception_handler(HTTPException)
    async def http_exception_handler(
            _request: Request, e: HTTPException
    ) -> JSONResponse:
        """Handler for all exceptions"""
        logger.error(f"HTTP exception:{e.detail}")
        return JSONResponse(
            status_code=e.status_code,
            content=jsonable_encoder(e.detail),
        )

    logger.info("registered exception handlers")