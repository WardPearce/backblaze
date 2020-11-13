from .base import BaseKey

from ..models.key import KeyModel

from ..decorators import authorize_required


class BlockingKey(BaseKey):
    @authorize_required
    def delete(self) -> KeyModel:
        """Used delete key.

        Returns
        -------
        KeyModel
            Details on delete key.
        """

        return KeyModel(
            self.context._post(
                url=self.context._routes.key.delete,
                json={"applicationKeyId": self.key_id},
                include_account=False
            )
        )
