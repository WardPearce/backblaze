class B2Create(object):
    def __init__(self, obj):
        self.obj = obj

    async def key(self, account_id, capabilities, key_name, **kwargs):
        """ https://www.backblaze.com/b2/docs/b2_create_key.html """

        return await self.obj._post(self.obj.ROUTES["create_key"].format(self.obj.api_url), headers=self.obj.authorization, 
                                    json={"accountId": account_id, "capabilities": capabilities, "keyName": key_name, **kwargs})

    async def bucket(self, account_id, bucket_name, bucket_type, **kwargs):
        """ https://www.backblaze.com/b2/docs/b2_create_bucket.html """

        return await self.obj._post(self.obj.ROUTES["create_bucket"].format(self.obj.api_url), headers=self.obj.authorization, 
                                    json={"accountId": account_id, "bucketName": bucket_name, "bucketType": bucket_type, **kwargs})