class B2Cancel(object):
    def __init__(self, obj):
        self.obj = obj

    async def large_file(self, file_id):
        """ https://www.backblaze.com/b2/docs/b2_copy_part.html """

        return await self.obj._post(self.obj.ROUTES["cancel_large_file"].format(self.obj.api_url), headers=self.obj.authorization, 
                                    json={"fileId": file_id})