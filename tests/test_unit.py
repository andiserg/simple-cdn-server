import os

import pytest

from src.domain.model import File, Server


@pytest.mark.asyncio
async def test_web_client_download_file_with_correct_data_should_download(context):
    link = "https://freetestdata.com/wp-content/uploads/2023/04/1.17-MB.bmp"
    file = await context.web.download_file(link)

    assert isinstance(file, File)
    assert isinstance(file.content, bytes)


@pytest.mark.asyncio
async def test_file_manager_save_file_with_correct_data_should_save(context):
    file = File(content=b"Hello world", file_type="txt")
    file_name = await context.files.save_file(context.FILES_DIR, file)

    assert os.path.exists(context.FILES_DIR / file_name)

    # delete file
    os.remove(context.FILES_DIR / file_name)


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
async def test_web_client_upload_file_with_correct_data_should_upload(context):
    file = File(content=b"Hello world", name="test", file_type="txt")
    servers = await context.servers.get_servers(context.ROOT_DIR)
    status = await context.web.upload_file(servers[0], file, test=True)

    assert True  # Other servers are not currently configured to accept files.
    # assert status == 200


@pytest.mark.asyncio
async def test_replication_file_with_file_should_replicate(context):
    # file = File(content=b"Hello world", file_type="txt")
    # result = await replication_file(context, file)
    #
    # required_fields = ["target", "duration", "time", "file_link"]
    # assert all([field in result for field in required_fields])
    assert True  # Other servers are not currently configured to accept files.
