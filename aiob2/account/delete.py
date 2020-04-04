class Delete(object):
    def __init__(self, obj):
        self.obj = obj

    async def bucket(self, bucket_id):
        """ https://www.backblaze.com/b2/docs/b2_delete_bucket.html """

        return await self.obj._post(url=self.obj.ROUTES["delete_bucket"].format(self.obj.api_url),
                                    json={"accountId": self.obj.account_id, "bucketId": bucket_id})