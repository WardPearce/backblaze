import asynctest

from uuid import uuid4

from .client import CLIENT

from ...settings import BucketSettings

from ...models.file import FileModel

from ...bucket.awaiting import AwaitingFile


class TestAwaitingFiles(asynctest.TestCase):
    use_default_loop = True

    async def test_file_listing_names(self):
        _, bucket = await CLIENT.create_bucket(BucketSettings(
            "file test {}".format(uuid4())
        ))

        async for data, file, name, id_ in bucket.file_versions():
            self.assertIsInstance(
                data, FileModel
            )

            self.assertIsInstance(
                file, AwaitingFile
            )

            self.assertTrue(type(name) == str)
            self.assertTrue(type(id_) == str)

        async for data, file, name in bucket.file_names():
            self.assertIsInstance(
                data, FileModel
            )

            self.assertIsInstance(
                file, AwaitingFile
            )

            self.assertTrue(type(name) == str)

        await bucket.delete()
