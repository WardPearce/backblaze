from .bucket.models import BucketModel
from .bucket import Bucket

from .wrapped_requests import AWR
from .routes import ROUTES, DL_ROUTES
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
            yield BucketModel(bucket), Bucket(bucket["bucketId"])

    async def download_from_name(self, bucket_name, file_name):
        """ https://www.backblaze.com/b2/docs/b2_download_file_by_name.html """

        return await AWR(
            DL_ROUTES.file_by_name.format(
                bucket_name, file_name
            )
        ).get()

    async def download_from_name_iterate(self, bucket_name, file_name):
        """ https://www.backblaze.com/b2/docs/b2_download_file_by_name.html """

        request = AWR(
            DL_ROUTES.file_by_name.format(
                bucket_name, file_name
            )
        )

        async for response in request.get_streamed():
            yield response
