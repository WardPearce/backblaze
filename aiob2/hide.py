class B2Hide(object):
    def __init__(self, obj):
        self.obj = obj

    async def file(self, bucket_id, file_name):
        """ https://www.backblaze.com/b2/docs/b2_hide_file.html """

        return await self.obj._post(self.obj.ROUTES["hide_file"].format(self.obj.api_url), headers=self.obj.authorization, json={"bucketId": bucket_id, "fileName": file_name})