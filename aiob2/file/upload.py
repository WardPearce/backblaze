class Upload(object):
    def __init__(self, file_id, obj):
        self.obj = obj
        self.file_id = file_id

    async def get(self):
        """ https://www.backblaze.com/b2/docs/b2_get_upload_part_url.html """

        return await self.obj._post(url=self.obj.ROUTES["get_upload_part_url"].format(self.obj.api_url),
                                    json={"fileId": self.file_id})

    async def part(self, data, bytes_count, x_bz_part_number: int):
        """ https://www.backblaze.com/b2/docs/b2_upload_part.html """

        upload_url = await self.get()
        if upload_url != False:
            self.obj.part_number(x_bz_part_number)

            headers = {
                "Authorization": upload_url["authorizationToken"],
                "X-Bz-Part-Number": x_bz_part_number,
                "Content-Length": str(bytes_count),
                "X-Bz-Content-Sha1": self.obj.get_sha1(data),
            }

            return await self.obj._post(upload_url["uploadUrl"], headers=headers, data=data)

        return False