from typing import TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .awaiting.file import AwaitingFile
    from .blocking.file import BlockingFile

    from .. import Awaiting, Blocking


class BaseBucket:
    def __init__(self, _context: Union["Awaiting", "Blocking"],
                 bucket_id: str) -> None:
        self._context = _context
        self.bucket_id = bucket_id


class BaseFile(BaseBucket):
    def __init__(self, file_id: str, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.file_id = file_id


class BasePart:
    def __init__(self,
                 file: Union["AwaitingFile", "BlockingFile"],
                 _context: Union["Awaiting", "Blocking"],
                 part_number: int = 0) -> None:

        self._file = file
        self._context = _context
        self.part_number = part_number
        self.sha1s = []
        self.sha1s_append = self.sha1s.append
