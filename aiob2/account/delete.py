class Delete(object):
    def __init__(self, account_id, obj):
        self.obj = obj
        self.account_id = account_id

    async def bucket(self, bucket_id):
        """ https://www.backblaze.com/b2/docs/b2_delete_bucket.html """

        return await self.obj._post(self.obj.ROUTES["delete_bucket"].format(self.obj.api_url),
                                    json={"accountId": self.account_id, "bucketId": bucket_id})