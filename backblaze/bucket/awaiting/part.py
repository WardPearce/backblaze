import aiofiles

from hashlib import sha1
from typing import AsyncGenerator

from ..base import BasePart

from ...models.file import PartModel, FileModel


class AwaitingParts(BasePart):
    async def list(self, limit: int = 100) -> AsyncGenerator[PartModel, int]:
        """Used to list parts.

        Yields
        -------
        PartModel
        int
            Next part number.
        limit : int
            Part limit.
        """

        data = await self.context._post(
            json={
                "fileId": self.file.file_id,
                "startPartNumber":
                self.part_number if self.part_number > 0 else 1,
                "maxPartCount": limit
            },
            include_account=False,
            url=self.context._routes.file.list_parts
        )

        for part in data["parts"]:
            yield PartModel(part), data["nextPartNumber"]

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

        upload = await self.file.upload_url()

        sha1_str = sha1(data).hexdigest()
        self.sha1s.append(sha1_str)

        return PartModel(
            await self.context._post(
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

        async with aiofiles.open(pathway, "rb") as file:
            chunk = b""

            while chunk:
                chunk = await file.read(self.context.chunk_size)
                if chunk:
                    await self.data(chunk)

    async def finish(self) -> FileModel:
        """Used to complete a part upload.

        Returns
        -------
        FileModel
            Holds details on uploaded file.
        """

        return FileModel(
            await self.context._post(
                url=self.context._routes.file.finish_large,
                json={
                    "fileId": self.file.file_id,
                    "partSha1Array": self.sha1s
                },
                include_account=False
            )
        )
