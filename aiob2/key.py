from .wrapped_requests import AWR
from .routes import ROUTES

from .resources import CONFIG


class Key:
    def __init__(self, capabilities, key_name):
        self.capabilities = capabilities
        self.key_name = key_name

    async def list(self, **kwargs):
        """ https://www.backblaze.com/b2/docs/b2_list_keys.html """

        return await AWR(
            ROUTES.list_keys,
            json={
                "accountId": CONFIG.account_id,
                **kwargs,
            }
        ).post()

    async def create(self, **kwargs):
        """ https://www.backblaze.com/b2/docs/b2_create_key.html """

        return await AWR(
            ROUTES.create_key,
            json={
                "accountId": CONFIG.account_id,
                "capabilities": self.capabilities,
                "keyName": self.key_name,
                **kwargs,
            }
        ).post()

    async def delete(self, **kwargs):
        """ https://www.backblaze.com/b2/docs/b2_delete_key.html """

        return await AWR(
            ROUTES.delete_key,
            json={
                "accountId": CONFIG.account_id,
                "capabilities": self.capabilities,
                "keyName": self.key_name,
                **kwargs,
            }
        ).post()
