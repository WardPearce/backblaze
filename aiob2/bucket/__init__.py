from .upload import Upload
from .file import File

from .wrapped_requests import AWR
from .routes import ROUTES
from .resources import CONFIG


class Bucket:
    def __init__(self, bucket_id):
        self.bucket_id = bucket_id

    async def create(self, bucket_name, bucket_type, **kwargs):
        """ https://www.backblaze.com/b2/docs/b2_create_bucket.html """

        return await AWR(
            ROUTES.create_bucket,
            json={
                "accountId": CONFIG.account_id,
                "bucketName": bucket_name,
                "bucketType": bucket_type,
                **kwargs,
            }
        ).post()

    async def list(self, **kwargs):
        """ https://www.backblaze.com/b2/docs/b2_list_buckets.html """

        return await AWR(
            ROUTES.list_buckets,
            json={
                "accountId": CONFIG.account_id,
                **kwargs,
            }
        ).post()

    @property
    def upload(self):
        """ Upload object """

        return Upload(bucket_id=self.bucket_id)

    @property
    def file(self):
        """ File object """

        return File(bucket_id=self.bucket_id)

    async def delete(self):
        """ https://www.backblaze.com/b2/docs/b2_delete_bucket.html """

        return await AWR(
            ROUTES.delete_bucket,
            json={
                "bucketId": self.bucket_id,
            },
        ).post()
