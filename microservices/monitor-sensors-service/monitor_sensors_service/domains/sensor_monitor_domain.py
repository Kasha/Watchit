from typing import Any
from ..domains.sensor_monitor_domain_base import ISensorMonitorDomain, ISensorMonitorClient
from ..clients.sensor_monitor_client import SensorMonitorClient
from ..resources.defines import logger, SensorMonitorBadRequestError, \
    SensorRuntimeFailedToReadConfigFileError
from ..resources.config import Configuration


class SensorMonitorDomain(ISensorMonitorDomain):
    @classmethod
    async def create(cls, *, class_name: str) -> ISensorMonitorClient:
        pass

    @classmethod
    async def read(cls, *, class_name: str) -> bool:
        pass

    @classmethod
    async def save(cls, *, class_name: str, data: dict[str, Any]) -> bool:
        pass

    @classmethod
    async def validate(cls, *, class_name: str, value: int) -> bool:
        pass

    @classmethod
    async def valid_range(cls, *, class_name: str) -> list[int]:
        pass

    @classmethod
    async def data_feeder(cls, *, class_name: str, value: int, app_config: Configuration) -> bool:
        try:
            return await SensorMonitorClient.data_feeder(class_name=class_name, value=value, app_config=app_config)
        except SensorRuntimeFailedToReadConfigFileError:
            logger.error(SensorRuntimeFailedToReadConfigFileError.dict())
            raise SensorMonitorBadRequestError(SensorRuntimeFailedToReadConfigFileError.details)
        return False
