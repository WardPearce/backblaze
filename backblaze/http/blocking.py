from typing import Any

from .base import BaseHTTP


class BlockingHTTP(BaseHTTP):
    def __handle(self, request, resp_json: bool = True,
                 *args, **kwargs) -> Any:
        resp = request(*args, **kwargs)

        return self.handle_resp(
            resp,
            resp_json,
        )

    def _get(self, resp_json: bool = True, *args, **kwargs) -> Any:
        return self.__handle(
            self._client.get,
            resp_json,
            *args,
            **kwargs
        )

    def _post(self, resp_json: bool = True, *args, **kwargs) -> Any:
        return self.__handle(
            self._client.post,
            resp_json,
            *args,
            **kwargs
        )
