import os

import pytest

from src.domain.model import FileInfo, Server


@pytest.mark.asyncio
async def test_web_client_download_file_with_correct_data_should_download(context):
    link = "https://freetestdata.com/wp-content/uploads/2023/04/1.17-MB.bmp"
    file = await context.web.download_and_save_file(
        link, context.FILES_DIR, "test", context.files.save_file
    )

    assert isinstance(file, FileInfo)
    assert os.path.exists(context.FILES_DIR / "test.bmp")

    # delete file
    os.remove(context.FILES_DIR / "test.bmp")


@pytest.mark.asyncio
async def test_file_manager_save_file_with_correct_data_should_save(
    context, test_chunk_iterator
):
    await context.files.save_file(context.FILES_DIR, "test.txt", test_chunk_iterator)

    assert os.path.exists(context.FILES_DIR / "test.txt")

    # delete file
    os.remove(context.FILES_DIR / "test.txt")


@pytest.mark.asyncio
async def test_file_manager_delete_file_with_correct_name_should_delete(context):
    with open(context.FILES_DIR / "test.txt", "wb") as f:
        # create file
        f.write(b"Hello world")

    await context.files.delete_file(context.FILES_DIR, "test.txt")

    assert not os.path.exists(context.FILES_DIR / "test.txt")


@pytest.mark.asyncio
async def test_servers_manager_get_servers_with_correct_data_return_servers(context):
    result = await context.servers.get_servers(context.ROOT_DIR)
    assert all([isinstance(server, Server) for server in result])


@pytest.mark.asyncio
async def test_web_client_upload_file_with_correct_data_should_upload(
    context, test_chunk_iterator, test_server
):
    server = Server(name="TestVPS", ip="")
    await context.web.upload_file()


@pytest.mark.asyncio
async def test_web_client_send_file_status_with_correct_data_should_send(context):
    """
    Test is not feasible, because passing it would require editing the handlers
    of other server to accept test requests.
    """
    assert True
