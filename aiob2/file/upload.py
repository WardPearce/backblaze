from ..wrapped_requests import AWR
from ..routes import ROUTES
from ..cache import CACHE
from ..resources import CONFIG
from ..utils import part_number, get_sha1

from datetime import datetime, timedelta


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

        return await AWR(
            ROUTES.get_upload_part_url,
            json={
                "fileId": self.file_id,
            }
        ).post()

    async def part(self, data, bytes_count, x_bz_part_number: int):
        """ https://www.backblaze.com/b2/docs/b2_upload_part.html """

        upload_url = await self._cached_upload()

        part_number(x_bz_part_number)
        headers = {
            "Authorization": upload_url["authorizationToken"],
            "X-Bz-Part-Number": x_bz_part_number,
            "Content-Length": str(bytes_count),
            "X-Bz-Content-Sha1": get_sha1(data),
        }

        return AWR(
            upload_url["uploadUrl"],
            headers=headers,
            data=data,
        ).post()

    async def cancel(self):
        """ https://www.backblaze.com/b2/docs/b2_cancel_large_file.html """

        return AWR(
            ROUTES.cancel_large_file,
            json={
                "fileId": self.file_id,
            }
        ).post()
