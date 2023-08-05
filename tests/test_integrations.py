import pytest


@pytest.mark.asyncio
async def test_download_file_with_correct_data_return_link(cli, context):
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

    # delete downloaded file
    await context.files.delete_file(context.FILES_DIR, response_json["file_link"])
