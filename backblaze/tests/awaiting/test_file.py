import asynctest
import aiofiles

from uuid import uuid4
from os import path

from .client import CLIENT

from ...settings import (
    BucketSettings,
    UploadSettings,
    PartSettings,
    CopyFileSettings
)

from ...models.file import FileModel, PartModel

from ...bucket.awaiting import AwaitingFile


class TestAwaitingFile(asynctest.TestCase):
    use_default_loop = True

    async def test_file(self):
        _, bucket = await CLIENT.create_bucket(BucketSettings(
            "file test {}".format(uuid4())
        ))

        local_path = path.join(
            path.dirname(path.realpath(__file__)),
            "../test_file.png"
        )

        async with aiofiles.open(local_path, "rb") as f:
            data = await f.read()

        file_data, file = await bucket.upload(
            UploadSettings(
                name="ウィーブ.png"
            ),
            data=data
        )

        self.assertIsInstance(file_data, FileModel)
        self.assertIsInstance(file, AwaitingFile)

        self.assertTrue(type(await file.download()) == bytes)

        copy_data, copy_file = await file.copy(CopyFileSettings(
            "copied file.png"
        ))

        self.assertIsInstance(copy_data, FileModel)
        self.assertIsInstance(copy_file, AwaitingFile)

        async for chunk in file.download_iterate():
            self.assertTrue(type(chunk) == bytes)

        await copy_file.delete()

        await file.delete(
            file_data.file_name
        )

        local_path = path.join(
            path.dirname(path.realpath(__file__)),
            "../parts_test"
        )

        details, file = await bucket.create_part(PartSettings(
            "test part.png"
        ))

        parts = file.parts()

        async with aiofiles.open(local_path, "rb") as f:
            data = await f.read()

        chunk_size = 5000000
        for chunk in range(0, len(data), chunk_size):
            await parts.data(data[chunk:chunk + chunk_size])

        async for part, _ in file.parts().list():
            self.assertIsInstance(part, PartModel)

        await parts.finish()

        await file.delete(details.file_name)

        details, file = await bucket.create_part(PartSettings(
            "test part upload.png"
        ))

        parts = file.parts()

        await parts.file(local_path)
        await parts.finish()

        await file.delete(details.file_name)

        data, file = await bucket.upload_file(
            UploadSettings("test part upload.bin"),
            local_path
        )
        await file.delete(data.file_name)

        local_path = path.join(
            path.dirname(path.realpath(__file__)),
            "../test_file.png"
        )

        data, file = await bucket.upload_file(
            UploadSettings("test upload file.png"),
            local_path
        )
        await file.delete(data.file_name)

        await bucket.delete()
