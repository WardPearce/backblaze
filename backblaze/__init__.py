from httpx import AsyncClient, Client

from .base import Base

from .models.auth import AuthModel

from .http.awaiting import AwaitingHTTP
from .http.blocking import BlockingHTTP


__version__ = "0.0.0"
__url__ = "https://backblaze.readthedocs.io/en/latest/"
__description__ = "Wrapper for Backblaze's B2."
__author__ = "WardPearce"
__author_email__ = "wardpearce@protonmail.com"
__license__ = "GPL-3.0 License"


class Awaiting(Base, AwaitingHTTP):
    def __init__(self, *args, **kwargs) -> None:

        super().__init__(*args, **kwargs)

        self._client = AsyncClient(auth=self._auth)

    async def close(self) -> None:
        """Closes any underlying TCP sessions.
        """

        await self._client.aclose()

    async def authorize(self) -> AuthModel:
        """Used to authorize B2 account.

        Returns
        -------
        AuthModel
            Holds data on account auth.
        """

        data = AuthModel(await self._get(url=self._auth_url))

        self.format_routes(
            data.api_url,
            data.download_url
        )

        return data


class Blocking(Base, BlockingHTTP):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self._client = Client(auth=self._auth)

    def close(self) -> None:
        """Closes any underlying TCP sessions.
        """

        self._client.close()

    def authorize(self) -> AuthModel:
        """Used to authorize B2 account.

        Returns
        -------
        AuthModel
            Holds data on account auth.
        """

        data = AuthModel(self._get(url=self._auth_url))

        self.format_routes(
            data.api_url,
            data.download_url
        )

        return data
