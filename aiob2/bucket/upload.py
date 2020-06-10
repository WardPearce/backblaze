from ..wrapped_requests import AWR
from ..routes import ROUTES
from ..utils import format_keys, read_file, get_sha1
from ..cache import CACHE
from ..resources import CONFIG

from .models import GetUploadUrlModel, FileModel

from datetime import datetime, timedelta


class Upload:
    def __init__(self, bucket_id):
        self.bucket_id = bucket_id

    async def _cached_upload(self):
        """
        Checks to see if a valid upload url for this bucket is already cached.
        Backblaze will revoke upload urls after 24 hours, this function ensures
        it isn't older then 23 hours & 58 minutes.
        (giving us 2 minutes to send a request)
        """
        if self.bucket_id in CACHE.bucket_upload_urls:
            if datetime.now() < CACHE.bucket_upload_urls[self.bucket_id][1]:
                return CACHE.bucket_upload_urls[self.bucket_id][0]

        if len(CACHE.bucket_upload_urls) > CONFIG.max_cache:
            CACHE.bucket_upload_urls = {}

        upload_url = await self.get()

        CACHE.bucket_upload_urls[self.bucket_id] = [
            upload_url,
            datetime.now() + timedelta(hours=23.0, minutes=58.0)
        ]

        return upload_url

    async def get(self):
        """ https://www.backblaze.com/b2/docs/b2_get_upload_url.html """

        data = await AWR(
            ROUTES.get_upload_url,
            json={
                "bucketId": self.bucket_id,
            }
        ).post()

        return GetUploadUrlModel(data)

    async def file(self, file_name, file_pathway,
                   content_type="b2/x-auto", **kwargs):
        """ https://www.backblaze.com/b2/docs/b2_upload_file.html
                file_name, name to save it under on the bucket.
                file_pathway, pathway to the file.
                content_type, content type to post with, defaults to b2/x-auto.
        """

        get_upload = await self._cached_upload()

        file_content = await read_file(file_pathway)
        kwargs = format_keys(kwargs)
        headers = {
            "Authorization": get_upload.authorization_token,
            "X-Bz-File-Name": file_name,
            "Content-Type": content_type,
            "Content-Length": file_content["bytes"],
            "X-Bz-Content-Sha1": file_content["sha1"],
            **kwargs,
        }

        data = await AWR(
            get_upload.upload_url,
            headers=headers,
            data=file_content["data"],
        ).post()

        return FileModel(data)

    async def data(self, data, file_name, content_type="b2/x-auto", **kwargs):
        """ https://www.backblaze.com/b2/docs/b2_upload_file.html
                data, data to upload.
                file_name, name to save it under on the bucket.
                content_type, content type to post with, defaults to b2/x-auto.
        """

        get_upload = await self._cached_upload()

        kwargs = format_keys(kwargs)
        headers = {
            "Authorization": get_upload.authorization_token,
            "X-Bz-File-Name": file_name,
            "Content-Type": content_type,
            "Content-Length": str(len(data)),
            "X-Bz-Content-Sha1": get_sha1(data),
            **kwargs,
        }

        data = await AWR(
            get_upload.upload_url,
            headers=headers,
            data=data
        ).post()

        return FileModel(data)
