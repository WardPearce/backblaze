from aiofile import AIOFile, Reader
from hashlib import sha1
from typing import cast, AsyncGenerator, TYPE_CHECKING, Tuple

from ..base import BasePart

from ...models.file import PartModel, FileModel

from ...settings import CopyPartSettings

from ...utils import UploadUrlCache

from ...decorators import authorize_required

if TYPE_CHECKING:
    from ... import Awaiting
    from .file import AwaitingFile


class AwaitingParts(BasePart):
    _context: "Awaiting"
    _file: "AwaitingFile"

    @authorize_required
    async def list(self, limit: int = 100
                   ) -> AsyncGenerator[Tuple[PartModel, int], None]:
        """Used to list parts.

        Yields
        -------
        PartModel
        int
            Next part number.
        limit : int
            Part limit.
        """

        data = cast(
            dict,
            await self._context._post(
                json={
                    "fileId": self._file.file_id,
                    "startPartNumber":
                    self.part_number if self.part_number > 0 else 1,
                    "maxPartCount": limit
                },
                include_account=False,
                url=self._context._routes.file.list_parts
            )
        )

        for part in data["parts"]:
            yield PartModel(part), data["nextPartNumber"]

    @authorize_required
    async def copy(self, settings: CopyPartSettings) -> PartModel:
        """Used to copy a part.

        Parameters
        ----------
        settings : CopyPartSettings

        Returns
        -------
        PartModel
        """

        return PartModel(await self._context._post(
            url=self._context._routes.file.copy_part,
            json={
                "sourceFileId": self._file.file_id,
                "partNumber":
                self.part_number if self.part_number > 0 else 1,
                **settings.payload
            },
            include_account=False,
        ))

    @authorize_required
    async def data(self, data: bytes) -> PartModel:
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

        upload = await self._file.upload_url()

        sha1_str = sha1(data).hexdigest()
        self.sha1s_append(sha1_str)

        return PartModel(
            await self._context._post(
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

    async def file(self, pathway: str) -> None:
        """Used to upload a file in parts.

        Parameters
        ----------
        pathway : str
            Local file pathway.
        """

        async with AIOFile(pathway, "rb") as afp:
            async for chunk in Reader(afp,
                                      chunk_size=self._context.chunk_size):
                await self.data(chunk)

    @authorize_required
    async def finish(self) -> FileModel:
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
            await self._context._post(
                url=self._context._routes.file.finish_large,
                json={
                    "fileId": self._file.file_id,
                    "partSha1Array": self.sha1s
                },
                include_account=False
            )
        )
