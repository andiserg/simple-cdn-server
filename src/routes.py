import os

from aiohttp import web


def get_routes() -> web.RouteTableDef:
    routes = web.RouteTableDef()

    @routes.get("/")
    async def get_zone(request: web.Request):
        return web.Response(text=os.environ.get("ZONE"))

    return routes
