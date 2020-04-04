from .upload import Upload

class File(object):
    def __init__(self, file_id, obj):
        self.obj = obj
        self.file_id = file_id

    async def info(self):
        """ https://www.backblaze.com/b2/docs/b2_get_file_info.html """

        return await self.obj._post(url=self.obj.ROUTES["get_file_info"].format(self.obj.api_url),
                                    json={"fileId": self.file_id,})

    async def finish(self, part_sha1_array):
        """ https://www.backblaze.com/b2/docs/b2_finish_large_file.html """

        return await self.obj._post(url=self.obj.ROUTES["finish_large_file"].format(self.obj.api_url),
                                    json={"fileId": self.file_id, "partSha1Array": part_sha1_array,})

    async def download(self):
        """ https://www.backblaze.com/b2/docs/b2_download_file_by_id.html """

        return await self.obj._get(url=self.obj.ROUTES["download_file_by_id"].format(self.obj.api_url, self.file_id), 
                                   headers=self.obj.authorization)

    async def cancel(self):
        """ https://www.backblaze.com/b2/docs/b2_copy_part.html """

        return await self.obj._post(url=self.obj.ROUTES["cancel_large_file"].format(self.obj.api_url),
                                    json={"fileId": self.file_id,})

    async def parts(self, **kwargs):
        """ https://www.backblaze.com/b2/docs/b2_list_parts.html """

        return await self.obj._post(url=self.obj.ROUTES["list_parts"].format(self.obj.api_url),
                                    json={"fileId": self.file_id, **kwargs,})

    @property
    def upload(self):
        """ Upload Object """
        
        return Upload(file_id=self.file_id, obj=self.obj)