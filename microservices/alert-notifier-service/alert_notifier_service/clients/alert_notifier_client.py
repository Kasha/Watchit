from alert_notifier_service.clients.alert_notifier_client_base import IAlertNotifierClient, AlertItem, AlertResponse
from alert_notifier_service.services.alert_notifier_log_service import AlertNotifierLogService, AlertResponse


class AlertNotifierClient(IAlertNotifierClient):
    @classmethod
    async def notify(cls, *, alert_item: AlertItem) -> AlertResponse:
        return await AlertNotifierLogService.notify(alert_item=alert_item)

    @classmethod
    async def notify_all(cls, *, alert_item: AlertItem) -> AlertResponse:
        return AlertResponse(details="Dummy response")
