[![GitHub issues](https://img.shields.io/github/issues/WardPearce/aiob2)](https://github.com/WardPearce/aiob2/issues)
[![GitHub license](https://img.shields.io/github/license/WardPearce/aiob2)](https://github.com/WardPearce/aiob2/blob/master/LICENSE)
[![Actions Status](https://github.com/WardPearce/aiob2/workflows/Python%20application/badge.svg)](https://github.com/WardPearce/aiob2/actions)

# About
``aiob2`` is a powerful & simple asynchronous wrapper for Backblaze's b2 API. Version 1.0.0 is considered a rewrite and as a result everything below that version is incompatible. 

# Install 
- Pypi: ``pip3 install aiob2``
- Git: ``pip3 install git+https://github.com/WardPearce/aiob2.git``

# Documentation
Currently under-construction.

Hosted on [readthedocs](https://aiob2.readthedocs.io/en/latest/).

# Example
```python
import aiob2
import asyncio
import aiohttp

from uuid import uuid4


B2 = aiob2.client(key_id="...", application_key="...")


async def example():
    try:
        await B2.connect(
            aiohttp.ClientSession()
        )
    except aiob2.exceptions.InvalidAuthorization:
        print("Invalid account details.")
    else:
        bucket = B2.bucket()

        await bucket.create(
            "bucket-{}".format(uuid4()),
            aiob2.bucket.models.BucketTypes.private
        )

        await bucket.delete()

    await B2.close()

loop = asyncio.get_event_loop()
loop.run_until_complete(example())
```