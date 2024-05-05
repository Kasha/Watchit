import uvicorn

from fastapi import FastAPI, Request
from starlette import status
from monitor_sensors_service.models.sensor_models import SensorItem, SensorResponse, ClientError, ServerError
from monitor_sensors_service.resources.config import app_config, Any
from monitor_sensors_service.resources.defines import register_exceptions_handlers, \
    SensorRuntimeFailedToReadConfigFileError, logger

from monitor_sensors_service.domains.sensor_monitor_domain import SensorMonitorDomain
from monitor_sensors_service.api.middlewares import setup_middlewares

app = FastAPI()
register_exceptions_handlers(app)
setup_middlewares(app)


async def sensor_handle(item: SensorItem, request: Request) -> SensorResponse:
    sensor_name: str = request.get('path').split('/sensors/')[1]
    sensor: dict[str, Any] = app_config.sensors[sensor_name]
    sensor_name = sensor['type']
    valid_range: list[int] = sensor['valid_range']

    res: bool = await SensorMonitorDomain.data_feeder(class_name=sensor_name, value=item.value)
    if not res:
        # Logic failure
        return SensorResponse(status="failed", details=f"{item.value} not in range: {valid_range}")

    return SensorResponse(status="ok", details="data in range")


# Create and register HTTP Restful Data feeder API for Sensors retrieving and validating data
for sensor_key, v in app_config.sensors.items():
    app.add_api_route(f"/watchit/sensors/{sensor_key}", sensor_handle, methods=["POST"], status_code=200,
                      summary=f" valid range {v['valid_range']}",
                      responses={
                          status.HTTP_200_OK: {
                              "description": "Sensor Monitor Valid Data",
                              "status": "ok",
                          },
                          status.HTTP_400_BAD_REQUEST: {
                              "description": "Sensor Monitor Invalid Data",
                              "model": ClientError,
                          },
                          status.HTTP_401_UNAUTHORIZED: {
                              "description": "Sensor Monitor, Un Authorized Access",
                              "model": ClientError,
                          },
                          status.HTTP_500_INTERNAL_SERVER_ERROR: {
                              "description": "Sensor Monitor Internal server error",
                              "model": ServerError,
                          },
                      }, )

if __name__ == "__main__":
    uvicorn.run(app="main:app", reload=True, port=8000, host="127.0.0.1")
