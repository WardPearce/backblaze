import asyncio
import aiohttp
import aiob2

from resources import B2

from bucket import BucketTest


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
        await bucket_test.delete()

    await B2.close()

loop = asyncio.get_event_loop()
loop.run_until_complete(start_test())

print("Test completed.")
