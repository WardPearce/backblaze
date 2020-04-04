class List(object):
    def __init__(self, obj):
        self.obj = obj

    async def keys(self, **kwargs):
        """ https://www.backblaze.com/b2/docs/b2_list_keys.html """

        return await self.obj._post(url=self.obj.ROUTES["list_keys"].format(self.obj.api_url),
                                   json={"accountId": self.obj.account_id, **kwargs,})

    async def buckets(self, **kwargs):
        """ https://www.backblaze.com/b2/docs/b2_list_buckets.html """

        return await self.obj._post(url=self.obj.ROUTES["list_buckets"].format(self.obj.api_url),
                                   json={"accountId": self.obj.account_id, **kwargs,})