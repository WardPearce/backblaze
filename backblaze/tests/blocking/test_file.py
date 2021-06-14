import unittest

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

        with open(local_path, "rb") as f:
            data = f.read()

        file_data, file = bucket.upload(
            UploadSettings(
                name="ウィーブ.png"
            ),
            data=data
        )

        self.assertIsInstance(file_data, FileModel)
        self.assertIsInstance(file, BlockingFile)

        self.assertTrue(type(file.download()) == bytes)

        copy_data, copy_file = file.copy(CopyFileSettings(
            "copied file.png"
        ))

        self.assertIsInstance(copy_data, FileModel)
        self.assertIsInstance(copy_file, BlockingFile)

        copy_file.delete()

        file.delete(
            file_data.file_name
        )

        local_path = path.join(
            path.dirname(path.realpath(__file__)),
            "../parts_test"
        )

        details, file = bucket.create_part(PartSettings(
            "test part.png"
        ))

        parts = file.parts()

        data = b""
        with open(local_path, "rb") as f:
            data = f.read()

        chunk_size = 5000000
        for chunk in range(0, len(data), chunk_size):
            parts.data(data[chunk:chunk + chunk_size])

        for part, _ in file.parts().list():
            self.assertIsInstance(part, PartModel)

        parts.finish()

        file.delete(details.file_name)

        details, file = bucket.create_part(PartSettings(
            "test part upload.png"
        ))

        parts = file.parts()

        parts.file(local_path)
        parts.finish()

        file.delete(details.file_name)

        data, file = bucket.upload_file(
            UploadSettings("test part.bin"),
            local_path
        )
        file.delete(data.file_name)

        local_path = path.join(
            path.dirname(path.realpath(__file__)),
            "../test_file.png"
        )

        data, file = bucket.upload_file(
            UploadSettings("test file upload.png"),
            local_path
        )
        file.delete(data.file_name)

        bucket.delete()
