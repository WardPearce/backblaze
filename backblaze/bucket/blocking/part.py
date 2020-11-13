from hashlib import sha1
from typing import Generator

from ..base import BasePart

from ...models.file import PartModel, FileModel

from ...settings import CopyPartSettings

from ...utils import UploadUrlCache

from ...decorators import authorize_required


class BlockingParts(BasePart):
    @authorize_required
    def list(self, limit: int = 100) -> Generator[PartModel, int, None]:
        """Used to list parts.

        Yields
        -------
        PartModel
        int
            Next part number.
        limit : int
            Part limit.
        """

        data = self.context._post(
            json={
                "fileId": self._file.file_id,
                "startPartNumber":
                self.part_number if self.part_number > 0 else 1,
                "maxPartCount": limit
            },
            include_account=False,
            url=self.context._routes.file.list_parts
        )

        for part in data["parts"]:
            yield PartModel(part), data["nextPartNumber"]

    @authorize_required
    def copy(self, settings: CopyPartSettings) -> PartModel:
        """Used to copy a part.

        Parameters
        ----------
        settings : CopyPartSettings

        Returns
        -------
        PartModel
        """

        return PartModel(self.context._post(
            url=self.context._routes.file.copy_part,
            json={
                "sourceFileId": self._file.file_id,
                "partNumber":
                self.part_number if self.part_number > 0 else 1,
                **settings.payload
            },
            include_account=False,
        ))

    @authorize_required
    def data(self, data: bytes) -> PartModel:
        """Uploads a part.

        Parameters
        ----------
        data : bytes

        Returns
        -------
        PartModel
            Holds details on upload part.
        """

        self.part_number += 1

        upload = self._file.upload_url()

        sha1_str = sha1(data).hexdigest()
        self.sha1s_append(sha1_str)

        return PartModel(
            self.context._post(
                headers={
                    "Content-Length": str(len(data)),
                    "X-Bz-Part-Number": str(self.part_number),
                    "X-Bz-Content-Sha1": sha1_str,
                    "Authorization": upload.authorization_token
                },
                include_account=False,
                url=upload.upload_url,
                data=data
            )
        )

    def file(self, pathway: str) -> None:
        """Used to upload a file in parts.

        Parameters
        ----------
        pathway : str
            Local file pathway.
        """

        with open(pathway, "rb") as fp:
            chunk = True

            while chunk:
                chunk = fp.read(self.context.chunk_size)
                if chunk:
                    self.data(chunk)

    @authorize_required
    def finish(self) -> FileModel:
        """Used to complete a part upload.

        Returns
        -------
        FileModel
            Holds details on uploaded file.
        """

        UploadUrlCache(
            self._file.bucket_id,
            self._file.file_id
        ).delete()

        return FileModel(
            self.context._post(
                url=self.context._routes.file.finish_large,
                json={
                    "fileId": self._file.file_id,
                    "partSha1Array": self.sha1s
                },
                include_account=False
            )
        )
