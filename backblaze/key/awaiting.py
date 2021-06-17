from typing import TYPE_CHECKING, cast

from .base import BaseKey
from ..models.key import KeyModel
from ..decorators import authorize_required

if TYPE_CHECKING:
    from .. import Awaiting


class AwaitingKey(BaseKey):
    _context: "Awaiting"

    @authorize_required
    async def delete(self) -> KeyModel:
        """Used delete key.

        Returns
        -------
        KeyModel
            Details on delete key.
        """

        return KeyModel(
            cast(
                dict,
                await self._context._post(
                    url=self._context._routes.key.delete,
                    json={"applicationKeyId": self.key_id},
                    include_account=False
                )
            )
        )
