import typing
import aiofiles

from ..base import BaseFile

from ...models.file import FileModel, UploadUrlModel

from ...settings import DownloadSettings

from ...utils import UploadUrlCache


class AwaitingFile(BaseFile):
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

    async def finish_large_file(self, sha1s: list) -> FileModel:
        """Used to complete a large upload.

        Parameters
        ----------
        sha1s : list
            List of sha1s

        Returns
        -------
        FileModel
            Holds details on uploaded file.
        """

        return FileModel(
            await self.context._post(
                url=self.context._routes.file.finish_large,
                json={
                    "fileId": self.file_id,
                    "partSha1Array": sha1s
                },
                include_account=False
            )
        )

    async def download(self, settings: DownloadSettings) -> bytes:
        """Used to download file into memory.

        Parameters
        ----------
        settings : DownloadSettings

        Returns
        -------
        bytes
        """

        return await self.context._get(
            url=self.context._routes.file.download_by_id,
            headers=settings.headers,
            params={"fileId": self.file_id, **settings.parameters},
            resp_json=False,
            include_account=False,
        )

    async def download_iterate(self, settings: DownloadSettings
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

        async for chunk in self.context._stream(
            url=self.context._routes.file.download_by_id,
            headers=settings.headers,
            params={"fileId": self.file_id, **settings.parameters},
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
