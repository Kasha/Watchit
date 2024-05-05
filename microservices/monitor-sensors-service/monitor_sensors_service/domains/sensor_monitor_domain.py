from typing import Any
from monitor_sensors_service.domains.sensor_monitor_domain_base import ISensorMonitorDomain, ISensorMonitorClient
from monitor_sensors_service.clients.sensor_monitor_client import SensorMonitorClient
from monitor_sensors_service.resources.defines import logger, SensorMonitorBadRequestError, \
    SensorRuntimeFailedToReadConfigFileError


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
    async def data_feeder(cls, *, class_name: str, value: int) -> bool:
        try:
            return await SensorMonitorClient.data_feeder(class_name=class_name, value=value)
        except SensorRuntimeFailedToReadConfigFileError:
            logger.error(SensorRuntimeFailedToReadConfigFileError.dict())
            raise SensorMonitorBadRequestError(SensorRuntimeFailedToReadConfigFileError.details)
        return False
