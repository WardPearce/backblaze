import logging

from json import JSONDecodeError
from typing import Any

from httpx import Response

from ..exceptions import (
    BadRequest,
    UnAuthorized,
    Forbidden,
    RequestTimeout,
    TooManyRequests,
    InternalError,
    ServiceUnavailable
)


class BaseHTTP:
    def handle_resp(self, resp: Response, json: bool = True) -> Any:
        """Handles resp response.

        Parameters
        ----------
        resp : Response

        Returns
        -------
        Any

        Raises
        ------
        BadRequest
        UnAuthorized
        Forbidden
        RequestTimeout
        TooManyRequests
        InternalError
        ServiceUnavailable
        HTTPStatusError
            Raised when none of the above are.
        """

        if resp.status_code == 200:
            if json:
                return resp.json()
            else:
                return resp.read()
        else:
            try:
                logging.debug(resp.json())
            except JSONDecodeError:
                pass

            if resp.status_code == 400:
                raise BadRequest()
            elif resp.status_code == 401:
                raise UnAuthorized()
            elif resp.status_code == 403:
                raise Forbidden()
            elif resp.status_code == 408:
                raise RequestTimeout()
            elif resp.status_code == 429:
                raise TooManyRequests()
            elif resp.status_code == 500:
                raise InternalError()
            elif resp.status_code == 503:
                raise ServiceUnavailable()
            else:
                resp.raise_for_status()
