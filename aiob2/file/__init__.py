import aiofiles

from ..wrapped_requests import AWR
from ..routes import ROUTES, DL_ROUTES

from .parts import Parts

from .models import FileModel, FileDeleteModel

from .. import bucket


class File:
    def __init__(self, file_id):
        self.file_id = file_id

    async def delete(self, file_name):
        """ https://www.backblaze.com/b2/docs/b2_delete_file_version.html """

        data = await AWR(
            ROUTES.delete_file_version,
            json={
                "fileName": file_name,
                "fileId": self.file_id,
            }
        ).post()

        return FileDeleteModel(data)

    async def info(self):
        """ https://www.backblaze.com/b2/docs/b2_get_file_info.html """

        data = await AWR(
            ROUTES.get_file_info,
            json={
                "fileId": self.file_id,
            }
        ).post()

        return FileModel(data), bucket.Bucket(data["bucketId"])

    async def save(self, pathway):
        """
        Save's file to given pathway.

        Uses download_iterate to avoid heavy memory usage.
        """

        async with aiofiles.open(pathway, mode="wb") as file:
            async for data in self.download_iterate():
                await file.write(data)

    async def download(self):
        """ https://www.backblaze.com/b2/docs/b2_download_file_by_id.html """

        return await AWR(
            DL_ROUTES.file_by_id.format(self.file_id)
        ).get()

    async def download_iterate(self):
        """ https://www.backblaze.com/b2/docs/b2_download_file_by_id.html """

        request = AWR(
            DL_ROUTES.file_by_id.format(self.file_id)
        )

        async for response in request.get_streamed():
            yield response

    @property
    def parts(self):
        """ Parts Object """

        return Parts(file_id=self.file_id)
