from ..base import BaseFile

from ...models.file import FileModel, UploadUrlModel, FileDeleteModel

from ...settings import DownloadSettings

from ...exceptions import AwaitingOnly

from ...utils import UploadUrlCache


class BlockingFile(BaseFile):
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

    def delete(self, name: str) -> FileDeleteModel:
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
            self.context._post(
                url=self.context._routes.file.delete,
                json={"fileName": name, "fileId": self.file_id},
                include_account=False
            )
        )

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

        cache = UploadUrlCache(self.bucket_id, parts=True)

        upload_url = cache.find()
        if upload_url:
            return upload_url

        return cache.save(UploadUrlModel(
            self.context._post(
                url=self.content._routes.upload.upload_part,
                json={
                    "bucketId": self.bucket_id,
                    "fileId": self.file_id
                }
            )
        ))

    def finish_large_file(self, sha1s: list) -> FileModel:
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
            self.context._post(
                url=self.context._routes.file.finish_large,
                json={
                    "fileId": self.file_id,
                    "partSha1Array": sha1s
                },
                include_account=False
            )
        )

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
