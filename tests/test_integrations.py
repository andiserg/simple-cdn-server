import asyncio
import json
import os

import pytest


@pytest.mark.asyncio
async def test_download_file_from_link_with_correct_data_return_200(
    cli, test_server, delete_all_files
):
    await test_server

    file_link = "https://freetestdata.com/wp-content/uploads/2023/04/1.05KB_JSON-File_FreeTestData.json"
    response = await cli.post("/files/", data=json.dumps({"link": file_link}))
    await asyncio.sleep(1)

    assert response.status == 200


@pytest.mark.asyncio
async def test_upload_file_with_correct_data_return_200(
    cli, test_server, context, delete_all_files
):
    await test_server
    data = b"Hello, world"
    headers = {"File-Name": "test.txt"}

    response = await cli.put("/files/", data=data, headers=headers)
    await asyncio.sleep(1)

    assert response.status == 200
