from typing import Any
from time import sleep

from .base import BaseHTTP


class BlockingHTTP(BaseHTTP):
    def __handle(self, request, resp_json: bool = True,
                 include_account: bool = True,
                 *args, **kwargs) -> Any:

        if include_account:
            if "json" in kwargs:
                kwargs["json"]["accountId"] = self.account_id
            else:
                kwargs["json"] = {"accountId": self.account_id}

        for _ in range(0, 2):
            resp = request(*args, **kwargs)
            if resp.status_code == 401:
                self.authorize()
            elif resp.status_code == 503 or resp.status_code == 429:
                if "Retry-After" in resp.headers:
                    sleep(float(resp.headers["Retry-After"]))
                else:
                    sleep(1.0)
            else:
                return self.handle_resp(
                    resp,
                    resp_json,
                )

    def _get(self, resp_json: bool = True,
             include_account: bool = True,
             *args, **kwargs) -> Any:
        return self.__handle(
            self._client.get,
            resp_json,
            include_account,
            *args,
            **kwargs
        )

    def _post(self, resp_json: bool = True,
              include_account: bool = True,
              *args, **kwargs) -> Any:
        return self.__handle(
            self._client.post,
            resp_json,
            include_account,
            *args,
            **kwargs
        )
