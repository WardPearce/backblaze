from typing import TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .. import Awaiting, Blocking

class BaseKey:
    def __init__(self, _context: Union[Awaiting, Blocking],
                 key_id: str) -> None:
        self._context = _context
        self.key_id = key_id
