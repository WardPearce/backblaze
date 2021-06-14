from sys import version_info
from httpx import BasicAuth, Limits
from datetime import datetime

from .routes import (
    BucketRoute,
    KeyRoute,
    FileRoute,
    UploadRoute,
    DownloadRoute
)
from .utils import format_route_name
from .cache import Cache


__version__ = "0.0.8"
__url__ = "https://backblaze.readthedocs.io/en/latest/"
__description__ = "Wrapper for Backblaze's B2."
__author__ = "WardPearce"
__author_email__ = "wardpearce@protonmail.com"
__license__ = "GPL-3.0 License"


class Routes:
    bucket: BucketRoute
    key: KeyRoute
    file: FileRoute
    upload: UploadRoute
    download: DownloadRoute


class Base:
    _auth_url = "https://api.backblazeb2.com/b2api/v2/b2_authorize_account"
    _refresh_seconds = 82800

    __api_routes = [
        BucketRoute,
        KeyRoute,
        FileRoute,
        UploadRoute
    ]

    __download_routes = [
        DownloadRoute
    ]

    def __init__(self, key_id: str, key: str, timeout: int = 30,
                 chunk_size: int = 5000024) -> None:
        """Used to interact with B2 account.

        Parameters
        ----------
        key_id : str
            Application Key ID.
        key : str
            Application Key
        timeout : int, optional
            Max time a request can take, by default 30
        chunk_size : int, optional
            File reading chunk size, must be above 5mb, by default 5000024

        Notes
        -----
        In theory timeout could be 3 times longer then you set.
        If a request takes X amount of seconds and then gets 401d
        the authorize function will be called again and the request reissued.

        The authorize could take another X amount of seconds and then the
        reissued request could take another X amount of seconds.
        """

        self._auth = BasicAuth(
            key_id,
            key
        )

        self._timeout = timeout
        self._limits = Limits(
            max_connections=None,
            max_keepalive_connections=None
        )
        self._user_agent = (
            "backblaze/{0}+python/{1.major}.{1.minor}.{1.micro}".format(
                __version__, version_info
            )
        )
        self.chunk_size = chunk_size

        self._routes = Routes()
        self._running_task = False
        self.account_id = None

    def __format_route(self, url, routes) -> None:
        for route in routes:
            route_obj = route(url)
            route_obj.format()

            setattr(
                self._routes,
                format_route_name(type(route_obj).__name__),
                route_obj
            )

    def _format_routes(self, api_url: str, download_url: str) -> None:
        self.__format_route(api_url, self.__api_routes)
        self.__format_route(download_url, self.__download_routes)

    def _check_cache(self) -> None:
        """Checks upload_parts_urls & upload_urls for any
        expired URls. This is mainly for upload_parts_urls what
        is cached on a per file ID basis.

        Notes
        -----
        This is ran in the background as part of __authorize_background.
        """

        now = datetime.now()

        if Cache.upload_parts_urls:
            for index, cached_upload in dict(Cache.upload_parts_urls).items():
                if now >= cached_upload["expires"]:
                    Cache.upload_parts_urls.pop(index, None)

        if Cache.upload_urls:
            for index, cached_upload in dict(Cache.upload_urls).items():
                if now >= cached_upload["expires"]:
                    Cache.upload_urls.pop(index, None)
