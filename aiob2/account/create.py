class Create(object):
    def __init__(self, account_id, obj):
        self.obj = obj
        self.account_id = account_id

    async def key(self, capabilities, key_name, **kwargs):
        """ https://www.backblaze.com/b2/docs/b2_create_key.html """

        return await self.obj._post(self.obj.ROUTES["create_key"].format(self.obj.api_url),
                                    json={"accountId": self.account_id, "capabilities": capabilities, "keyName": key_name, **kwargs,})

    async def bucket(self, bucket_name, bucket_type, **kwargs):
        """ https://www.backblaze.com/b2/docs/b2_create_bucket.html """

        return await self.obj._post(self.obj.ROUTES["create_bucket"].format(self.obj.api_url),
                                    json={"accountId": self.account_id, "bucketName": bucket_name, "bucketType": bucket_type, **kwargs,})