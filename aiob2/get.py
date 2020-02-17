class B2Get(object):
    def __init__(self, obj):
        self.obj = obj

    async def upload_url(self, bucket_id):
        """ https://www.backblaze.com/b2/docs/b2_get_upload_url.html """

        return await self.obj._post(self.obj.ROUTES["get_upload_url"].format(self.obj.api_url), headers=self.obj.authorization, json={"bucketId": bucket_id})

    async def part_url(self, file_id):
        """ https://www.backblaze.com/b2/docs/b2_get_upload_part_url.html """

        return await self.obj._post(self.obj.ROUTES["get_upload_part_url"].format(self.obj.api_url), headers=self.obj.authorization, json={"fileId": file_id})

    async def file_info(self, file_id):
        """ https://www.backblaze.com/b2/docs/b2_get_file_info.html """

        return await self.obj._post(self.obj.ROUTES["get_file_info"].format(self.obj.api_url), headers=self.obj.authorization, json={"fileId": file_id})

    async def download_authorization(self, bucket_id, file_name_prefix, valid_duration_in_seconds, **kwargs):
        """ https://www.backblaze.com/b2/docs/b2_get_download_authorization.html """

        return await self.obj._post(self.obj.ROUTES["get_download_authorization"].format(self.obj.api_url), headers=self.obj.authorization, 
                                   json={"bucketId": bucket_id, "fileNamePrefix": file_name_prefix, 
                                         "validDurationInSeconds": valid_duration_in_seconds, **kwargs})