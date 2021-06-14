import os
import aiofiles

from hashlib import sha1
from typing import Any, AsyncGenerator, Tuple

from ..base import BaseBucket

from ...models.bucket import BucketModel
from ...models.file import FileModel, UploadUrlModel

from .file import AwaitingFile

from ...settings import (
    FileSettings,
    UploadSettings,
    PartSettings,
    BucketUpdateSettings
)

from ...utils import UploadUrlCache

from ...decorators import authorize_required


class AwaitingBucket(BaseBucket):
    @authorize_required
    async def update(self, settings: BucketUpdateSettings) -> BucketModel:
        """Updates bucket details.

        Parameters
        ----------
        settings : BucketUpdateSettings

        Returns
        -------
        BucketModel
        """

        return BucketModel(
            await self.context._post(
                url=self.context._routes.bucket.update,
                json={"bucketId": self.bucket_id, **settings.payload}
            )
        )

    @authorize_required
    async def create_part(self, settings: PartSettings
                          ) -> Tuple[FileModel, AwaitingFile]:
        """Used to create a part.

        Parameters
        ----------
        settings : PartSettings

        Returns
        -------
        FileModel
        AwaitingFile
        """

        data = await self.context._post(
            url=self.context._routes.file.start_large,
            json={"bucketId": self.bucket_id, **settings.payload},
            include_account=False
        )

        return FileModel(data), self.file(data["fileId"])

    @authorize_required
    async def file_versions(self, settings: FileSettings = None
                            ) -> AsyncGenerator[Any, None]:
        """Used to list file by version.

        Parameters
        ----------
        settings : FileSettings, optional
            by default None

        Yields
        -------
        FileModel
            Holds details on file.
        AwaitingFile
        str
            Next file name.
        str
            Next file ID.
        """

        json = {
            "bucketId": self.bucket_id,
        }

        if settings:
            json = {
                **json,
                **settings.payload
            }

        data = await self.context._post(
            url=self.context._routes.file.versions,
            json=json,
            include_account=False
        )

        for file in data["files"]:
            yield (
                FileModel(file),
                self.file(file["fileId"]),
                file["nextFileName"],
                file["nextFileId"]
            )

    @authorize_required
    async def file_names(self, settings: FileSettings = None
                         ) -> AsyncGenerator[Any, None]:
        """Used to list file by name.

        Parameters
        ----------
        settings : FileSettings, optional
            by default None

        Yields
        -------
        FileModel
            Holds details on file.
        AwaitingFile
        str
            Next file name.
        """

        json = {
            "bucketId": self.bucket_id,
        }

        if settings:
            json = {
                **json,
                **settings.payload
            }

        data = await self.context._post(
            url=self.context._routes.file.names,
            json=json,
            include_account=False
        )

        for file in data["files"]:
            yield (
                FileModel(file),
                self.file(file["fileId"]),
                file["nextFileName"]
            )

    async def upload_file(self, settings: UploadSettings, pathway: str,
                          allow_parts: bool = True
                          ) -> Tuple[FileModel, AwaitingFile]:
        """Used to upload a file to the bucket.

        Parameters
        ----------
        settings : UploadSettings
        pathway : str
        allow_parts : bool, optional
            by default True

        Returns
        -------
        FileModel
            Holds details on the uploaded file.
        AwaitingFile
            Used to interact with the file.

        Notes
        -----
        If file size above 5mb file will be uploaded in parts.
        """

        if allow_parts and os.path.getsize(pathway) > 5000000:
            _, file = await self.create_part(PartSettings(
                settings._name,
                settings._content_type
            ))

            parts = file.parts()
            await parts.file(pathway)

            data = await parts.finish()
        else:
            async with aiofiles.open(pathway, "rb") as f:
                data, file = await self.upload(
                    settings, await f.read()
                )

        return data, file

    @authorize_required
    async def upload(self, settings: UploadSettings, data: bytes
                     ) -> Tuple[FileModel, AwaitingFile]:
        """Used to upload a file to b2.

        Parameters
        ----------
        settings : UploadSettings
        data : bytes
            Bytes to upload.

        Returns
        -------
        FileModel
            Holds details on the uploaded file.
        AwaitingFile
            Used to interact with the file.
        """

        upload = await self.upload_url()

        file = FileModel(await self.context._post(
            url=upload.upload_url,
            headers={
                "Content-Length": str(len(data)),
                "X-Bz-Content-Sha1": sha1(data).hexdigest(),
                "Authorization": upload.authorization_token,
                **settings.headers
            },
            data=data,
            include_account=False
        ))

        return file, self.file(file.file_id)

    @authorize_required
    async def upload_url(self) -> UploadUrlModel:
        """Used to get a upload URL.

        Returns
        -------
        UploadUrlModel
            Holds details on the upload URL.

        Notes
        -----
        Caching is used.
        """

        cache = UploadUrlCache(self.bucket_id)

        upload_url = cache.find()
        if upload_url:
            return upload_url

        return cache.save(UploadUrlModel(
            await self.context._post(
                url=self.context._routes.upload.upload,
                json={"bucketId": self.bucket_id},
                include_account=False
            )
        ))

    def file(self, file_id: str) -> AwaitingFile:
        """Used to interact with a file.

        Parameters
        ----------
        file_id : str
            ID of a file.

        Returns
        -------
        AwaitingFile
        """

        return AwaitingFile(file_id, self.context, self.bucket_id)

    @authorize_required
    async def delete(self) -> BucketModel:
        """Used to delete a bucket.

        Returns
        -------
        BucketModel
            Holds details on delete bucked.
        """

        return BucketModel(await self.context._post(
            url=self.context._routes.bucket.delete,
            json={
                "bucketId": self.bucket_id
            }
        ))
