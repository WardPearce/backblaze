import asynctest

from uuid import uuid4

from .client import CLIENT

from ...settings import BucketSettings, BucketUpdateSettings

from ...bucket.awaiting import AwaitingBucket
from ...models.bucket import BucketModel


class TestBucketAwaiting(asynctest.TestCase):
    use_default_loop = True

    async def test_bucket(self):
        data, bucket = await CLIENT.create_bucket(BucketSettings(
            "test-bucket-{}".format(uuid4())
        ))

        await bucket.update(BucketUpdateSettings(
            private=True
        ))

        self.assertIsInstance(
            data, BucketModel
        )
        self.assertTrue(
            type(bucket) == AwaitingBucket
        )

        self.assertIsInstance(
            await bucket.delete(), BucketModel
        )

    async def test_list_buckets(self):
        async for data, bucket in CLIENT.buckets():
            self.assertIsInstance(
                data, BucketModel
            )

            self.assertIsInstance(
                bucket, AwaitingBucket
            )
