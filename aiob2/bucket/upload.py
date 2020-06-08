class Upload:
    def __init__(self, bucket_id):
        self.bucket_id = bucket_id

    async def get(self):
        """ https://www.backblaze.com/b2/docs/b2_get_upload_url.html """

        return await self.obj._post(url=self.obj.ROUTES["get_upload_url"].format(self.obj.api_url),
                                    json={"bucketId": self.bucket_id,})

    async def file(self, file_name, file_pathway, content_type="b2/x-auto", **kwargs):
        """ https://www.backblaze.com/b2/docs/b2_upload_file.html 
                file_name, name to save it under on the bucket.
                file_pathway, pathway to the file.
                content_type, content type to post with, defaults to b2/x-auto.
        """

        upload_url = await self.get()
        if upload_url != False:
            file_content = await self.obj.read_file(file_pathway)

            kwargs = self.obj.format_keys(kwargs)

            headers = {
                "Authorization": upload_url["authorizationToken"],
                "X-Bz-File-Name": file_name,
                "Content-Type": content_type,
                "Content-Length": file_content["bytes"],
                "X-Bz-Content-Sha1": file_content["sha1"],
                **kwargs,
            }

            return await self.obj._post(url=upload_url["uploadUrl"], headers=headers, 
                                        data=file_content["data"])

        return False

    async def data(self, data, file_name, content_type="b2/x-auto", **kwargs):
        """ https://www.backblaze.com/b2/docs/b2_upload_file.html
                data, data to upload.
                file_name, name to save it under on the bucket.
                content_type, content type to post with, defaults to b2/x-auto.
        """

        upload_url = await self.get()
        if upload_url != False:
            kwargs = self.obj.format_keys(kwargs)

            headers = {
                "Authorization": upload_url["authorizationToken"],
                "X-Bz-File-Name": file_name,
                "Content-Type": content_type,
                "Content-Length": str(len(data)),
                "X-Bz-Content-Sha1": self.obj.get_sha1(data),
                **kwargs,
            }

            return await self.obj._post(url=upload_url["uploadUrl"], headers=headers, 
                                        data=data)

        return False
