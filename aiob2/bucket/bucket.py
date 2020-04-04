from upload import Upload
from file import File

class Bucket(object):
    def __init__(self, bucket_id, obj):
        self.obj = obj
        self.bucket_id = bucket_id

    async def unfinished_large_files(self, **kwargs):
        """ https://www.backblaze.com/b2/docs/b2_list_unfinished_large_files.html """

        return await self.obj._post(url=self.obj.ROUTES["list_unfinished_large_files"].format(self.obj.api_url),
                                    json={"bucketId": self.bucket_id, **kwargs,})

    @property
    def upload(self):
        """ Upload object """

        return Upload(bucket_id=self.bucket_id, obj=self.obj)

    def file(self, file_name=None):
        """ File object 
                - file_name, not required.
        """

        return File(bucket_id=self.bucket_id, file_name=file_name, obj=self.obj)