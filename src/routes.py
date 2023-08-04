import os

from aiohttp import web
from aiohttp.web_routedef import RouteDef

from src.context import Context


def get_handlers(context: Context) -> list[RouteDef]:
    handlers = Handlers(context)
    return [
        web.get("/", handlers.get_zone),
        web.post("/files/", handlers.download_file_handler),
    ]


class Handlers:
    def __init__(self, context: Context):
        self.context = context

    async def get_zone(self, request: web.Request):
        return web.Response(text=os.environ.get("ZONE"))

    async def download_file_handler(self, request: web.Request):
        data = await request.post()
        link = data.get("link")
        if not link:
            raise web.HTTPBadRequest(reason="link is required.")
        return web.json_response({"link": ""}, status=200)
