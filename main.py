import os
from aiohttp import web

routes = web.RouteTableDef()


@routes.get('/')
async def get_zone(request: web.Request):
    return web.Response(text=os.environ.get("ZONE"))


app = web.Application()
app.add_routes(routes)
web.run_app(app)
