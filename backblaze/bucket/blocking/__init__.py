import typing

from hashlib import sha1

from ..base import BaseBucket

from ...models.bucket import BucketModel
from ...models.file import FileModel, UploadUrlModel

from .file import BlockingFile

from ...settings import FileSettings, UploadSettings, PartSettings

from ...utils import UploadUrlCache


class BlockingBucket(BaseBucket):
    def create_part(self, settings: PartSettings
                    ) -> typing.Tuple[FileModel, BlockingFile]:
        """Used to create a part.

        Parameters
        ----------
        settings : PartSettings

        Returns
        -------
        FileModel
        BlockingFile
        """

        data = self.context._post(
            url=self.context._routes.file.start_large,
            json={"bucketId": self.bucket_id, **settings.payload},
            include_account=False
        )

        return FileModel(data), self.file(data["fileId"])

    def file_versions(self, settings: FileSettings = None
                      ) -> typing.Generator[typing.Any, None, None]:
        """Used to list file by version.

        Parameters
        ----------
        settings : FileSettings, optional
            by default None

        Yields
        -------
        FileModel
            Holds details on file.
        BlockingFile
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

        data = self.context._post(
            url=self.context._routes.file.versions,
            json=json,
            include_account=False
        )

        for file in data["files"]:
            yield FileModel(file), self.file(file["fileId"]), \
                file["nextFileName"], file["nextFileId"]

    def file_names(self, settings: FileSettings = None
                   ) -> typing.Generator[typing.Any, None, None]:
        """Used to list file by name.

        Parameters
        ----------
        settings : FileSettings, optional
            by default None

        Yields
        -------
        FileModel
            Holds details on file.
        BlockingFile
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

        data = self.context._post(
            url=self.context._routes.file.names,
            json=json,
            include_account=False
        )

        for file in data["files"]:
            yield FileModel(file), self.file(file["fileId"]), \
                file["nextFileName"]

    def upload(self, settings: UploadSettings, data: bytes
               ) -> typing.Tuple[FileModel, BlockingFile]:
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
        BlockingFile
            Used to interact with the file.
        """

        upload = self.upload_url()

        file = FileModel(self.context._post(
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

    def upload_url(self) -> UploadUrlModel:
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
            self.context._post(
                url=self.context._routes.upload.upload,
                json={"bucketId": self.bucket_id},
                include_account=False
            )
        ))

    def file(self, file_id: str) -> BlockingFile:
        """Used to interact with a file.

        Parameters
        ----------
        file_id : str
            ID of a file.

        Returns
        -------
        BlockingFile
        """

        return BlockingFile(file_id, self.context, self.bucket_id)

    def delete(self) -> BucketModel:
        """Used to delete a bucket.

        Returns
        -------
        BucketModel
            Holds details on delete bucked.
        """

        return BucketModel(self.context._post(
            url=self.context._routes.bucket.delete,
            json={
                "bucketId": self.bucket_id
            }
        ))
