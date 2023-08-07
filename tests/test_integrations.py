import asyncio
import os

import pytest


@pytest.mark.asyncio
async def test_download_file_from_link_with_correct_data_return_200(cli, test_server):
    await test_server

    file_link = "https://freetestdata.com/wp-content/uploads/2023/04/1.05KB_JSON-File_FreeTestData.json"
    response = await cli.post("/files/", data={"link": file_link})
    await asyncio.sleep(1)

    assert response.status == 200


@pytest.mark.asyncio
async def test_upload_file_with_correct_data_return_200(cli, test_server, context):
    await test_server
    data = b"Hello, world"
    headers = {"FILE_NAME": "test.txt"}

    response = await cli.put("/files/", data=data, headers=headers)
    await asyncio.sleep(1)

    assert response.status == 200

    # delete file
    os.remove(context.FILES_DIR / "test.txt")
