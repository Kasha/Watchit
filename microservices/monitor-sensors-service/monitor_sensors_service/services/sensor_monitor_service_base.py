from abc import ABC, abstractmethod
from typing import Any
from monitor_sensors_service.models.sensor_models import ValidateResponse
from monitor_sensors_service.resources.config import app_config
from monitor_sensors_service.resources.defines import logger, SensorRuntimeFailedToReadConfigFileError


class ISensorMonitorService(ABC):
    @classmethod
    @abstractmethod
    async def read(cls) -> Any:
        pass

    @classmethod
    @abstractmethod
    async def save(cls, *, data: dict[str, Any]) -> Any:
        pass

    @classmethod
    @abstractmethod
    async def valid_range(cls) -> list[int]:
        pass

    @classmethod
    async def validate(cls, *, value: int) -> ValidateResponse:
        sensor_name: str = cls.__name__.split("Service")[0]
        logger.info(f"Validate {sensor_name}: {value}")
        # Config.py validates existing and validity of configuration attributes
        sensor: dict[str, Any] = app_config.sensors[sensor_name.lower()]
        sensor_valid_range: list[int] = sensor['valid_range']

        val_low: int = sensor_valid_range[0]
        val_high: int = sensor_valid_range[1]
        if val_low <= value <= val_high:
            message: str = f"Validate {sensor_name}: {value} in range {val_low}-{val_high}"
            logger.info(message)
            return ValidateResponse(sensor=sensor_name, res=True, status="ok", details=message)
        message: str = f"Validate {sensor_name}: {value} Not in range {val_low}-{val_high}"
        logger.info(message)
        return ValidateResponse(sensor=sensor_name, res=False, status="ok", details=message)
