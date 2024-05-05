import uvicorn

from fastapi import FastAPI
from starlette import status
from alert_notifier_service.models.alert_models import AlertItem, AlertResponse
from alert_notifier_service.resources.defines import ClientError, ServerError, register_exceptions_handlers

from alert_notifier_service.domains.alert_notifier_domain import AlertNotifierDomain
from alert_notifier_service.api.middlewares import setup_middlewares

app = FastAPI()
register_exceptions_handlers(app)
setup_middlewares(app)


@app.post("/watchit/notify/", responses={
    status.HTTP_200_OK: {
        "description": "Notification was Sent successfully",
        "status": "ok",
    },
    status.HTTP_400_BAD_REQUEST: {
        "description": "Notification Invalid Request",
        "model": ClientError,
    },
    status.HTTP_401_UNAUTHORIZED: {
        "description": "Notification, Un Authorized Access",
        "model": ClientError,
    },
    status.HTTP_500_INTERNAL_SERVER_ERROR: {
        "description": "Notification Internal server error",
        "model": ServerError,
    },
},
          status_code=200)
async def notify(item: AlertItem) -> AlertResponse:
    response: AlertResponse = await AlertNotifierDomain.notify(alert_item=item)
    if not response.res:
        pass
    return response


@app.post("/watchit/notify_all/", responses={
    status.HTTP_200_OK: {
        "description": "Notification was Sent successfully",
        "status": "ok",
    },
    status.HTTP_400_BAD_REQUEST: {
        "description": "Notification Invalid Request",
        "model": ClientError,
    },
    status.HTTP_401_UNAUTHORIZED: {
        "description": "Notification, Un Authorized Access",
        "model": ClientError,
    },
    status.HTTP_500_INTERNAL_SERVER_ERROR: {
        "description": "Notification Internal server error",
        "model": ServerError,
    },
},
          status_code=200)
async def notify_all(item: AlertItem) -> AlertResponse:
    return AlertResponse(sensor=item.sensor, res=True, status="ok", details="Dummy Request - Sent OK")


if __name__ == "__main__":
    uvicorn.run(app="main:app", reload=True, port=8001, host="127.0.0.1")
