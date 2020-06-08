import asyncio
import aiob2

import settings

import sys
import re
import requests


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
