import asyncio

from aiohttp import web
from aiohttp.web_routedef import RouteDef

from src.abstract.context import AContext
from src.services import commands
from src.utils import get_unique_filename


def get_handlers(context: AContext) -> list[RouteDef]:
    """Binding handlers to paths."""
    handlers = Handlers(context)
    return [
        web.post("/files/", handlers.download_file_from_link_handler),
        web.put("/files/", handlers.upload_file_handler),
    ]


class Handlers:
    """
    Class with request handlers.
    This structure is designed so that handlers have access to the context through self.
    """

    def __init__(self, context: AContext):
        self.context = context

    async def download_file_from_link_handler(self, request: web.Request):
        """Download and save a file by URL"""
        # checking the presence of required fields
        data = await request.json()
        link = data.get("link")
        if not link:
            raise web.HTTPBadRequest(reason="link is required.")

        # set file name
        file_name = await get_unique_filename(self.context)
        # downloading and saving file in the file system
        asyncio.create_task(
            commands.download_and_save_file(
                self.context,
                link,
                self.context.FILES_DIR,
                file_name,
                self.context.files.save_file,
            )
        )
        data = {"file_name": file_name, "origin_url": link}
        return web.json_response(data, status=200)

    async def upload_file_handler(self, request: web.Request):
        file_name = request.headers["File-Name"]
        # get an iterator for file chunks
        iter_chunks = request.content.iter_chunks()
        result = await commands.save_file(self.context, file_name, iter_chunks)
        if result:
            return web.Response(status=200)
