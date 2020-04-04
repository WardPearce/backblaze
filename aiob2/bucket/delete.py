class Delete(object):
    def __init__(self, bucket_id, obj):
        self.obj = obj
        self.bucket_id = bucket_id

    async def bucket(self):
        """ https://www.backblaze.com/b2/docs/b2_delete_bucket.html """

        return await self.obj._post(url=self.obj.ROUTES["delete_bucket"].format(self.obj.api_url),
                                    json={"accountId": self.obj.account_id, "bucketId": self.bucket_id,})