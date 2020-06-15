from .upload import Upload
from .files import Files
from .models import BucketModel, BucketTypes

from ..wrapped_requests import AWR
from ..routes import ROUTES
from ..resources import CONFIG


class Bucket:
    def __init__(self, bucket_id):
        self.bucket_id = bucket_id

    async def create(self, name, type: BucketTypes, **kwargs):
        """ Creates a bucket.

            Parameters
            ----------
            name: str
                Unique name of bucket.
            type:
                BucketTypes object.
            bucketInfo:
                User-defined information to be stored with the bucket:
                a dictionary mapping names to values. See Buckets.
                Cache-Control policies can be set here on a global
                level for all the files in the bucket.
            corsRules:
                The initial list (a dictionary) of CORS rules for this bucket.
                See CORS Rules for an overview and the rule structure.
            lifecycleRules:
                The initial list (a dictionary) of lifecycle
                rules for this bucket.
                Structure defined below. See Lifecycle Rules.

            Returns
            -------
            BucketModel:
                Bucket data model.

            Notes
            -----
            When a bucket is created it sets the current initialized
            Bucket object's bucket_id to the created bucket's ID.

            References
            ----------
            https://www.backblaze.com/b2/docs/b2_create_bucket.html
        """

        data = await AWR(
            ROUTES.create_bucket,
            json={
                "accountId": CONFIG.account_id,
                "bucketName": name,
                "bucketType": type,
                **kwargs,
            }
        ).post()

        self.bucket_id = data["bucketId"]

        return BucketModel(data)

    @property
    def upload(self):
        """ Contains all bucket uploading calls.

            Returns
            -------
            Upload:
                Object what can upload data.
        """

        return Upload(bucket_id=self.bucket_id)

    @property
    def files(self):
        """ Contains all file calls.

            Returns
            -------
            Files:
                Object for interacting with files.
        """

        return Files(bucket_id=self.bucket_id)

    async def delete(self):
        """ Deletes the current bucket..

            Returns
            -------
            BucketModel:
                Bucket data model.

            References
            ----------
            https://www.backblaze.com/b2/docs/b2_delete_bucket.html
        """

        data = await AWR(
            ROUTES.delete_bucket,
            json={
                "accountId": CONFIG.account_id,
                "bucketId": self.bucket_id,
            },
        ).post()

        return BucketModel(data)
