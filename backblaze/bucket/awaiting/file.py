import aiofiles

from typing import Any, AsyncGenerator

from ..base import BaseFile

from .part import AwaitingParts

from ...models.file import (
    FileModel,
    UploadUrlModel,
    FileDeleteModel,
    PartCancelModel
)

from ...settings import DownloadSettings, CopyFileSettings

from ...utils import UploadUrlCache

from ...decorators import authorize_required


class AwaitingFile(BaseFile):
    def parts(self, part_number: int = 0) -> AwaitingParts:
        """Used to upload a parts.

        Parameters
        ----------
        part_number : int, optional
            by default 0

        Returns
        -------
        AwaitingParts
        """

        return AwaitingParts(
            self,
            self.context,
            part_number
        )

    @authorize_required
    async def copy(self, settings: CopyFileSettings) -> Any:
        """Used copy a file.

        Parameters
        ----------
        settings : CopyFileSettings

        Returns
        -------
        FileModel
        AwaitingFile
        """

        data = await self.context._post(
            url=self.context._routes.file.copy,
            json={"sourceFileId": self.file_id, **settings.payload},
            include_account=False
        )

        return FileModel(data), AwaitingFile(
            data["fileId"], self.context, self.bucket_id)

    @authorize_required
    async def cancel(self) -> PartCancelModel:
        """Used for cancelling a uncompleted file.

        Returns
        -------
        PartCancelModel
            Holds details on canceled file.
        """

        UploadUrlCache(self.bucket_id, self.file_id).delete()

        return PartCancelModel(
            await self.context._post(
                url=self.context._routes.file.cancel_large,
                json={"fileId": self.file_id},
                include_account=False
            )
        )

    @authorize_required
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

    @authorize_required
    async def delete(self, name: str = None) -> FileDeleteModel:
        """Deletes give file.

        Parameters
        ----------
        name : str, optional
            Name of file, if not given calls self.get,
            by default None.

        Returns
        -------
        FileDeleteModel
            Holds details on delete file.
        """

        if not name:
            name = (await self.get()).file_name

        return FileDeleteModel(
            await self.context._post(
                url=self.context._routes.file.delete,
                json={"fileName": name, "fileId": self.file_id},
                include_account=False
            )
        )

    @authorize_required
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

        cache = UploadUrlCache(self.bucket_id, self.file_id)

        upload_url = cache.find()
        if upload_url:
            return upload_url

        return cache.save(UploadUrlModel(
            await self.context._post(
                url=self.context._routes.upload.upload_part,
                json={
                    "fileId": self.file_id
                },
                include_account=False
            )
        ))

    @authorize_required
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

    @authorize_required
    async def download_iterate(self, settings: DownloadSettings = None
                               ) -> AsyncGenerator[bytes, None]:
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
