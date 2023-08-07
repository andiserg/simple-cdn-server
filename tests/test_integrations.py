import pytest


@pytest.mark.asyncio
async def test_download_file_with_correct_data_return_link(cli):
    file_link = "https://freetestdata.com/wp-content/uploads/2023/04/1.17-MB.bmp"
    response = await cli.post("/files/", data={"link": file_link})

    assert response.status == 200
