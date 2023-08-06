import asyncio
from collections import defaultdict
from typing import Callable

from src.abstract.event_manager import AEventManager
from src.context import Context
from src.domain.events import Event


class EventManager(AEventManager):
    def __int__(self):
        self.subscribers = defaultdict(list)

    async def subscribe(self, event_class: Event, callback: Callable):
        """
        Add a method as a handler for an event.
        :param event_class: Event class
        :param callback: callable method
        """
        self.subscribers[event_class].append(callback)

    async def publish(self, context: Context, event: Event):
        """
        Run event handlers in the background in an asynchronous mode
        :param context: Context. Needed for method execution
        :param event: object of a child class of the Event class
        """
        if type(event) in self.subscribers:
            for callback in self.subscribers[type(event)]:
                # launching a background asynchronous task for the event handler.
                asyncio.create_task(callback(context, event))
