from .bucket import Bucket
from .file import File
from .account import Account
from .source_file import SourceFile

from .resources import AIOHTTP, CONFIG

from .exceptions import InvalidAuthorization

import base64

__version__ = "1.0.0"


class client:
    """ B2 API Interface. """

    AUTH_URL = "https://api.backblazeb2.com/b2api/v2/b2_authorize_account"

    async def connect(self, application_key_id, application_key):
        """ Gets authorization details to send requests.
            https://www.backblaze.com/b2/docs/b2_authorize_account.html
        """

        encoded_bytes = base64.b64encode(
            "{}:{}".format(application_key_id, application_key).encode("utf-8")
        )
        basic_auth_string = "Basic {}".format(str(encoded_bytes, "utf-8"))

        async with AIOHTTP.get(
                self.AUTH_URL,
                headers={"Authorization": basic_auth_string}) as resp:
            if resp.status == 200:
                resp_json = await resp.json()

                CONFIG.api_url = resp_json["apiUrl"]
                CONFIG.download_url = resp_json["downloadUrl"]
                CONFIG.account_id = resp_json["accountId"]
                CONFIG.authorization = {
                    "Authorization": resp_json["authorizationToken"]
                }
            else:
                raise InvalidAuthorization()

    def source_file(self, source_file_id):
        """ Source File Object
                - source_file_id, required.
        """

        return SourceFile(source_file_id=source_file_id, obj=self)

    def file(self, file_id=None):
        """ File Object.
                - file_id, required.
        """

        return File(file_id=file_id, obj=self)

    @property
    def account(self):
        """ Account Object """

        return Account(obj=self)
