from ...wrapped_requests import AWR
from ...routes import ROUTES
from ...cache import CACHE
from ...resources import CONFIG
from ...utils import part_number, get_sha1

from datetime import datetime, timedelta

from ..models import GetUploadUrlModel, PartModel, PartDeleteModel

from ... import bucket


class Upload:
    def __init__(self, file_id):
        self.file_id = file_id

    async def _cached_upload(self):
        """
        Checks to see if a valid upload url for this file is already cached.
        Backblaze will revoke upload urls after 24 hours, this function ensures
        it isn't older then 23 hours & 58 minutes.
        (giving us 2 minutes to send a request)
        """
        if self.file_id in CACHE.file_upload_urls:
            if datetime.now() < CACHE.file_upload_urls[self.file_id][1]:
                return CACHE.file_upload_urls[self.file_id][0]

        if len(CACHE.file_upload_urls) > CONFIG.max_cache:
            CACHE.file_upload_urls = {}

        upload_url = await self.get()

        CACHE.file_upload_urls[self.file_id] = [
            upload_url,
            datetime.now() + timedelta(hours=23.0, minutes=58.0)
        ]

        return upload_url

    async def get(self):
        """ https://www.backblaze.com/b2/docs/b2_get_upload_part_url.html """

        data = await AWR(
            ROUTES.get_upload_part_url,
            json={
                "fileId": self.file_id,
            }
        ).post()

        return GetUploadUrlModel(data)

    async def data(self, data, bytes_count: int, x_bz_part_number: int):
        """ https://www.backblaze.com/b2/docs/b2_upload_part.html """

        get_upload = await self._cached_upload()

        part_number(x_bz_part_number)
        headers = {
            "Authorization": get_upload.authorization_token,
            "X-Bz-Part-Number": x_bz_part_number,
            "Content-Length": str(bytes_count),
            "X-Bz-Content-Sha1": get_sha1(data),
        }

        data = await AWR(
            get_upload.upload_url,
            headers=headers,
            data=data,
        ).post()

        return PartModel(data)

    async def cancel(self):
        """ https://www.backblaze.com/b2/docs/b2_cancel_large_file.html """

        data = await AWR(
            ROUTES.cancel_large_file,
            json={
                "fileId": self.file_id,
            }
        ).post()

        return PartDeleteModel(data), bucket.Bucket(data["bucketId"])