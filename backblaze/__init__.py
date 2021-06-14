import sys
import asyncio
import threading
import time

from httpx import AsyncClient, Client
from typing import Any, Generator, AsyncGenerator, Tuple
from random import randint

from .base import Base

from .models.auth import AuthModel
from .models.bucket import BucketModel
from .models.key import KeyModel

from .http.awaiting import AwaitingHTTP
from .http.blocking import BlockingHTTP

from .bucket.awaiting import AwaitingBucket
from .bucket.blocking import BlockingBucket

from .key.blocking import BlockingKey
from .key.awaiting import AwaitingKey

from .settings import BucketSettings, KeySettings, DownloadSettings

from .decorators import authorize_required


class Awaiting(Base, AwaitingHTTP):
    def __init__(self, *args, **kwargs) -> None:
        if not sys.version_info[1] >= 7:
            sys.exit("Python 3.7 & above is required.")

        super().__init__(*args, **kwargs)

        self._client = AsyncClient(
            timeout=self._timeout,
            limits=self._limits,
            headers={"User-Agent": self._user_agent}
        )

    async def close(self) -> None:
        """Closes any underlying TCP sessions.
        """

        await self._client.aclose()

    @authorize_required
    async def download_by_name(self, bucket_name: str, file_name: str,
                               settings: DownloadSettings = None) -> bytes:
        """Used to download a file by its name.

        Parameters
        ----------
        bucket_name : str
            Name of bucket.
        file_name : str
            Name of file to download.
        settings : DownloadSettings, optional
            by default None

        Returns
        -------
        bytes

        Notes
        -----
        Use bucket.file.download instead whenever you can.
        """

        if not settings:
            params = None
            headers = None
        else:
            params = settings.parameters
            headers = settings.headers

        return await self._get(
            url="{}/{}/{}".format(
                self._routes.download.file,
                bucket_name,
                file_name
            ),
            headers=headers,
            params=params,
            resp_json=False,
            include_account=False
        )

    @authorize_required
    async def create_key(self, settings: KeySettings
                         ) -> Tuple[KeyModel, AwaitingKey]:
        """Used to create a key.

        Parameters
        ----------
        settings: KeySettings
            Used to hold details on a key.

        Returns
        -------
        KeyModel
            Holds details on key.
        AwaitingKey
        """

        data = await self._post(
            json=settings.payload,
            url=self._routes.key.create
        )

        return KeyModel(data), self.key(data["applicationKeyId"])

    @authorize_required
    async def keys(self, limit: int = 100,
                   start_key_id: str = None
                   ) -> AsyncGenerator[Any, None]:
        """Used to list keys.

        Parameters
        ----------
        limit : int, optional
            Used to limit the listing, by default 100
        start_key_id : str, optional
            Key to start listing from, by default None

        Yields
        -------
        KeyModel
            Holds details on key.
        AwaitingKey
        str
            Next application key ID.
        """

        data = await self._post(
            url=self._routes.key.list,
            json={"maxKeyCount": limit, "startApplicationKeyId": start_key_id}
        )

        for key in data["keys"]:
            yield (
                KeyModel(key),
                self.key(key["applicationKeyId"]),
                data["nextApplicationKeyId"]
            )

    def key(self, key_id: str) -> AwaitingKey:
        """Used to interact with key.

        Parameters
        ----------
        key_id : str
            ID of key.

        Returns
        -------
        AwaitingKey
        """

        return AwaitingKey(self, key_id)

    @authorize_required
    async def create_bucket(self, settings: BucketSettings
                            ) -> Tuple[BucketModel, AwaitingBucket]:
        """Used to create a bucket.

        Parameters
        ----------
        settings: BucketSettings
            Holds bucket settings.

        Returns
        -------
        BucketModel
            Holds details on a bucket.
        AwaitingBucket
            Used to interact with a bucket.
        """

        data = BucketModel(await self._post(
            url=self._routes.bucket.create,
            json=settings.payload
        ))

        return data, self.bucket(data.bucket_id)

    @authorize_required
    async def buckets(self, types: list = ["all"]
                      ) -> AsyncGenerator[BucketModel, AwaitingBucket]:
        """Lists buckets.

        Parameters
        ----------
        types : list, optional
            Used to filter bucket types, by default ["all"]

        Yields
        -------
        BucketModel
            Holds details on bucket.
        AwaitingBucket
            Used for interacting with bucket.
        """

        data = await self._post(
            url=self._routes.bucket.list,
            json={"bucketTypes": types}
        )

        for bucket in data["buckets"]:
            yield BucketModel(bucket), self.bucket(bucket["bucketId"])

    def bucket(self, bucket_id: str) -> AwaitingBucket:
        """Used to interact with a bucket.

        Parameters
        ----------
        bucket_id : str
            ID of Bucket.

        Returns
        -------
        AwaitingBucket
        """

        return AwaitingBucket(self, bucket_id)

    async def __authorize_background(self) -> None:
        """Used to refresh auth tokens every 23.5 hours.
        """

        self._running_task = True
        await asyncio.sleep(self._refresh_seconds + randint(0, 1500))
        self._running_task = False

        await self.authorize()
        self._check_cache()

    async def authorize(self) -> AuthModel:
        """Used to authorize B2 account.

        Returns
        -------
        AuthModel
            Holds data on account auth.
        """

        resp = await self._client.get(url=self._auth_url, auth=self._auth)
        resp.raise_for_status()

        data = AuthModel(resp.json())

        self.account_id = data.account_id

        self._format_routes(
            data.api_url,
            data.download_url
        )

        self._client.headers["Authorization"] = data.authorization_token

        if not self._running_task:
            asyncio.create_task(self.__authorize_background())

        return data


class Blocking(Base, BlockingHTTP):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self._client = Client(
            timeout=self._timeout,
            limits=self._limits,
            headers={"User-Agent": self._user_agent}
        )

    def close(self) -> None:
        """Closes any underlying TCP sessions.
        """

        self._client.close()

    @authorize_required
    def download_by_name(self, bucket_name: str, file_name: str,
                         settings: DownloadSettings = None) -> bytes:
        """Used to download a file by its name.

        Parameters
        ----------
        bucket_name : str
            Name of bucket.
        file_name : str
            Name of file to download.
        settings : DownloadSettings, optional
            by default None

        Returns
        -------
        bytes

        Notes
        -----
        Use bucket.file.download instead whenever you can.
        """

        if not settings:
            params = None
            headers = None
        else:
            params = settings.parameters
            headers = settings.headers

        return self._get(
            url="{}/{}/{}".format(
                self._routes.download.file,
                bucket_name,
                file_name
            ),
            headers=headers,
            params=params,
            resp_json=False,
            include_account=False
        )

    @authorize_required
    def create_key(self, settings: KeySettings
                   ) -> Tuple[KeyModel, BlockingKey]:
        """Used to create a key.

        Parameters
        ----------
        settings: KeySettings
            Used to hold details on a key.

        Returns
        -------
        KeyModel
            Holds details on key.
        BlockingKey
        """

        data = self._post(
            json=settings.payload,
            url=self._routes.key.create
        )

        return KeyModel(data), self.key(data["applicationKeyId"])

    @authorize_required
    def keys(self, limit: int = 100,
             start_key_id: str = None
             ) -> Generator[KeyModel, AwaitingKey, None]:
        """Used to list keys.

        Parameters
        ----------
        limit : int, optional
            Used to limit the listing, by default 100
        start_key_id : str, optional
            Key to start listing from, by default None

        Yields
        -------
        KeyModel
            Holds details on key.
        AwaitingKey
        """

        data = self._post(
            url=self._routes.key.list,
            json={"maxKeyCount": limit, "startApplicationKeyId": start_key_id}
        )

        for key in data["keys"]:
            yield KeyModel(key), self.key(key["applicationKeyId"])

    def key(self, key_id: str) -> BlockingKey:
        """Used to interact with key.

        Parameters
        ----------
        key_id : str
            ID of key.

        Returns
        -------
        BlockingKey
        """

        return BlockingKey(self, key_id)

    @authorize_required
    def create_bucket(self, settings: BucketSettings
                      ) -> Tuple[BucketModel, BlockingBucket]:
        """Used to create a bucket.

        Parameters
        ----------
        settings: BucketSettings
            Holds bucket settings.

        Returns
        -------
        BucketModel
            Holds details on a bucket.
        BlockingBucket
            Used to interact with a bucket.
        """

        data = BucketModel(self._post(
            url=self._routes.bucket.create,
            json=settings.payload,
        ))

        return data, self.bucket(data.bucket_id)

    @authorize_required
    def buckets(self, types: list = ["all"]
                ) -> Generator[BucketModel, BlockingBucket, None]:
        """Lists buckets.

        Parameters
        ----------
        types : list, optional
            Used to filter bucket types, by default ["all"]

        Yields
        -------
        BucketModel
            Holds details on bucket.
        BlockingBucket
            Used for interacting with bucket.
        """

        data = self._post(
            url=self._routes.bucket.list,
            json={"bucketTypes": types}
        )

        for bucket in data["buckets"]:
            yield BucketModel(bucket), self.bucket(bucket["bucketId"])

    def bucket(self, bucket_id: str) -> BlockingBucket:
        """Used to interact with a bucket.

        Parameters
        ----------
        bucket_id : str
            ID of Bucket.

        Returns
        -------
        BlockingBucket
        """

        return BlockingBucket(self, bucket_id)

    def __authorize_background(self) -> None:
        """Used to refresh auth tokens every 23.5 hours.
        """

        self._running_task = True
        time.sleep(self._refresh_seconds + randint(0, 1500))
        self._running_task = False

        self.authorize()
        self._check_cache()

    def authorize(self) -> AuthModel:
        """Used to authorize B2 account.

        Returns
        -------
        AuthModel
            Holds data on account auth.
        """

        resp = self._client.get(self._auth_url, auth=self._auth)
        resp.raise_for_status()

        data = AuthModel(resp.json())

        self.account_id = data.account_id

        self._format_routes(
            data.api_url,
            data.download_url
        )

        self._client.headers["Authorization"] = data.authorization_token

        if not self._running_task:
            threading.Thread(target=self.__authorize_background)

        return data
