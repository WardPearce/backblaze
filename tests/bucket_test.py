import asyncio
import aiob2
import aiohttp

from uuid import uuid4

import settings

import sys
import re
import requests
import os


def get_latest_version(location):
    url = "https://raw.githubusercontent.com/" + location

    with requests.get(url) as resp:
        if resp.status_code == 200:
            return re.search(
                "__version__ = ['\"]([^'\"]+)['\"]", resp.text
            ).group(1)
        else:
            sys.exit("Request to {} failed with status code {}".format(
                url, resp.status_code
            ))


if aiob2.__version__ != get_latest_version(
    "WardPearce/aiob2/master/aiob2/__init__.py"
        ):
    sys.exit("""PLEASE INSTALL THE LATEST VERSION BEFORE TESTING
                `pip3 install aiob2`""")

b2 = aiob2.client()


async def test_save(bucket_obj):
    for counter in range(0, 4):
        file_name = "aiob2/test{}.bin".format(counter)

        print("Saving {} into {}".format(
            file_name,
            bucket_obj.bucket_id
        ))

        await bucket_obj.upload.data(
            data=b"0",
            file_name=file_name
        )

        print("Saved {}".format(file_name))

        await asyncio.sleep(0.001)


async def bucket_test():
    try:
        await b2.connect(
            settings.KEY_ID,
            settings.APP_KEY,
            aiohttp.ClientSession()
        )
    except aiob2.exceptions.InvalidAuthorization:
        print("Check settings.py, your account details are wrong.")

    try:
        bucket_ids = []
        buckets_append = bucket_ids.append
        async for bucket in b2.bucket().list():
            buckets_append(
                bucket.bucket_id
            )

        print("Current bucket IDs:\n {}".format(bucket_ids))

    except Exception as e:
        print(e)
    else:
        bucket_name = "bucket-{}".format(uuid4())

        print("Creating {}".format(bucket_name))

        bucket = await b2.bucket().create(
            bucket_name,
            aiob2.bucket.models.BucketTypes.private
        )

        print("Created {}".format(bucket_name))

        bucket = b2.bucket(bucket.bucket_id)

        await test_save(bucket)

        pathway = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            "test_image.png"
        )
        if os.path.exists(pathway):
            print("Attempting to upload {}".format(pathway))

            await bucket.upload.file(
                "aiob2/foobar.png",
                pathway
            )

            print("Uploaded {}".format(pathway))

        print("Hiding test_image.png")

        await bucket.file.hide("test_image.png")

        print("test_image.png is hidden")

        print("Deleting {}".format(bucket.bucket_id))

        await bucket.delete()

        print("Deleted {}".format(bucket.bucket_id))

    await b2.close()

loop = asyncio.get_event_loop()
loop.run_until_complete(bucket_test())

print("Test completed.")
