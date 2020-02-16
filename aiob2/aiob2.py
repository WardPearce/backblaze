from upload import B2Upload
from routes import ROUTES

import aiohttp
import aiofiles
import os
import asyncio
import base64

class b2(object):
    """ B2 API Interface. """

    def __init__(self, application_key_id, application_key):
        self.ROUTES = ROUTES

        self.loop = asyncio.get_event_loop()
        self.session = aiohttp.ClientSession(loop=self.loop)
        self.loop.run_until_complete(self.auth(application_key_id, application_key))

        self.upload = B2Upload(obj=self)

    def get_bucket(self, bucket_id):
        return {"bucketId": bucket_id}

    def get_file_id(self, file_id):
        return {"fileId": file_id}

    def part_number(self, number):
        if number > 10000 and number < 1:
            raise Exception("InvalidPartNumber")

    async def read_file(self, file_pathway):
        if os.path.isfile(file_pathway):
            async with aiofiles.open(file_pathway, mode="r") as f:
                contents = await f.read()
                
            return contents

        raise Exception("CantReadFile")

    async def post(self, url, **kwargs):
        async with self.session.post(url, headers=self.authorization, **kwargs) as resp:
            if resp.status == 200:
                return await resp.json()
            else:
                return False

    async def auth(self, application_key_id, application_key):
        """ https://www.backblaze.com/b2/docs/b2_authorize_account.html """

        encoded_bytes = base64.b64encode("{}:{}".format(application_key_id, application_key).encode("utf-8"))
        basic_auth_string = "Basic {}".format(str(encoded_bytes, "utf-8"))

        async with self.session.get(self.ROUTES["authorize"], headers={"Authorization": basic_auth_string}) as resp:
            if resp.status == 200:
                resp_json = await resp.json()

                self.api_url = resp_json["apiUrl"]
                self.download_url = resp_json["downloadUrl"]
                self.account_id = resp_json["accountId"]
                self.authorization = {"Authorization": resp_json["authorizationToken"]}

                return resp_json
            else:
                raise Exception("InvalidAuthorization")

if __name__ == "__main__":
    b2_client = b2(application_key_id="", application_key="")

    async def testing():
        print(await b2_client.upload.get_url(bucket_id="33e138c438fbe35e6be90b11"))

        await b2_client.session.close()
        
    loop = asyncio.get_event_loop()
    loop.run_until_complete(testing())
    loop.close()