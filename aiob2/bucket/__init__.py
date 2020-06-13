from .upload import Upload
from .files import Files
from .models import BucketModel, BucketTypes

from ..wrapped_requests import AWR
from ..routes import ROUTES
from ..resources import CONFIG


class Bucket:
    def __init__(self, bucket_id):
        self.bucket_id = bucket_id

    async def create(self, name, type: BucketTypes, **kwargs):
        """ https://www.backblaze.com/b2/docs/b2_create_bucket.html """

        data = await AWR(
            ROUTES.create_bucket,
            json={
                "accountId": CONFIG.account_id,
                "bucketName": name,
                "bucketType": type,
                **kwargs,
            }
        ).post()

        self.bucket_id = data["bucketId"]

        return BucketModel(data)

    @property
    def upload(self):
        """ Upload object """

        return Upload(bucket_id=self.bucket_id)

    @property
    def files(self):
        """ File object """

        return Files(bucket_id=self.bucket_id)

    async def delete(self):
        """ https://www.backblaze.com/b2/docs/b2_delete_bucket.html """

        data = await AWR(
            ROUTES.delete_bucket,
            json={
                "accountId": CONFIG.account_id,
                "bucketId": self.bucket_id,
            },
        ).post()

        return BucketModel(data)
