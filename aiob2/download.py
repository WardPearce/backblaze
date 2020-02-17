class B2Download(object):
    def __init__(self, obj):
        self.obj = obj

    async def file_by_name(self, bucket_name, file_pathway):
        """ https://www.backblaze.com/b2/docs/b2_download_file_by_name.html """

        return await self.obj._get(self.obj.ROUTES["download_file_by_name"].format(self.obj.api_url, bucket_name, file_pathway), headers=self.obj.authorization)

    async def file_by_id(self, file_id):
        """ https://www.backblaze.com/b2/docs/b2_download_file_by_id.html """

        return await self.obj._get(self.obj.ROUTES["download_file_by_id"].format(self.obj.api_url, file_id), headers=self.obj.authorization)