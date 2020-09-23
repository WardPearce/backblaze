from typing import Any

from .base import BaseHTTP


class AwaitingHTTP(BaseHTTP):
    async def __handle(self, request, resp_json: bool = True,
                       *args, **kwargs) -> Any:
        for _ in range(0, 2):
            async with request(*args, **kwargs) as resp:
                if resp.status_code == 401:
                    await self.authorize()
                else:
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
