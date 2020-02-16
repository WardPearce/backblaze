import aiohttp
import base64
from routes import ROUTES

class B2Base(object):
    def __init__(self):
        self.api_url = None
        self.download_url = None
        self.account_id = None
        self.authorization = None

    def aiohttp_init(self, session):
        self.session = session

        return self.session

    async def post(self, url, **kwargs):
        async with self.session.post(url, headers=self.authorization, **kwargs) as resp:
            if resp.status == 200:
                return await resp.json()
            else:
                return False

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