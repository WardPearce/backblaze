from .resources import AIOHTTP, CONFIG


class AWR:
    """ Wrapped Aiohttp for B2. """

    def __init__(self, route, **kwargs):
        self.route = route
        self.kwargs = kwargs

    async def get(self):
        pass

    async def post(self):
        """ Wrapped async post request. """

        async with AIOHTTP.post(self.route, **self.kwargs) as resp:
            if resp.status == 200:
                return await resp.json()
