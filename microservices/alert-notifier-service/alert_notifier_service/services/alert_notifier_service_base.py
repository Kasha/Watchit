from abc import ABC, abstractmethod
from alert_notifier_service.models.alert_models import AlertItem, AlertResponse


class IAlertNotifierService(ABC):
    @classmethod
    @abstractmethod
    async def notify(cls, alert_item: AlertItem) -> AlertResponse:
        pass
