import aiohttp
import base64
import json

from routes import ROUTES

class buckets(object):
    async def list_buckets(self):
        return await self.post("{}{}".format(self.api_url, ROUTES["list_buckets"]))

class aiohttp_wrap(object):
    def aiohttp_init(self, session):
        self.session = session

        return self.session

    async def post(self, url):
        async with self.session.post(url, headers=self.authorization, json={"accountId": self.account_id}) as resp:
            if resp.status == 200:
                return await resp.json()
            else:
                return False

class auth(object):
    async def auth(self, application_key_id, application_key):
        encoded_bytes = base64.b64encode("{}:{}".format(application_key_id, application_key).encode("utf-8"))
        basic_auth_string = "Basic {}".format(str(encoded_bytes, "utf-8"))

        async with self.session.get(ROUTES["authorize"], headers={"Authorization": basic_auth_string}) as resp:
            if resp.status == 200:
                resp_json = await resp.json()

                self.api_url = resp_json["apiUrl"]
                self.download_url = resp_json["downloadUrl"]
                self.account_id = resp_json["accountId"]
                self.authorization = {"Authorization": resp_json["authorizationToken"]}

                return resp_json
            else:
                raise Exception("InvalidAuthorization")


class client(buckets, auth, aiohttp_wrap):
    def __init__(self):
        pass

if __name__ == "__main__":
    import asyncio

    b2 = client()

    async def testing():
        aiohttp_session = b2.aiohttp_init(aiohttp.ClientSession(loop=loop))

        await b2.auth(application_key_id="", application_key="")
        
        print(await b2.list_buckets())

        await aiohttp_session.close()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(testing())
    loop.close()