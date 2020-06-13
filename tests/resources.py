import aiob2
from uuid import uuid4


BUCKET_NAME = "bucket-{}".format(uuid4())
B2 = aiob2.client()
