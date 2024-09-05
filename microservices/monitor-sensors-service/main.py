import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from starlette import status
from typing import Any
from monitor_sensors_service.models.sensor_models import \
    (SensorItem, SensorResponse, ClientError, ServerError)

from monitor_sensors_service.resources.defines import register_exceptions_handlers
from monitor_sensors_service.domains.sensor_monitor_domain import SensorMonitorDomain
from monitor_sensors_service.api.middlewares import setup_middlewares
from monitor_sensors_service.resources.config import Configuration, _get_config


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("startup has begun!!")
    yield
    print('App was ended gracefully.')


app = FastAPI(lifespan=lifespan)
register_exceptions_handlers(app)
origins = [
    "*"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
setup_middlewares(app)

app_config: Configuration = _get_config()


async def sensor_handle(item: SensorItem, request: Request) -> SensorResponse:
    sensor_name: str = request.get('path').split('/sensors/')[1]
    sensor: dict[str, Any] = app_config.sensors[sensor_name]
    sensor_name = sensor['type']
    valid_range: list[int] = sensor['valid_range']

    res: bool = await SensorMonitorDomain.data_feeder(class_name=sensor_name, value=item.value, app_config=app_config)
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
