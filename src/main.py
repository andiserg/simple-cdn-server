from aiohttp import web

from routes import get_routes

app = web.Application()
app.add_routes(get_routes())
web.run_app(app)
