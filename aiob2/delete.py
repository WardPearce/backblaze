class B2Delete(object):
    def __init__(self, obj):
        self.obj = obj

    async def key(self, application_key_id):
        """ https://www.backblaze.com/b2/docs/b2_delete_key.html """

        return await self.obj._post(self.obj.ROUTES["delete_key"].format(self.obj.api_url), headers=self.obj.authorization, json={"applicationKeyId": application_key_id})

    async def file_version(self, file_name, file_id):
        """ https://www.backblaze.com/b2/docs/b2_delete_file_version.html """

        return await self.obj._post(self.obj.ROUTES["delete_file_version"].format(self.obj.api_url), headers=self.obj.authorization, 
                                    json={"fileName": file_name, "fileId": file_id})

    async def bucket(self, account_id, bucket_id):
        """ https://www.backblaze.com/b2/docs/b2_delete_bucket.html """

        return await self.obj._post(self.obj.ROUTES["delete_bucket"].format(self.obj.api_url), headers=self.obj.authorization, 
                                    json={"accountId": account_id, "bucketId": bucket_id})