from aiohttp import web

from src.context import Context
from src.routes import get_handlers


def init_app() -> web.Application:
    context = Context()
    app = web.Application()
    handlers = get_handlers(context)
    app.add_routes(handlers)
    return app


web.run_app(init_app())
