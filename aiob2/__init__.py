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

__version__ = "1.0.1"


class client(Misc):
    """ B2 API Interface.

        Parameters
        ----------
        key_id: str
            API Key ID
        application_key: str
            API App Key
        max_cache: int
            Max amount of upload urls allowed to be cached
            at a given time.
        chunk_size: int
            How many chunks should we read each loop.
    """

    AUTH_URL = "https://api.backblazeb2.com/b2api/v2/b2_authorize_account"

    key = Key()

    def __init__(self, key_id, application_key,  max_cache=100, chunk_size=25):
        self.key_id = key_id
        self.application_key = application_key

        CONFIG.chunk_size = chunk_size
        CONFIG.max_cache = max_cache

    async def connect(self, session: aiohttp.ClientSession = None):
        """ Gets authorization details needed to send requests.

            Parameters
            ----------
            session: object

            Raises
            ------
            InvalidAuthorization
                Bad account details were passed.

            References
            ----------
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
        """ Closes all sessions.
        """

        await SESSIONS.AIOHTTP.close()

    def bucket(self, bucket_id=None):
        """ Contains all bucket related calls.

            Parameters
            ----------
            bucket_id: str
                Unique bucket ID.

            Returns
            -------
            Bucket:
                Object what interacts with buckets.
        """

        return Bucket(bucket_id=bucket_id)

    def source_file(self, source_file_id):
        """ Contains source file related calls.

            Parameters
            ----------
            source_file_id: str
                Unique source file ID.

            Returns
            -------
            SourceFile:
                Object for interacting with source files.
        """

        return SourceFile(source_file_id=source_file_id)

    def file(self, file_id):
        """ Contains all file related calls.

            Parameters
            ----------
            file_id: str
                Unique file ID.

            Returns
            -------
            File:
                Object for interacting with files.
        """

        return File(file_id=file_id)
