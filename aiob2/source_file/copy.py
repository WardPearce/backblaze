from ..wrapped_requests import AWR
from ..routes import ROUTES
from ..utils import part_number as _part_number

from ..file.models import PartModel, FileModel

from ..file import File


class Copy:
    def __init__(self, source_file_id):
        self.source_file_id = source_file_id

    async def part(self, large_file_id, part_number, **kwargs):
        """ https://www.backblaze.com/b2/docs/b2_copy_part.html """

        _part_number(part_number)

        data = await AWR(
            ROUTES.copy_part,
            json={
                "sourceFileId": self.source_file_id,
                "largeFileId": large_file_id,
                "partNumber": part_number,
                **kwargs,
            }
        ).post()

        return PartModel(data), File(data["fileId"])

    async def file(self, file_name, **kwargs):
        """ https://www.backblaze.com/b2/docs/b2_copy_file.html """

        data = await AWR(
            ROUTES.copy_file,
            json={
                "sourceFileId": self.source_file_id,
                "fileName": file_name,
                **kwargs,
            }
        ).post()

        return FileModel(data), File(data["fileId"])
