import asyncio

import pytest


@pytest.mark.asyncio
async def test_download_file_with_correct_data_return_link(cli, test_server):
    await test_server

    file_link = "https://freetestdata.com/wp-content/uploads/2023/04/1.05KB_JSON-File_FreeTestData.json"
    response = await cli.post("/files/", data={"link": file_link})
    await asyncio.sleep(1)

    assert response.status == 200
