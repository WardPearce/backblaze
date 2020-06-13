from .bucket import Bucket
from .file import File
from .source_file import SourceFile
from .key import Key
from .misc import Misc

from .resources import SESSIONS, CONFIG

from .routes import ROUTES, DL_ROUTES

from .exceptions import InvalidAuthorization

import base64
import aiohttp

__version__ = "1.0.0"


class client(Misc):
    """ B2 API Interface. """

    AUTH_URL = "https://api.backblazeb2.com/b2api/v2/b2_authorize_account"

    def __init__(self, key_id, application_key,  max_cache=100):
        """ max_cache, how many cached upload urls do we allow. """

        self.key_id = key_id
        self.application_key = application_key

        CONFIG.max_cache = max_cache

    async def connect(self, session: aiohttp.ClientSession = None):
        """ Gets authorization details to send requests.
            https://www.backblaze.com/b2/docs/b2_authorize_account.html
        """

        if session:
            SESSIONS.AIOHTTP = session
        else:
            SESSIONS.AIOHTTP = aiohttp.ClientSession()

        encoded_bytes = base64.b64encode(
            "{}:{}".format(
                self.key_id,
                self.application_key
            ).encode("utf-8")
        )
        basic_auth_string = "Basic {}".format(str(encoded_bytes, "utf-8"))

        async with SESSIONS.AIOHTTP.get(
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

                ROUTES.format_routes()
                DL_ROUTES.format_routes()
            else:
                raise InvalidAuthorization()

    async def close(self):
        """ Closes sessions """

        await SESSIONS.AIOHTTP.close()

    def key(self, capabilities=None, key_name=None, **kwargs):
        """ Key Object
                - capabilities, optional.
                - key_name, optional.

        """

        return Key(
            capabilities=capabilities,
            key_name=key_name,
            **kwargs
        )

    def bucket(self, bucket_id=None):
        """ Bucket Object
                - bucket_id, optional.
        """

        return Bucket(bucket_id=bucket_id)

    def source_file(self, source_file_id):
        """ Source File Object
                - source_file_id, required.
        """

        return SourceFile(source_file_id=source_file_id)

    def file(self, file_id):
        """ File Object.
                - file_id, required.
        """

        return File(file_id=file_id)
