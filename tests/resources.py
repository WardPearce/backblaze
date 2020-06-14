import aiob2
from uuid import uuid4

import settings


BUCKET_NAME = "bucket-{}".format(uuid4())
FILENAME_FORMAT = "aiob2/{}"


class ShardVars:
    file_id = None


SHARD_VARS = ShardVars()


B2 = aiob2.client(
    settings.KEY_ID,
    settings.APP_KEY
)
