class B2Finish(object):
    def __init__(self, obj):
        self.obj = obj

    async def large_file(self, file_id, part_sha1_array):
        """ https://www.backblaze.com/b2/docs/b2_finish_large_file.html """

        return await self.obj._post(self.obj.ROUTES["finish_large_file"].format(self.obj.api_url), headers=self.obj.authorization, json={"fileId": file_id, "partSha1Array": part_sha1_array})