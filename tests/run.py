import asyncio
import aiohttp
import aiob2

from resources import B2

from bucket import BucketTest
from file import FileTest


async def start_test():
    try:
        await B2.connect(
            aiohttp.ClientSession()
        )
    except aiob2.exceptions.InvalidAuthorization:
        print("Check settings.py, your account details are wrong.")
    else:
        # Runs bucket test.
        bucket_test = BucketTest()
        await bucket_test.run()

        file_test = FileTest()
        await file_test.run()

        await bucket_test.delete()

    await B2.close()

loop = asyncio.get_event_loop()
loop.run_until_complete(start_test())

print("Test completed.")
