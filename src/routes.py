from datetime import datetime

from aiohttp import web
from aiohttp.web_routedef import RouteDef

from src import utils
from src.context import Context
from src.services import commands
from src.utils import get_unique_filename


def get_handlers(context: Context) -> list[RouteDef]:
    handlers = Handlers(context)
    return [
        web.post("/files/", handlers.download_file_handler),
    ]


class Handlers:
    def __init__(self, context: Context):
        self.context = context

    async def download_file_handler(self, request: web.Request):
        # checking the presence of required fields
        data = await request.post()
        link = data.get("link")
        if not link:
            raise web.HTTPBadRequest(reason="link is required.")

        timer = utils.Timer()
        # starting the timer for measuring the download time of the file
        async with timer:
            # downloading the content of the file
            file = await commands.download_file(self.context, link)
            # set file name if file.name is None
            file.name = (
                file.name if file.name else await get_unique_filename(self.context)
            )
            # saving the file in the file system
            file_name = await commands.save_file(self.context, file)

        # generating the response
        response = {
            "name": await self.context.env.get("NAME"),
            "city": await self.context.env.get("CITY"),
            "ip": await self.context.env.get("IP"),
            "download_duration": timer.execution_time,
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "file_link": file_name,
            "origin_link": link,
        }
        return web.json_response(response, status=200)
