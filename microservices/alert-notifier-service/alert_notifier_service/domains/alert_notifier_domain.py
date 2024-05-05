from alert_notifier_service.domains.alert_notifier_domain_base import IAlertNotifierDomain, AlertItem, AlertResponse
from alert_notifier_service.clients.alert_notifier_client import AlertNotifierClient


class AlertNotifierDomain(IAlertNotifierDomain):
    @classmethod
    async def notify(cls, *, alert_item: AlertItem) -> AlertResponse:
        return await AlertNotifierClient.notify(alert_item=alert_item)

    @classmethod
    async def notify_all(cls, *, alert_item: AlertItem) -> AlertResponse:
        return await AlertNotifierClient.notify_all(alert_item=alert_item)
