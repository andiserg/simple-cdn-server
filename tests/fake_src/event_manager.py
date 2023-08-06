from collections import defaultdict
from typing import Callable

from src.abstract.event_manager import AEventManager
from src.context import Context
from src.domain.events import Event


class FakeEventManager(AEventManager):
    def __int__(self):
        self.subscribers = defaultdict(list)
        self.events = []

    async def subscribe(self, event_class: Event, callback: Callable):
        self.subscribers[event_class].append(callback)

    async def publish(self, context: Context, event: Event):
        """
        Recording the published event into a field
        to test whether the services are actually publishing events.
        """
        self.events.append(event)
