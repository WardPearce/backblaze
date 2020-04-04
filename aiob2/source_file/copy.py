class Copy(object):
    def __init__(self, source_file_id, obj):
        self.source_file_id = source_file_id
        self.obj = obj

    async def part(self, large_file_id, part_number, **kwargs):
        """ https://www.backblaze.com/b2/docs/b2_copy_part.html """

        self.obj.part_number(part_number)

        return await self.obj._post(self.obj.ROUTES["copy_part"].format(self.obj.api_url),
                                    json={"sourceFileId": self.source_file_id, "largeFileId": large_file_id, 
                                          "partNumber": part_number, **kwargs,})

    async def file(self, file_name, **kwargs):
        """ https://www.backblaze.com/b2/docs/b2_copy_file.html """

        return await self.obj._post(self.obj.ROUTES["copy_file"].format(self.obj.api_url),
                                    json={"sourceFileId": self.source_file_id, 
                                          "fileName": file_name, **kwargs,})