from .upload import B2Upload
from .lists import B2List
from .hide import B2Hide
from .get import B2Get
from .finish import B2Finish
from .download import B2Download
from .delete import B2Delete
from .create import B2Create
from .copy import B2Copy
from .cancel import B2Cancel

from .routes import ROUTES

import aiohttp
import requests
import hashlib
import aiofiles
import os
import asyncio
import base64

class b2(object):
    """ B2 API Interface. """

    def __init__(self, application_key_id, application_key, session=None, debug=False):
        self.ROUTES = ROUTES
        self.debug = debug
        
        self.loop = asyncio.get_event_loop()
        if session == None:
            self.session = aiohttp.ClientSession(loop=self.loop)
        else:
            self.session = session

        self.auth(application_key_id, application_key)

        self.get = B2Get(obj=self)
        self.upload = B2Upload(obj=self)
        self.list = B2List(obj=self)
        self.hide = B2Hide(obj=self)
        self.finish = B2Finish(obj=self)
        self.download = B2Download(obj=self)
        self.delete = B2Delete(obj=self)
        self.create = B2Create(obj=self)
        self.copy = B2Copy(obj=self)
        self.cancel = B2Cancel(obj=self)

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

    async def debugger(self, resp):
        try:
            print(await resp.json())
        except:
            print("Debug couldn't render json.")

    async def _post(self, url, **kwargs):
        async with self.session.post(url, **kwargs) as resp:
            if resp.status == 200:
                return await resp.json()
            else:
                if self.debug == True:
                    await self.debugger(resp)

                return False

    async def _get(self, url, **kwargs):
        async with self.session.get(url, **kwargs) as resp:
            if resp.status == 200:
                return await resp.read()
            else:
                if self.debug == True:
                    await self.debugger(resp)

                return False

    def auth(self, application_key_id, application_key):
        """ https://www.backblaze.com/b2/docs/b2_authorize_account.html """

        encoded_bytes = base64.b64encode("{}:{}".format(application_key_id, application_key).encode("utf-8"))
        basic_auth_string = "Basic {}".format(str(encoded_bytes, "utf-8"))

        resp = requests.get(self.ROUTES["authorize"], headers={"Authorization": basic_auth_string})
        if resp.status_code == 200:
            resp_json = resp.json()

            self.api_url = resp_json["apiUrl"]
            self.download_url = resp_json["downloadUrl"]
            self.account_id = resp_json["accountId"]
            self.authorization = {"Authorization": resp_json["authorizationToken"]}
        else:
            raise Exception("InvalidAuthorization")