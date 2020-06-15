from ..wrapped_requests import AWR
from ..routes import ROUTES

from ..resources import CONFIG

from .models import KeyModel
from ..bucket import Bucket


class Key:
    """ Contains all key related calls.

        Returns
        -------
        Key:
            Object what interacts with keys.
    """

    async def create(self, capabilities, key_name, **kwargs):
        """ Creates a new key.

            Parameters
            ----------
            validDurationInSeconds:
                When provided, the key will expire after the given number of
                seconds, and will have expirationTimestamp set. Value must be
                a positive integer, and must be less than 1000 days.
            bucketId:
                When present, the new key can only access this bucket.
                When set, only these capabilities can be specified:
                    'listBuckets',
                    'listFiles',
                    'readFiles',
                    'shareFiles',
                    'writeFiles',
                    'deleteFiles'
            namePrefix:
                When present, restricts access to files
                whose names start with the prefix.
                You must set bucketId when setting this.

            Returns
            -------
            KeyModel:
                Data model for keys.
            Bucket:
                Object for interacting with buckets.

            References
            ----------
            https://www.backblaze.com/b2/docs/b2_create_key.html
        """

        data = await AWR(
            ROUTES.create_key,
            json={
                "accountId": CONFIG.account_id,
                "capabilities": capabilities,
                "keyName": key_name,
                **kwargs,
            }
        ).post()

        return KeyModel(data), Bucket(data["bucketId"])

    async def delete(self, application_key_id):
        """ Deletes given key.

            Returns
            -------
            KeyModel:
                Data model for keys.
            Bucket:
                Object for interacting with buckets.

            References
            ----------
            https://www.backblaze.com/b2/docs/b2_delete_key.html
        """

        data = await AWR(
            ROUTES.delete_key,
            json={
                "applicationKeyId": application_key_id,
            }
        ).post()

        return KeyModel(data), Bucket(data["bucketId"])
