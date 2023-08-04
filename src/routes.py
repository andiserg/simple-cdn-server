import os

from aiohttp import web
from aiohttp.web_routedef import RouteDef

from src import services
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

        file = await services.download_file(self.context, link)
        file.name = file.name if not data.get("name") else data.get("name")
        file_name = await services.save_file(self.context, file)
        return web.json_response({"link": file_name}, status=200)
