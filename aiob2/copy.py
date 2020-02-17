class B2Copy(object):
    def __init__(self, obj):
        self.obj = obj

    async def part(self, source_file_id, large_file_id, part_number, **kwargs):
        """ https://www.backblaze.com/b2/docs/b2_copy_part.html """

        self.obj.part_number(part_number)

        return await self.obj._post(self.obj.ROUTES["copy_part"].format(self.obj.api_url), headers=self.obj.authorization, 
                                    json={"sourceFileId": source_file_id, "largeFileId": large_file_id, 
                                          "partNumber": part_number, **kwargs})

    async def file(self, source_file_id, file_name, **kwargs):
        """ https://www.backblaze.com/b2/docs/b2_copy_file.html """

        return await self.obj._post(self.obj.ROUTES["copy_file"].format(self.obj.api_url), headers=self.obj.authorization, 
                                    json={"sourceFileId": source_file_id, "fileName": file_name, **kwargs})