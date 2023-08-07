import asyncio
from collections import defaultdict
from typing import Callable, Type

from src.abstract.context import AContext
from src.abstract.event_manager import AEventManager
from src.domain.events import Event


class EventManager(AEventManager):
    def __init__(self):
        self.subscribers = defaultdict(list)

    def subscribe(self, event_class: Type[Event], callback: Callable):
        """
        Add a method as a handler for an event.
        :param event_class: Event class
        :param callback: callable method
        """
        self.subscribers[event_class].append(callback)

    async def publish(self, context: AContext, event: Event):
        """
        Run event handlers in the background in an asynchronous mode
        :param context: Context. Needed for method execution
        :param event: object of a child class of the Event class
        """
        if type(event) in self.subscribers:
            for callback in self.subscribers[type(event)]:
                # launching a background asynchronous task for the event handler.
                asyncio.create_task(callback(context, event))
