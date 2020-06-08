from ..wrapped_requests import AWR
from ..routes import ROUTES


class File:
    def __init__(self, bucket_id):
        self.bucket_id = bucket_id

    async def hide(self, file_name):
        """ https://www.backblaze.com/b2/docs/b2_hide_file.html """

        return await AWR(
            ROUTES.hide_file,
            json={
                "bucketId": self.bucket_id,
                "fileName": file_name,
            }
        ).post()

    async def versions(self, **kwargs):
        """ https://www.backblaze.com/b2/docs/b2_list_file_versions.html """

        return await AWR(
            ROUTES.list_file_versions,
            json={
                "bucketId": self.bucket_id,
                **kwargs,
            }
        ).post()

    async def names(self, **kwargs):
        """ https://www.backblaze.com/b2/docs/b2_list_file_names.html """

        return await AWR(
            ROUTES.list_file_names,
            json={
                "bucketId": self.bucket_id,
                **kwargs,
            }
        ).post()

    async def download_authorization(self, file_name_prefix,
                                     valid_duration_in_seconds, **kwargs):
        """
        https://www.backblaze.com/b2/docs/b2_get_download_authorization.html
        """

        return await AWR(
            ROUTES.get_download_authorization,
            json={
                "bucketId": self.bucket_id,
                "fileNamePrefix": file_name_prefix,
                "validDurationInSeconds": valid_duration_in_seconds,
                **kwargs,
            }
        ).post()

    async def unfinished_large_files(self, **kwargs):
        """
        https://www.backblaze.com/b2/docs/b2_list_unfinished_large_files.html
        """

        return await AWR(
            ROUTES.list_unfinished_large_files,
            json={
                "bucketId": self.bucket_id,
                **kwargs,
            }
        ).post()
