from typing import Any

from .base import BaseHTTP


class BlockingHTTP(BaseHTTP):
    def __handle(self, request, resp_json: bool = True,
                 *args, **kwargs) -> Any:
        if not kwargs:
            kwargs = {}

        if "json" in kwargs:
            kwargs["json"]["accountId"] = self.account_id
        else:
            kwargs["json"] = {"accountId": self.account_id}

        for _ in range(0, 2):
            resp = request(*args, **kwargs)
            if resp.status_code == 401:
                self.authorize()
            else:
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
