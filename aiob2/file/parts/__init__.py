from ...wrapped_requests import AWR
from ...routes import ROUTES

from .upload import Upload

from ..models import PartModel, FileModel

from ... import bucket


class Parts:
    def __init__(self, file_id):
        self.file_id = file_id

    async def list(self, **kwargs):
        """ https://www.backblaze.com/b2/docs/b2_list_parts.html """

        data = await AWR(
            ROUTES.list_parts,
            json={
                "fileId": self.file_id,
                **kwargs,
            }
        ).post()

        for part in data["parts"]:
            yield PartModel(part)

    async def finish(self, part_sha1_array):
        """ https://www.backblaze.com/b2/docs/b2_finish_large_file.html """

        data = await AWR(
            ROUTES.finish_large_file,
            json={
                "fileId": self.file_id,
                "partSha1Array": part_sha1_array,
            }
        ).post()

        return FileModel(data), bucket.Bucket(data["bucketId"])

    @property
    def upload(self):
        """ Upload Object. """

        return Upload(file_id=self.file_id)
