import asyncio

from aiohttp import web

from src.abstract.event_manager import AEventManager
from src.context import Context
from src.routes import get_handlers
from src.services.event_manager import EventManager
from src.services.file_cleaner import start_file_cleaner
from src.services.handlers import EVENT_HANDLERS


def init_app() -> web.Application:
    event_manager = subscribe_handlers(EventManager())
    context = Context(event_manager)
    app = web.Application()
    app["context"] = context
    handlers = get_handlers(context)
    app.add_routes(handlers)

    app.on_startup.append(start_background_tasks)
    app.on_cleanup.append(cleanup_background_tasks)
    return app


async def start_background_tasks(app: web.Application):
    app["file_cleaner_task"] = asyncio.create_task(start_file_cleaner(app["context"]))


async def cleanup_background_tasks(app: web.Application):
    app["file_cleaner_task"].cancel()


def subscribe_handlers(event_manager: AEventManager) -> AEventManager:
    """
    Subscribing handlers to events.
    :param event_manager: event manager
    """
    for event_class, handlers in EVENT_HANDLERS.items():
        for handler in handlers:
            event_manager.subscribe(event_class, handler)
    return event_manager
