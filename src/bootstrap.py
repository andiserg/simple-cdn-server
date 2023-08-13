import asyncio

from aiohttp import web

from src.abstract.event_manager import AEventManager
from src.context import Context
from src.routes import get_handlers
from src.services.event_manager import EventManager
from src.services.file_cleaner import start_file_cleaner
from src.services.handlers import EVENT_HANDLERS


def init_app() -> web.Application:
    """Creating and configuring a web server."""
    # creating an event manager and subscribing services handlers to events
    event_manager = subscribe_handlers(EventManager())
    # context that contains all the necessary tools for work
    context = Context(event_manager)
    app = web.Application()
    app["context"] = context
    # handlers for web requests to the server
    handlers = get_handlers(context)
    app.add_routes(handlers)
    # configure methods for starting and cleaning up background tasks
    app.on_startup.append(start_background_tasks)
    app.on_cleanup.append(cleanup_background_tasks)
    return app


async def start_background_tasks(app: web.Application):
    # launching file system cleaner task
    app["file_cleaner_task"] = asyncio.create_task(start_file_cleaner(app["context"]))


async def cleanup_background_tasks(app: web.Application):
    # file system cleaner task completed
    app["file_cleaner_task"].cancel()


def subscribe_handlers(event_manager: AEventManager) -> AEventManager:
    """Subscribing handlers to events."""
    for event_class, handlers in EVENT_HANDLERS.items():
        for handler in handlers:
            event_manager.subscribe(event_class, handler)
    return event_manager
