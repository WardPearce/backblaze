import asyncio
import aiob2

import settings

import sys
import os
import re


def get_version(package):
    with open(os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "../",
        package,
        "__init__.py"
    )) as f:
        return re.search(
            "__version__ = ['\"]([^'\"]+)['\"]", f.read()
        ).group(1)


if aiob2.__version__ != get_version("aiob2"):
    sys.exit("""PLEASE INSTALL THE LATEST VERSION BEFORE TESTING
                `pip3 install aiob2`""")

b2 = aiob2.client()


async def connection_test():
    try:
        await b2.connect(
            settings.APP_ID,
            settings.KEY
        )
    except aiob2.exceptions.InvalidAuthorization:
        print("Check settings.py, your account details are wrong.")

    await b2.close()

loop = asyncio.get_event_loop()
loop.run_until_complete(connection_test())
