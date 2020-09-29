from hashlib import sha1

from ..base import BasePart

from ...models.file import PartModel, FileModel

from ...utils import read_in_chunks


class BlockingPart(BasePart):
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

        upload = self.file.upload_url()

        sha1_str = sha1(data).hexdigest()
        self.sha1s.append(sha1_str)

        return PartModel(
            self.context._post(
                headers={
                    "Content-Length": str(len(data)),
                    "X-Bz-Part-Number": str(self.part_number),
                    "X-Bz-Content-Sha1": sha1_str,
                    "Authorization": upload.authorization_token
                },
                include_account=False,
                url=upload.upload_url
            )
        )

    def file(self, pathway: str) -> None:
        """Used to upload a file in parts.

        Parameters
        ----------
        pathway : str
            Local file pathway.
        """

        with open(pathway, "rb") as file:
            for chunk in read_in_chunks(file):
                self.data(chunk)

    def finish(self) -> FileModel:
        """Used to complete a part upload.

        Returns
        -------
        FileModel
            Holds details on uploaded file.
        """

        return FileModel(
            self.context._post(
                url=self.context._routes.file.finish_large,
                json={
                    "fileId": self.file.file_id,
                    "partSha1Array": self.sha1s
                },
                include_account=False
            )
        )
