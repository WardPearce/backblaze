from .wrapped_requests import AWR
from .routes import ROUTES


class List:
    def __init__(self, account_id):
        self.account_id = account_id

    async def keys(self, **kwargs):
        """ https://www.backblaze.com/b2/docs/b2_list_keys.html """

        return await AWR(
            ROUTES.list_keys,
            json={
                "accountId": self.account_id,
                **kwargs,
            }
        ).post()

    async def buckets(self, **kwargs):
        """ https://www.backblaze.com/b2/docs/b2_list_buckets.html """

        return await AWR(
            ROUTES.list_buckets,
            json={
                "accountId": self.account_id,
                **kwargs,
            }
        ).post()
