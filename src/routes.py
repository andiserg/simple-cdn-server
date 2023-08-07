from datetime import datetime

from aiohttp import web
from aiohttp.web_routedef import RouteDef

from src import utils
from src.abstract.context import AContext
from src.domain import events
from src.services import commands
from src.utils import get_unique_filename


def get_handlers(context: AContext) -> list[RouteDef]:
    handlers = Handlers(context)
    return [
        web.post("/files/", handlers.download_file_from_link_handler),
    ]


class Handlers:
    def __init__(self, context: AContext):
        self.context = context

    async def download_file_from_link_handler(self, request: web.Request):
        # checking the presence of required fields
        data = await request.post()
        link = data.get("link")
        if not link:
            raise web.HTTPBadRequest(reason="link is required.")

        timer = utils.Timer()
        # starting the timer for measuring the download time of the file
        async with timer:
            # set file name
            file_name = await get_unique_filename(self.context)
            # downloading and saving file in the file system
            file = await commands.download_and_save_file(
                self.context,
                link,
                self.context.FILES_DIR,
                file_name,
                self.context.files.save_file,
            )

        event = events.FileSavedEvent(file)
        await self.context.events.publish(self.context, event)

        # generating the response
        response = {
            "name": await self.context.env.get("NAME"),
            "city": await self.context.env.get("CITY"),
            "ip": await self.context.env.get("IP"),
            "download_duration": timer.execution_time,
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "file_link": f"{await self.context.env.get('FILES_URL')}/files/{file_name}",
            "origin_link": link,
        }
        return web.json_response(response, status=200)

    async def file_status_handler(self):
        pass

    async def upload_file_handler(self, request: web.Request):
        pass
