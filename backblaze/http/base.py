import logging

from json import JSONDecodeError
from typing import Union

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


HTTP_ERRORS = {
    400: BadRequest,
    401: UnAuthorized,
    403: Forbidden,
    408: RequestTimeout,
    429: TooManyRequests,
    500: InternalError,
    503: ServiceUnavailable
}


class BaseHTTP:
    def handle_resp(self, resp: Response, json: bool = True
                    ) -> Union[dict, bytes, None]:
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
        """

        if resp.status_code not in HTTP_ERRORS:
            if json:
                return resp.json()
            else:
                return resp.read()
        else:
            try:
                logging.debug(resp.json())
            except JSONDecodeError:
                pass

            raise HTTP_ERRORS[resp.status_code]
