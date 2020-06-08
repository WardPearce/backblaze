from .resources import AIOHTTP, CONFIG
from .exceptions import BadRequest, InvalidAuthorization, \
    Forbidden, RequestTimeout, TooManyRequests, InternalError, \
    ServiceUnavailable


class AWR:
    """ Wrapped Aiohttp for B2. """

    def __init__(self, route, **kwargs):
        self.route = route

        if "headers" not in kwargs:
            kwargs["headers"] = CONFIG.authorization

        self.kwargs = kwargs

    async def _validate(self, resp, json=True):
        if resp.status == 200:
            if json:
                return await resp.json()
            else:
                return await resp.read()
        else:
            error_message = await resp.json()

            if "message" in error_message:
                error_message = error_message["message"]
            else:
                error_message = None

            if resp.status == 400:
                raise BadRequest(error_message)
            elif resp.status == 401:
                raise InvalidAuthorization(error_message)
            elif resp.status == 403:
                raise Forbidden(error_message)
            elif resp.status == 408:
                raise RequestTimeout(error_message)
            elif resp.status == 429:
                raise TooManyRequests(error_message)
            elif resp.status == 500:
                raise InternalError(error_message)
            elif resp.status == 503:
                raise ServiceUnavailable(error_message)

    async def get(self):
        """ Wrapped async get request. """

        async with AIOHTTP.get(self.route, **self.kwargs) as resp:
            return await self._validate(resp)

    async def post(self):
        """ Wrapped async post request. """

        async with AIOHTTP.post(self.route, **self.kwargs) as resp:
            return await self._validate(resp)
