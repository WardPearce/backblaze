from typing import Any

from ..base import BaseFile

from .part import BlockingParts

from ...models.file import (
    FileModel,
    UploadUrlModel,
    FileDeleteModel,
    PartCancelModel
)

from ...settings import DownloadSettings, CopyFileSettings

from ...exceptions import AwaitingOnly

from ...utils import UploadUrlCache

from ...decorators import authorize_required


class BlockingFile(BaseFile):
    def parts(self, part_number: int = 0) -> BlockingParts:
        """Used to upload a parts.

        Parameters
        ----------
        part_number : int, optional
            by default 0

        Returns
        -------
        BlockingParts
        """

        return BlockingParts(
            self,
            self.context,
            part_number
        )

    @authorize_required
    def copy(self, settings: CopyFileSettings) -> Any:
        """Used copy a file.

        Parameters
        ----------
        settings : CopyFileSettings

        Returns
        -------
        FileModel
        BlockingFile
        """

        data = self.context._post(
            url=self.context._routes.file.copy,
            json={"sourceFileId": self.file_id, **settings.payload},
            include_account=False
        )

        return FileModel(data), BlockingFile(
            data["fileId"], self.context, self.bucket_id)

    @authorize_required
    def cancel(self) -> PartCancelModel:
        """Used for cancelling a uncompleted file.

        Returns
        -------
        PartCancelModel
            Holds details on canceled file.
        """

        UploadUrlCache(self.bucket_id, self.file_id).delete()

        return PartCancelModel(
            self.context._post(
                url=self.context._routes.file.cancel_large,
                json={"fileId": self.file_id},
                include_account=False
            )
        )

    @authorize_required
    def get(self) -> FileModel:
        """Used to get details on a file.

        Returns
        -------
        FileModel
            Holds details on a file
        """

        return FileModel(
            self.context._post(
                url=self.context._routes.file.get,
                json={"fileId": self.file_id},
                include_account=False
            )
        )

    @authorize_required
    def delete(self, name: str = None) -> FileDeleteModel:
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
            name = (self.get()).file_name

        return FileDeleteModel(
            self.context._post(
                url=self.context._routes.file.delete,
                json={"fileName": name, "fileId": self.file_id},
                include_account=False
            )
        )

    @authorize_required
    def upload_url(self) -> UploadUrlModel:
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
            self.context._post(
                url=self.context._routes.upload.upload_part,
                json={
                    "fileId": self.file_id
                },
                include_account=False
            )
        ))

    @authorize_required
    def download(self, settings: DownloadSettings = None) -> bytes:
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

        return self.context._get(
            url=self.context._routes.file.download_by_id,
            headers=headers,
            params=params,
            resp_json=False,
            include_account=False,
        )

    def download_iterate(self) -> None:
        """This doesn't work, only here for a identical API.

        Raises
        ------
        AwaitingOnly
            Raised when a coroutine called is awaiting supported only.
        """

        raise AwaitingOnly()

    def save(self, settings: DownloadSettings, pathway: str) -> None:
        """Used to save a file to a local pathway.

        Parameters
        ----------
        settings : DownloadSettings
        pathway : str
            Local pathway to save to.
        """

        with open(pathway, "wb") as f:
            f.write(self.download(settings))
