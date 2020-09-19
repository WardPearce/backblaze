import unittest

from uuid import uuid4

from .shared_vars import CLIENT

from ...settings import BucketSettings

from ...bucket.blocking import BlockingBucket
from ...models.bucket import BucketModel


class TestBucketBlocking(unittest.TestCase):
    def test_bucket(self):
        data, bucket = CLIENT.create_bucket(BucketSettings(
            "test-bucket-{}".format(uuid4())
        ))

        self.assertTrue(
            type(data) == BucketModel
        )
        self.assertTrue(
            type(bucket) == BlockingBucket
        )
