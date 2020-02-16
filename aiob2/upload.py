class B2Upload(object):
    def __init__(self, obj):
        self.obj = obj

    async def get_url(self, bucket_id):
        """ https://www.backblaze.com/b2/docs/b2_get_upload_url.html """

        return await self.obj.post(self.obj.ROUTES["get_upload_url"].format(self.obj.api_url), json=self.obj.get_bucket(bucket_id))

    async def get_part_url(self, file_id):
        """ https://www.backblaze.com/b2/docs/b2_get_upload_part_url.html """

        return await self.obj.post(self.obj.ROUTES["get_upload_part_url"].format(self.obj.api_url), json=self.obj.get_file_id(file_id))

    async def file(self, file_name, file_pathway):
        """ https://www.backblaze.com/b2/docs/b2_upload_file.html 
            
                file_name, name to save it under on the bucket.
                file_pathway, pathway to the file.
        """

        file_data = await self.obj.read_file(file_pathway)
        file_name = file_name.encode("utf-8")

    async def part(self, x_bz_part_number: int, content_lenght, x_bz_content_sha1, **kwargs):
        """ https://www.backblaze.com/b2/docs/b2_upload_part.html """

        self.obj.part_number(x_bz_part_number)