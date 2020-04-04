from .bucket.bucket import Bucket
from .file.file import File
from .account.account import Account
from .source_file.source_file import SourceFile
from routes import ROUTES

import aiohttp
import requests
import hashlib
import aiofiles
import os
import asyncio
import base64

class client(object):
    """ B2 API Interface. """

    def __init__(self, application_key_id, application_key, session=None, debug=False):
        self.ROUTES = ROUTES
        self.debug = debug
        
        if session:
            self.session = session
        else:
            self.session = aiohttp.ClientSession(loop=asyncio.get_event_loop())

        self.auth(application_key_id, application_key)

    def bucket(self, bucket_id):
        """ Bucket Object.
                - bucket_id, required.
        """

        return Bucket(bucket_id=bucket_id, obj=self)

    def source_file(self, source_file_id):
        """ Source File Object
                - source_file_id, required.
        """

        return SourceFile(source_file_id=source_file_id, obj=self)

    def file(self, file_id):
        """ File Object.
                - file_id, required.
        """

        return File(file_id=file_id, obj=self)

    def account(self, account_id):
        """ Account Object 
                - account_id, required.
        """

        return Account(account_id=account_id, obj=self)

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
            print("Couldn't phrase json.")

    async def _post(self, **kwargs):
        if not kwargs.get("headers"):
            kwargs["headers"] = self.authorization

        async with self.session.post(**kwargs) as resp:
            if resp.status == 200:
                return await resp.json()
            else:
                if self.debug:
                    await self.debugger(resp)

                return False

    async def _get(self, **kwargs):
        if not kwargs.get("headers"):
            kwargs["headers"] = self.authorization

        async with self.session.get(**kwargs) as resp:
            if resp.status == 200:
                return await resp.read()
            else:
                if self.debug:
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