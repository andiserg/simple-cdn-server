import os
from datetime import datetime

import pytest

from src.domain.model import FileInfo, Server


@pytest.mark.asyncio
async def test_web_client_download_file_with_correct_data_should_download(
    context, delete_all_files
):
    link = "https://freetestdata.com/wp-content/uploads/2023/04/1.17-MB.bmp"
    file = await context.web.download_and_save_file(
        link, context.FILES_DIR, "test", context.files.save_file
    )

    assert isinstance(file, FileInfo)
    assert os.path.exists(context.FILES_DIR / "test.bmp")


@pytest.mark.asyncio
async def test_file_manager_save_file_with_correct_data_should_save(
    context, test_chunk_iterator_download, delete_all_files
):
    await context.files.save_file(
        context.FILES_DIR, "test.txt", test_chunk_iterator_download
    )

    assert os.path.exists(context.FILES_DIR / "test.txt")


@pytest.mark.asyncio
async def test_servers_manager_get_servers_with_correct_data_return_servers(context):
    result = await context.servers.get_servers(context.ROOT_DIR)
    assert all([isinstance(server, Server) for server in result])


@pytest.mark.asyncio
async def test_web_client_upload_file_with_correct_data_should_upload(
    context, test_chunk_iterator_upload, test_server, delete_all_files
):
    with open(context.FILES_DIR / "test.txt", "wb") as f:
        # create file
        f.write(b"Hello world")

    # run test server
    await test_server
    port = os.environ.get("TEST_SERVER_PORT")
    server = Server(name="TestVPS", url=f"http://127.0.0.1:{port}", zone="test")
    file_info = FileInfo(name="test", file_type="txt", origin_url="test")

    response = await context.web.upload_file(
        server, file_info, test_chunk_iterator_upload
    )
    assert response["status"] == 200
    assert response["server"] == server


@pytest.mark.asyncio
async def test_web_client_send_file_status_with_correct_data_should_send(
    context, test_server
):
    # run test server
    await test_server
    status = {
        "file_url": f"{os.environ.get('FILES_URL')}/files/test.txt",
        "origin_url": "test",
        "duration": 0,
        "time": datetime.now().strftime("%Y-%M-%D %H-%m-%S"),
    }
    origin_url = os.environ.get("ORIGIN_URL")
    await context.web.send_file_status(origin_url, status)
    assert True


@pytest.mark.asyncio
async def test_get_old_files_file_manager_return_files(context, delete_all_files):
    with open(context.FILES_DIR / "test.txt", "wb") as f:
        f.write(b"Hello, world")

    files = await context.files.get_old_files(context.FILES_DIR, 0)

    assert files == ["test.txt"]


@pytest.mark.asyncio
async def test_delete_files_file_manager_with_correct_data_should_delete(context):
    with open(context.FILES_DIR / "test.txt", "wb") as f:
        f.write(b"Hello, world")

    await context.files.delete_files(context.FILES_DIR, ["test.txt"])
    assert not os.path.exists(context.FILES_DIR / "test.txt")
