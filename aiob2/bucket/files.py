from ..wrapped_requests import AWR
from ..routes import ROUTES

from ..file.models import FileModel
from .models import GetDowloadAuthModel

from ..file import File


class Files:
    def __init__(self, bucket_id):
        self.bucket_id = bucket_id

    async def hide(self, file_name):
        """ https://www.backblaze.com/b2/docs/b2_hide_file.html """

        data = await AWR(
            ROUTES.hide_file,
            json={
                "bucketId": self.bucket_id,
                "fileName": file_name,
            }
        ).post()

        return FileModel(data), File(data["fileId"])

    async def versions(self, **kwargs):
        """ https://www.backblaze.com/b2/docs/b2_list_file_versions.html """

        data = await AWR(
            ROUTES.list_file_versions,
            json={
                "bucketId": self.bucket_id,
                **kwargs,
            }
        ).post()

        for file in data["files"]:
            yield FileModel(file), File(file["fileId"])

    async def names(self, **kwargs):
        """ https://www.backblaze.com/b2/docs/b2_list_file_names.html """

        data = await AWR(
            ROUTES.list_file_names,
            json={
                "bucketId": self.bucket_id,
                **kwargs,
            }
        ).post()

        for file in data["files"]:
            yield FileModel(file), File(file["fileId"])

    async def download_authorization(self, file_name_prefix,
                                     valid_duration_in_seconds, **kwargs):
        """
        https://www.backblaze.com/b2/docs/b2_get_download_authorization.html
        """

        data = await AWR(
            ROUTES.get_download_authorization,
            json={
                "bucketId": self.bucket_id,
                "fileNamePrefix": file_name_prefix,
                "validDurationInSeconds": valid_duration_in_seconds,
                **kwargs,
            }
        ).post()

        return GetDowloadAuthModel(data)

    async def unfinished_large_files(self, **kwargs):
        """
        https://www.backblaze.com/b2/docs/b2_list_unfinished_large_files.html
        """

        data = await AWR(
            ROUTES.list_unfinished_large_files,
            json={
                "bucketId": self.bucket_id,
                **kwargs,
            }
        ).post()

        for file in data["files"]:
            yield FileModel(file), File(file["fileId"])
