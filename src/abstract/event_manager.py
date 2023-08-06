from abc import ABC, abstractmethod
from typing import Callable

from src.context import Context
from src.domain.events import Event


class AEventManager(ABC):
    @abstractmethod
    async def subscribe(self, event_class: Event, callback: Callable):
        pass

    @abstractmethod
    async def publish(self, context: Context, event: Event):
        pass
