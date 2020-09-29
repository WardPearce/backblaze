import typing
import aiofiles

from ..base import BaseFile

from .part import AwaitingPart

from ...models.file import (
    FileModel,
    UploadUrlModel,
    FileDeleteModel,
    PartCancelModel
)

from ...settings import DownloadSettings

from ...utils import UploadUrlCache


class AwaitingFile(BaseFile):
    def part(self, part_number: int = 0) -> AwaitingPart:
        """Used to upload a part.

        Parameters
        ----------
        part_number : int, optional
            by default 0

        Returns
        -------
        AwaitingPart
        """

        return AwaitingPart(
            self,
            self.context,
            part_number
        )

    async def cancel(self) -> PartCancelModel:
        """Used for cancelling a uncompleted file.

        Returns
        -------
        PartCancelModel
            Holds details on canceled file.
        """

        return PartCancelModel(
            await self.context._post(
                url=self.context._routes.file.cancel_large,
                json={"fileId": self.file_id},
                include_account=False
            )
        )

    async def get(self) -> FileModel:
        """Used to get details on a file.

        Returns
        -------
        FileModel
            Holds details on a file
        """

        return FileModel(
            await self.context._post(
                url=self.context._routes.file.get,
                json={"fileId": self.file_id},
                include_account=False
            )
        )

    async def delete(self, name: str) -> FileDeleteModel:
        """Deletes give file.

        Parameters
        ----------
        name : str
            Name of file.

        Returns
        -------
        FileDeleteModel
            Holds details on delete file.
        """

        return FileDeleteModel(
            await self.context._post(
                url=self.context._routes.file.delete,
                json={"fileName": name, "fileId": self.file_id},
                include_account=False
            )
        )

    async def upload_url(self) -> UploadUrlModel:
        """Used to get a part upload URL.

        Returns
        -------
        UploadUrlModel
            Holds details on the upload URL.

        Notes
        -----
        Caching is used.
        """

        cache = UploadUrlCache(self.bucket_id, parts=True)

        upload_url = cache.find()
        if upload_url:
            return upload_url

        return cache.save(UploadUrlModel(
            await self.context._post(
                url=self.content._routes.upload.upload_part,
                json={
                    "bucketId": self.bucket_id,
                    "fileId": self.file_id
                }
            )
        ))

    async def download(self, settings: DownloadSettings = None) -> bytes:
        """Used to download file into memory.

        Parameters
        ----------
        settings : DownloadSettings

        Returns
        -------
        bytes
        """

        if not settings:
            params = {"fileId": self.file_id}
            headers = None
        else:
            params = {"fileId": self.file_id, **settings.parameters}
            headers = settings.headers

        return await self.context._get(
            url=self.context._routes.file.download_by_id,
            headers=headers,
            params=params,
            resp_json=False,
            include_account=False,
        )

    async def download_iterate(self, settings: DownloadSettings = None
                               ) -> typing.AsyncGenerator[bytes, None]:
        """Used to iterate over the download.

        Parameters
        ----------
        settings : DownloadSettings

        Yields
        -------
        bytes

        Notes
        -----
        This is recommended for downloading files because its more
        memory efficient.
        """

        if not settings:
            params = {"fileId": self.file_id}
            headers = None
        else:
            params = {"fileId": self.file_id, **settings.parameters}
            headers = settings.headers

        async for chunk in self.context._stream(
            url=self.context._routes.file.download_by_id,
            headers=headers,
            params=params,
        ):
            yield chunk

    async def save(self, settings: DownloadSettings, pathway: str) -> None:
        """Used to save a file to a local pathway.

        Parameters
        ----------
        settings : DownloadSettings
        pathway : str
            Local pathway to save to.

        Notes
        -----
        Saves file in chunks to be more memory efficient.
        """

        async with aiofiles.open(pathway, "wb") as f:
            async for chunk in self.download_iterate(settings):
                await f.write(chunk)
