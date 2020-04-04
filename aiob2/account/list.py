class List(object):
    def __init__(self, account_id, obj):
        self.obj = obj
        self.account_id = account_id

    async def keys(self, **kwargs):
        """ https://www.backblaze.com/b2/docs/b2_list_keys.html """

        return await self.obj._post(self.obj.ROUTES["list_keys"].format(self.obj.api_url),
                                   json={"accountId": self.account_id, **kwargs,})

    async def buckets(self, **kwargs):
        """ https://www.backblaze.com/b2/docs/b2_list_buckets.html """

        return await self.obj._post(self.obj.ROUTES["list_buckets"].format(self.obj.api_url),
                                   json={"accountId": self.account_id, **kwargs,})