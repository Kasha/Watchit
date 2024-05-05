from typing import Optional
from pydantic import BaseModel


class AlertItem(BaseModel):
    sensor: str
    value: int
    details: str


class AlertResponse(BaseModel):
    sensor: str
    res: bool = True
    status: str = "ok"
    details: str
