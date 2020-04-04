class File(object):
    def __init__(self, bucket_id, file_name, obj):
        self.obj = obj
        self.bucket_id = bucket_id
        self.file_name = file_name

    async def hide(self):
        """ https://www.backblaze.com/b2/docs/b2_hide_file.html """

        return await self.obj._post(url=self.obj.ROUTES["hide_file"].format(self.obj.api_url), 
                                    json={"bucketId": self.bucket_id, "fileName": self.file_name,})

    async def versions(self, **kwargs):
        """ https://www.backblaze.com/b2/docs/b2_list_file_versions.html """

        return await self.obj._post(url=self.obj.ROUTES["list_file_versions"].format(self.obj.api_url),
                                    json={"bucketId": self.bucket_id,  **kwargs,})

    async def names(self, **kwargs):
        """ https://www.backblaze.com/b2/docs/b2_list_file_names.html """

        return await self.obj._post(url=self.obj.ROUTES["list_file_names"].format(self.obj.api_url),
                                    json={"bucketId": self.bucket_id, **kwargs,})

    async def download_authorization(self, file_name_prefix, valid_duration_in_seconds, **kwargs):
        """ https://www.backblaze.com/b2/docs/b2_get_download_authorization.html """

        return await self.obj._post(self.obj.ROUTES["get_download_authorization"].format(self.obj.api_url),
                                   json={"bucketId": self.obj.bucket_id, "fileNamePrefix": file_name_prefix, 
                                         "validDurationInSeconds": valid_duration_in_seconds, **kwargs,})