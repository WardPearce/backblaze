from .upload import Upload
from .file import File

from .wrapped_requests import AWR
from .routes import ROUTES


class Bucket:
    def __init__(self, bucket_id):
        self.bucket_id = bucket_id

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
            url=ROUTES.delete_bucket,
            json={
                "bucketId": self.bucket_id,
            },
        ).post()
