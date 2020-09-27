import unittest

from uuid import uuid4
from os import path

from .client import CLIENT

from ...settings import BucketSettings, UploadSettings

from ...models.file import FileModel

from ...bucket.blocking import BlockingFile


class TestBlockingFile(unittest.TestCase):
    def test_file(self):
        _, bucket = CLIENT.create_bucket(BucketSettings(
            "file test {}".format(uuid4())
        ))

        local_path = path.join(
            path.dirname(path.realpath(__file__)),
            "../test_file.png"
        )

        data = None
        with open(local_path, "rb") as f:
            data = f.read()

        file_data, file = bucket.upload(
            UploadSettings(
                name="Test file.png"
            ),
            data=data
        )

        self.assertIsInstance(file_data, FileModel)
        self.assertIsInstance(file, BlockingFile)

        self.assertTrue(type(file.download()) == bytes)

        file.delete(
            file_data.file_name
        )

        bucket.delete()
