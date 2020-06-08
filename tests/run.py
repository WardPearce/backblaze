import asyncio
import aiob2

import settings

import sys


if aiob2.__version__ != "1.0.0":
    sys.exit("""PLEASE INSTALL THE LATEST VERSION BEFORE TESTING
                `pip3 install aiob2`""")

b2 = aiob2.client()


async def connection_test():
    await b2.connect(
        settings.APP_ID,
        settings.KEY
    )

    await b2.close()

loop = asyncio.get_event_loop()
loop.run_until_complete(connection_test())
