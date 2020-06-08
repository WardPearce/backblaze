from .wrapped_requests import AWR
from .routes import ROUTES


class Create:
    def __init__(self, account_id):
        self.account_id = account_id

    async def key(self, capabilities, key_name, **kwargs):
        """ https://www.backblaze.com/b2/docs/b2_create_key.html """

        return await AWR(
            ROUTES.create_key,
            json={
                "accountId": self.account_id,
                "capabilities": capabilities,
                "keyName": key_name, **kwargs,
            }
        ).post()

    async def bucket(self, bucket_name, bucket_type, **kwargs):
        """ https://www.backblaze.com/b2/docs/b2_create_bucket.html """

        return await AWR(
            ROUTES.create_bucket,
            json={
                "accountId": self.account_id,
                "bucketName": bucket_name,
                "bucketType": bucket_type,
                **kwargs,
            }
        ).post()
