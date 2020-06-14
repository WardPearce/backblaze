##### Version 1.0.0 is NOT backwards compatibility with anything below that version.

# About
aiob2 is a powerful & simple asynchronous wrapper for Backblaze's b2 API.

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