from abc import ABC, abstractmethod
from typing import Any
from ..clients.sensor_monitor_client_base import ISensorMonitorClient
from ..resources.config import Configuration


class ISensorMonitorDomain(ABC):
    @classmethod
    @abstractmethod
    async def create(cls, *, class_name: str) -> ISensorMonitorClient:
        pass

    @classmethod
    @abstractmethod
    async def read(cls, *, class_name: str) -> bool:
        pass

    @classmethod
    @abstractmethod
    async def save(cls, *, class_name: str, data: dict[str, Any]) -> bool:
        pass

    @classmethod
    @abstractmethod
    async def validate(cls, *, class_name: str, value: int) -> bool:
        pass

    @classmethod
    @abstractmethod
    async def valid_range(cls, *, class_name: str) -> list[int]:
        pass

    @classmethod
    @abstractmethod
    async def data_feeder(cls, *, class_name: str, value: int, app_config: Configuration) -> bool:
        pass
