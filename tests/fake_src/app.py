from aiohttp import web


async def upload_file_test_endpoint(request: web.Request):
    data = await request.post()
    file_info = data["file"]
    filename = file_info.filename
    return web.json_response({"filename": filename}, status=200)


def init_test_app() -> web.Application:
    app = web.Application()
    app.add_routes([web.post("/files/", upload_file_test_endpoint)])
    return app
