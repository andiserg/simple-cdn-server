from aiohttp import web

from src.abstract.event_manager import AEventManager
from src.context import Context
from src.routes import get_handlers
from src.services.event_manager import EventManager
from src.services.handlers import EVENT_HANDLERS


def init_app() -> web.Application:
    event_manager = subscribe_handlers(EventManager())
    context = Context(event_manager)
    app = web.Application()
    handlers = get_handlers(context)
    app.add_routes(handlers)
    return app


def subscribe_handlers(event_manager: AEventManager) -> AEventManager:
    """
    Subscribing handlers to events.
    :param event_manager: event manager
    """
    for event_class, handlers in EVENT_HANDLERS.items():
        map(lambda handler: event_manager.subscribe(event_class, handler), handlers)
    return event_manager
