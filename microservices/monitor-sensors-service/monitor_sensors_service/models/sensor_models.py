from pydantic import BaseModel


class AlertItem(BaseModel):
    sensor: str
    value: int
    details: str


class ValidateResponse(BaseModel):
    sensor: str = ""
    res: bool = False
    status: str
    details: str = ""


class ClientError(BaseModel):
    """Base error response"""

    details: str
    error_code: int


class ServerError(BaseModel):
    details: str
    error_code: int


class SensorItem(BaseModel):
    value: int


class SensorResponse(BaseModel):
    status: str
    details: str = ""
