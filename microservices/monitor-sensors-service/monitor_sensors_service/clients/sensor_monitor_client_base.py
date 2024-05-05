from abc import ABC, abstractmethod
from typing import Any
from monitor_sensors_service.services.sensor_monitor_service_base import ISensorMonitorService, ValidateResponse


class ISensorMonitorClient(ABC):
    @classmethod
    @abstractmethod
    async def create(cls, *, class_name: str) -> ISensorMonitorService:
        pass

    @classmethod
    @abstractmethod
    async def read(cls, *, class_name: str | ISensorMonitorService) -> bool:
        pass

    @classmethod
    @abstractmethod
    async def save(cls, *, class_name: str | ISensorMonitorService, data: dict[str, Any]) -> bool:
        pass

    @classmethod
    @abstractmethod
    async def validate(cls, *, class_name: str | ISensorMonitorService, value: int) -> bool:
        pass

    @classmethod
    @abstractmethod
    async def valid_range(cls, *, class_name: str | ISensorMonitorService) -> list[int]:
        pass

    @classmethod
    @abstractmethod
    async def data_feeder(cls, *, class_name: str | ISensorMonitorService, value: int) -> bool:
        pass
