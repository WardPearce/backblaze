from .bucket.models import BucketModel
from .bucket import Bucket

from .wrapped_requests import AWR
from .routes import ROUTES
from .resources import CONFIG


class Misc:
    async def buckets(self, **kwargs):
        """ https://www.backblaze.com/b2/docs/b2_list_buckets.html """

        data = await AWR(
            ROUTES.list_buckets,
            json={
                "accountId": CONFIG.account_id,
                **kwargs,
            }
        ).post()

        for bucket in data["buckets"]:
            yield Bucket(bucket["bucketId"]), BucketModel(bucket)
