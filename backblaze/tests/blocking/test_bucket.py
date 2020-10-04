import unittest

from uuid import uuid4

from .client import CLIENT

from ...settings import BucketSettings, BucketUpdateSettings

from ...bucket.blocking import BlockingBucket
from ...models.bucket import BucketModel


class TestBucketBlocking(unittest.TestCase):
    def test_bucket(self):
        data, bucket = CLIENT.create_bucket(BucketSettings(
            "test-bucket-{}".format(uuid4())
        ))

        bucket.update(BucketUpdateSettings(
            private=False
        ))

        self.assertIsInstance(
            data, BucketModel
        )
        self.assertTrue(
            type(bucket) == BlockingBucket
        )

        self.assertIsInstance(
            bucket.delete(), BucketModel
        )

    def test_list_buckets(self):
        for data, bucket in CLIENT.buckets():
            self.assertIsInstance(
                data, BucketModel
            )

            self.assertIsInstance(
                bucket, BlockingBucket
            )
