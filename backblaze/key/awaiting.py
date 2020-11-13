from .base import BaseKey

from ..models.key import KeyModel

from ..decorators import authorize_required


class AwaitingKey(BaseKey):
    @authorize_required
    async def delete(self) -> KeyModel:
        """Used delete key.

        Returns
        -------
        KeyModel
            Details on delete key.
        """

        return KeyModel(
            await self.context._post(
                url=self.context._routes.key.delete,
                json={"applicationKeyId": self.key_id},
                include_account=False
            )
        )
