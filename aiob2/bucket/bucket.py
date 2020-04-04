from .upload import Upload
from .file import File

class Bucket(object):
    def __init__(self, bucket_id, obj):
        self.obj = obj
        self.bucket_id = bucket_id

    @property
    def upload(self):
        """ Upload object """

        return Upload(bucket_id=self.bucket_id, obj=self.obj)

    @property
    def file(self):
        """ File object """

        return File(bucket_id=self.bucket_id, obj=self.obj)

    async def delete(self):
        """ https://www.backblaze.com/b2/docs/b2_delete_bucket.html """

        return await self.obj._post(url=self.obj.ROUTES["delete_bucket"].format(self.obj.api_url),
                                    json={"accountId": self.obj.account_id, "bucketId": self.bucket_id,})