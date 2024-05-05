from alert_notifier_service.services.alert_notifier_service_base import IAlertNotifierService, AlertItem, AlertResponse
from alert_notifier_service.resources.defines import logger


class AlertNotifierLogService(IAlertNotifierService):
    @classmethod
    async def notify(cls, alert_item: AlertItem) -> AlertResponse:
        logger.info(f'Notification of invalid sensor\'s data: {alert_item}')
        return AlertResponse(res=True, sensor=alert_item.sensor, details=alert_item.details)
