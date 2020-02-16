from upload import B2Upload
from routes import ROUTES

import aiohttp
import hashlib
import aiofiles
import os
import asyncio
import base64

class b2(object):
    """ B2 API Interface. """

    def __init__(self, application_key_id, application_key, debug=False):
        self.ROUTES = ROUTES
        self.debug = debug
        
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
    
    def get_sha1(self, data):
        return hashlib.sha1(data).hexdigest()

    async def read_file(self, file_pathway):
        if os.path.isfile(file_pathway):
            sha1 = hashlib.sha1()

            contents = {
                "data": b"",
                "bytes":str(os.path.getsize(file_pathway)),
            }

            async with aiofiles.open(file_pathway, mode="rb") as f:
                async for line in f:
                    sha1.update(line)
                    contents["data"] += line

            contents["sha1"] = sha1.hexdigest()
            
            return contents

        raise Exception("CantReadFile")

    async def post(self, url, **kwargs):
        async with self.session.post(url, **kwargs) as resp:
            if resp.status == 200:
                return await resp.json()
            else:
                if self.debug == True:
                    print(await resp.json())
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
            else:
                raise Exception("InvalidAuthorization")

if __name__ == "__main__":
    b2_client = b2(application_key_id="", application_key="", debug=True)

    async def testing():
        CURRECT_DIR = os.path.dirname(os.path.realpath(__file__))

        print(await b2_client.upload.file(bucket_id="33e138c438fbe35e6be90b11", file_name="test.json", file_pathway="{}/test.json".format(CURRECT_DIR)))

        await b2_client.session.close()
        
    loop = asyncio.get_event_loop()
    loop.run_until_complete(testing())
    loop.close()