import asynctest
import aiofiles

from uuid import uuid4
from os import path

from .client import CLIENT

from ...settings import BucketSettings, UploadSettings

from ...models.file import FileModel

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

        data = None
        async with aiofiles.open(local_path, "rb") as f:
            data = await f.read()

        file_data, file = await bucket.upload(
            UploadSettings(
                name="Test file.png"
            ),
            data=data
        )

        self.assertIsInstance(file_data, FileModel)
        self.assertIsInstance(file, AwaitingFile)

        self.assertTrue(type(await file.download()) == bytes)

        async for chunk in file.download_iterate():
            self.assertTrue(type(chunk) == bytes)

        await file.delete(
            file_data.file_name
        )

        await bucket.delete()
