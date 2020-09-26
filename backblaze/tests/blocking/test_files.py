import unittest

from uuid import uuid4

from .client import CLIENT

from ...settings import BucketSettings

from ...models.file import FileModel

from ...bucket.blocking import BlockingFile


class TestBlockingFiles(unittest.TestCase):
    def test_file_listing_names(self):
        _, bucket = CLIENT.create_bucket(BucketSettings(
            "file test {}".format(uuid4())
        ))

        for data, file, name, id_ in bucket.file_versions():
            self.assertIsInstance(
                data, FileModel
            )

            self.assertIsInstance(
                file, BlockingFile
            )

            self.assertTrue(type(name) == str)
            self.assertTrue(type(id_) == str)

        for data, file, name in bucket.file_names():
            self.assertIsInstance(
                data, FileModel
            )

            self.assertIsInstance(
                file, BlockingFile
            )

            self.assertTrue(type(name) == str)

        bucket.delete()
