from monitor_sensors_service.services.sensor_monitor_service_base import ISensorMonitorService, Any


class HumiditySensorService(ISensorMonitorService):
    @classmethod
    async def read(cls) -> Any:
        pass

    @classmethod
    async def save(cls, data: dict[str, Any]) -> Any:
        pass

    @classmethod
    async def valid_range(cls) -> list[int]:
        pass
