import typing
from httpx import BasicAuth

from .routes import (
    BucketRoute,
    KeyRoute,
    FileRoute,
    UploadRoute,
    DownloadRoute
)
from .utils import format_route_name


class Routes:
    bucket: BucketRoute
    key: KeyRoute
    file: FileRoute
    upload: UploadRoute
    download: DownloadRoute


class Base:
    _routes = Routes()
    _auth_url = "https://api.backblazeb2.com/b2api/v2/b2_authorize_account"
    _refresh_seconds = 84600
    _running_task = False

    account_id = None

    __api_routes = [
        BucketRoute,
        KeyRoute,
        FileRoute,
        UploadRoute
    ]

    __download_routes = [
        DownloadRoute
    ]

    def __init__(self, key_id: str, key: str, timeout: int = 30) -> None:
        """Used to interact with B2 account.

        Parameters
        ----------
        key_id : str
            Application Key ID.
        key : str
            Application Key
        timeout : int, optional
            Max time a request can take, by default 30

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
        for route in self.__api_routes:
            self.__format_route(api_url, route)

        for route in self.__download_routes:
            self.__format_route(download_url, route)
