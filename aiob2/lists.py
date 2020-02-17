class B2List(object):
    def __init__(self, obj):
        self.obj = obj

    async def unfinished_large_files(self, bucket_id, **kwargs):
        """ https://www.backblaze.com/b2/docs/b2_list_unfinished_large_files.html """

        return await self.obj._post(self.obj.ROUTES["list_unfinished_large_files"].format(self.obj.api_url), headers=self.obj.authorization,
                                   json={"bucketId": bucket_id, **kwargs})

    async def parts(self, file_id, **kwargs):
        """ https://www.backblaze.com/b2/docs/b2_list_parts.html """

        return await self.obj._post(self.obj.ROUTES["list_parts"].format(self.obj.api_url), headers=self.obj.authorization,
                                   json={"fileId": file_id, **kwargs})

    async def keys(self, account_id, **kwargs):
        """ https://www.backblaze.com/b2/docs/b2_list_keys.html """

        return await self.obj._post(self.obj.ROUTES["list_keys"].format(self.obj.api_url), headers=self.obj.authorization,
                                   json={"accountId": account_id, **kwargs})

    async def file_versions(self, bucket_id, **kwargs):
        """ https://www.backblaze.com/b2/docs/b2_list_file_versions.html """

        return await self.obj._post(self.obj.ROUTES["list_file_versions"].format(self.obj.api_url), headers=self.obj.authorization,
                                   json={"bucketId": bucket_id,  **kwargs})

    async def file_names(self, bucket_id, **kwargs):
        """ https://www.backblaze.com/b2/docs/b2_list_file_names.html """

        return await self.obj._post(self.obj.ROUTES["list_file_names"].format(self.obj.api_url), headers=self.obj.authorization,
                                   json={"bucketId": bucket_id, **kwargs})

    async def buckets(self, account_id, **kwargs):
        """ https://www.backblaze.com/b2/docs/b2_list_buckets.html """

        return await self.obj._post(self.obj.ROUTES["list_buckets"].format(self.obj.api_url), headers=self.obj.authorization,
                                   json={"accountId": account_id, **kwargs})