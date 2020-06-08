from .upload import Upload

from .wrapped_requests import AWR
from .routes import ROUTES


class File:
    def __init__(self, file_id):
        self.file_id = file_id

    async def delete(self, file_name):
        """ https://www.backblaze.com/b2/docs/b2_delete_file_version.html """

        return await AWR(
            ROUTES.delete_file_version,
            json={
                "fileName": file_name,
                "fileId": self.file_id,
            }
        ).post()

    async def info(self):
        """ https://www.backblaze.com/b2/docs/b2_get_file_info.html """

        return await AWR(
            ROUTES.get_file_info,
            json={
                "fileId": self.file_id,
            }
        ).post()

    async def finish(self, part_sha1_array):
        """ https://www.backblaze.com/b2/docs/b2_finish_large_file.html """

        return await AWR(
            ROUTES.finish_large_file,
            json={
                "fileId": self.file_id,
                "partSha1Array": part_sha1_array,
            }
        ).post()

    async def download(self):
        """ https://www.backblaze.com/b2/docs/b2_download_file_by_id.html """

        return await AWR(
            ROUTES.download_file_by_id.format(self.file_id)
        ).get()

    async def parts(self, **kwargs):
        """ https://www.backblaze.com/b2/docs/b2_list_parts.html """

        return await AWR(
            ROUTES.list_parts,
            json={
                "fileId": self.file_id,
                **kwargs,
            }
        ).post()

    @property
    def upload(self):
        """ Upload Object """

        return Upload(file_id=self.file_id)
