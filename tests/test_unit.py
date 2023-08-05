import os

import pytest

from src.domain import File


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
