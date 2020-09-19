from httpx import BasicAuth

from .routes import BucketRoute, Route
from .utils import format_route_name


class Routes:
    bucket: Route


class Base:
    _routes = Routes()
    _auth_url = "https://api.backblazeb2.com/b2api/v2/b2_authorize_account"
    _refresh_seconds = 84600

    def __init__(self, key_id: str, key: str) -> None:
        """Used to interact with B2 account.

        Parameters
        ----------
        key_id : str
            Application Key ID.
        key : str
            Application Key
        """

        self._auth = BasicAuth(
            key_id,
            key
        )

    def _format_routes(self, api_url: str, download_url: str) -> None:
        for route in [BucketRoute]:
            route_obj = route(api_url)
            route_obj.format()

            setattr(
                self._routes,
                format_route_name(type(route_obj).__name__),
                route_obj
            )
