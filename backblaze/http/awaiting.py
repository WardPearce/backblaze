from typing import AsyncGenerator, Callable, Union
from asyncio import sleep
from httpx import AsyncClient

from .base import BaseHTTP
from ..exceptions import RequestAttemptsFailed


class AwaitingHTTP(BaseHTTP):
    authorize: Callable
    account_id: str
    _client: AsyncClient

    async def __handle(self, request, resp_json: bool = True,
                       include_account: bool = True,
                       *args, **kwargs) -> Union[dict, bytes, None]:

        if include_account:
            if "json" in kwargs:
                kwargs["json"]["accountId"] = self.account_id
            else:
                kwargs["json"] = {"accountId": self.account_id}

        for _ in range(0, 3):
            resp = await request(*args, **kwargs)
            if resp.status_code == 401:
                await self.authorize()
            elif resp.status_code == 503 or resp.status_code == 429:
                if "Retry-After" in resp.headers:
                    await sleep(float(resp.headers["Retry-After"]))
                else:
                    await sleep(1.0)
            else:
                return self.handle_resp(
                    resp,
                    resp_json,
                )

        print(resp.status_code)  # type: ignore

        raise RequestAttemptsFailed()

    async def _get(self, resp_json: bool = True,
                   include_account: bool = True,
                   *args, **kwargs) -> Union[dict, bytes, None]:
        return await self.__handle(
            self._client.get,
            resp_json,
            include_account,
            *args,
            **kwargs
        )

    async def _post(self, resp_json: bool = True,
                    include_account: bool = True,
                    *args, **kwargs) -> Union[dict, bytes, None]:
        return await self.__handle(
            self._client.post,
            resp_json,
            include_account,
            *args,
            **kwargs
        )

    async def _stream(self, *args, **kwargs) -> AsyncGenerator[bytes, None]:
        async with self._client.stream("GET", *args, **kwargs) as resp:
            resp.raise_for_status()

            async for chunk in resp.aiter_bytes():
                yield chunk
