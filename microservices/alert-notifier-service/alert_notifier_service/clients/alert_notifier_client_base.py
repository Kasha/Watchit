from abc import ABC, abstractmethod
from alert_notifier_service.services.alert_notifier_service_base import AlertItem, AlertResponse


class IAlertNotifierClient(ABC):
    @classmethod
    @abstractmethod
    async def notify(cls, *, alert_item: AlertItem) -> AlertResponse:
        pass

    @classmethod
    @abstractmethod
    async def notify_all(cls, *, alert_item: AlertItem) -> AlertResponse:
        pass
