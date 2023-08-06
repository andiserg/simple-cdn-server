from aiohttp import web

from src.bootstrap import init_app

web.run_app(init_app())
