from typing import Any

from .base import BaseHTTP


class AwaitingHTTP(BaseHTTP):
    async def __handle(self, request, resp_json: bool = True,
                       *args, **kwargs) -> Any:
        async with request(*args, **kwargs) as resp:
            return self.handle_resp(
                resp,
                resp_json,
            )

    async def _get(self, resp_json: bool = True, *args, **kwargs) -> Any:
        return await self.__handle(
            self._client.get,
            resp_json,
            *args,
            **kwargs
        )

    async def _post(self, resp_json: bool = True, *args, **kwargs) -> Any:
        return await self.__handle(
            self._client.post,
            resp_json,
            *args,
            **kwargs
        )
