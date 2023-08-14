from aiohttp import web

from src.bootstrap import init_app

web.run_app(init_app(), host="0.0.0.0", port=8000)
