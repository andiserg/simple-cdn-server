from aiohttp import web


async def upload_file_test_endpoint(request: web.Request):
    await request.content.read()
    return web.Response(status=200)


async def file_status_test_handler(request: web.Request):
    return web.Response(status=200)


def init_test_app() -> web.Application:
    app = web.Application()
    app.add_routes(
        [
            web.put("/files/", upload_file_test_endpoint),
            web.post("/status/", file_status_test_handler),
        ]
    )
    return app
