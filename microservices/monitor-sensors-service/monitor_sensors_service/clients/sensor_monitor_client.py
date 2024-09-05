from typing import Any
import aiohttp
from aiohttp import TraceRequestStartParams, ClientResponse, ClientSession, ClientTimeout
from monitor_sensors_service.services.sensor_monitor_temprature import TempratureSensorService
from monitor_sensors_service.services.sensor_monitor_pressure import PressureSensorService
from monitor_sensors_service.services.sensor_monitor_humidity import HumiditySensorService
from monitor_sensors_service.services.sensor_monitor_n2o import N2OSensorService
from monitor_sensors_service.domains.sensor_monitor_domain_base import ISensorMonitorDomain
from monitor_sensors_service.resources.config import Configuration
from monitor_sensors_service.models.sensor_models import AlertItem, ValidateResponse, ClientError
from monitor_sensors_service.clients.sensor_monitor_client_base import ISensorMonitorClient, ISensorMonitorService, \
    ValidateResponse
from monitor_sensors_service.resources.defines import logger, app_settings, \
    SensorMonitorInternalServerError, SensorMonitorNotFoundError, SensorMonitorBadRequestError


class SensorMonitorClient(ISensorMonitorClient):
    @classmethod
    async def create(cls, *, class_name: str) -> ISensorMonitorService:
        pass

    @classmethod
    async def read(cls, *, class_name: str | ISensorMonitorService) -> bool:
        pass

    @classmethod
    async def save(cls, *, class_name: str | ISensorMonitorService, data: dict[str, Any]) -> bool:
        pass

    @classmethod
    async def validate(cls, *, class_name: str | ISensorMonitorService, value: int) -> bool:
        pass

    @classmethod
    async def valid_range(cls, *, class_name: str | ISensorMonitorService) -> list[int]:
        pass

    @classmethod
    async def __check_response(cls, *, alert_item: AlertItem, response: ClientResponse) -> None:
        if response.status != 200:
            client_error: ClientError = ClientError(**await response.json())

            logger.error(
                f"couldn't send invalid data to alert notifier service. Error: {client_error.dict()} Data: {alert_item}"
            )

            if response.status == SensorMonitorInternalServerError.http_status_code:
                raise SensorMonitorInternalServerError
            elif response.status == SensorMonitorNotFoundError.http_status_code:
                raise SensorMonitorNotFoundError
            elif response.status == SensorMonitorBadRequestError.http_status_code:
                raise SensorMonitorBadRequestError

    @classmethod
    async def __send_notification(cls, alert_item: AlertItem) -> ValidateResponse:
        logger.debug(
            f'Attempting to send invalid data notification to alert notifier service {alert_item.dict()}'
        )
        timeout = ClientTimeout(total=10)
        async with ClientSession(
                timeout=timeout
        ) as session:
            logger.debug(
                f"Posting invalid data notification {alert_item.dict()}",
            )
            async with session.post(
                    f"{app_settings.ALERT_NOTIFIER_SERVICE_HOST}{app_settings.ALERT_NOTIFIER_NOTIFY}",
                    json=alert_item.dict(),
            ) as response:
                await cls.__check_response(alert_item=alert_item, response=response)

                validate_response: ValidateResponse = ValidateResponse(**(await response.json()))
                logger.info(
                    f"Notification was sent successfully, {validate_response.dict()}"
                )
                return validate_response

    @classmethod
    async def data_feeder(cls, *, class_name: str | ISensorMonitorService, value: int, app_config: Configuration)\
            -> bool:
        if isinstance(class_name, str):
            name: str = f'{class_name}Service'
            # No need for object  instance, but class reference for static service call
            sensor_monitor_service = globals()[name]
        else:
            sensor_monitor_service = class_name
        logger.info(f'data_feeder check for {value} in Sensor {sensor_monitor_service.__class__.__name__}')
        validate_response: ValidateResponse = await sensor_monitor_service.validate(value=value, app_config=app_config)
        if not validate_response.res:
            await cls.__send_notification(alert_item=
                                          AlertItem(**{'sensor': validate_response.sensor,
                                                       'value': value,
                                                       'details': validate_response.details}))
        return validate_response.res
