import pytest


@pytest.mark.asyncio
async def test_upload_file(cli):
    file_link = "https://freetestdata.com/wp-content/uploads/2023/04/1.17-MB.bmp"
    response = await cli.post("/files/", data={"link": file_link})
    response_json = await response.json()

    required_fields = [
        "name",
        "city",
        "ip",
        "download_duration",
        "time",
        "file_link",
        "origin_link",
    ]
    assert response.status == 200
    assert all([field in response_json for field in required_fields])
