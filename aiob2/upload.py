class B2Upload(object):
    def __init__(self, obj):
        self.obj = obj

    async def file(self, bucket_id, file_name, file_pathway, content_type="b2/x-auto", **kwargs):
        """ https://www.backblaze.com/b2/docs/b2_upload_file.html 

                bucket_id, id of the bucket to upload to.
                file_name, name to save it under on the bucket.
                file_pathway, pathway to the file.
                content_type, content type to post with, defaults to b2/x-auto.
        """

        upload_url = await self.obj.get.upload_url(bucket_id)
        if upload_url != False:
            file_content = await self.obj.read_file(file_pathway)

            headers = {
                "Authorization": upload_url["authorizationToken"],
                "X-Bz-File-Name": file_name,
                "Content-Type": content_type,
                "Content-Length": file_content["bytes"],
                "X-Bz-Content-Sha1": file_content["sha1"],
                **kwargs,
            }

            return await self.obj._post(upload_url["uploadUrl"], headers=headers, data=file_content["data"])

        return False

    async def data(self, bucket_id, upload_data, file_name, content_type="b2/x-auto", **kwargs):
        """ https://www.backblaze.com/b2/docs/b2_upload_file.html
                bucket_id, id of the bucket to upload to.
                upload_data, data to upload.
                file_name, name to save it under on the bucket.
                content_type, content type to post with, defaults to b2/x-auto.
        """

        upload_url = await self.obj.get.upload_url(bucket_id)
        if upload_url != False:
            headers = {
                "Authorization": upload_url["authorizationToken"],
                "X-Bz-File-Name": file_name,
                "Content-Type": content_type,
                "Content-Length": str(len(upload_data)),
                "X-Bz-Content-Sha1": self.obj.get_sha1(upload_data),
                **kwargs,
            }

            return await self.obj._post(upload_url["uploadUrl"], headers=headers, data=upload_data)

        return False

    async def part(self, file_id, part_data, bytes_count, x_bz_part_number: int):
        """ https://www.backblaze.com/b2/docs/b2_upload_part.html """

        upload_url = await self.obj.get.part_url(file_id)
        if upload_url != False:
            self.obj.part_number(x_bz_part_number)

            headers = {
                "Authorization": upload_url["authorizationToken"],
                "X-Bz-Part-Number": x_bz_part_number,
                "Content-Length": str(bytes_count),
                "X-Bz-Content-Sha1": self.obj.get_sha1(part_data),
            }

            return await self.obj._post(upload_url["uploadUrl"], headers=headers, data=part_data)

        return False