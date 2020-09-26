from .base import BaseKey

from ..models.key import KeyModel


class BlockingKey(BaseKey):
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
