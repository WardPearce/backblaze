from utils import B2Base
from upload import B2Upload

class b2(B2Base):
    """ B2 API Interface. """

    def __init__(self):
        B2Base.__init__(self)

        self.upload = B2Upload()

if __name__ == "__main__":
    import asyncio
    import aiohttp

    b2_client = b2()

    async def testing():
        aiohttp_session = b2_client.aiohttp_init(aiohttp.ClientSession(loop=loop))

        await b2_client.auth(application_key_id="", application_key="")

        await b2_client.upload.part()

        await aiohttp_session.close()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(testing())
    loop.close()