import aiohttp


AIOHTTP = aiohttp.ClientSession()


class Config:
    """ Contains infomation from auth request. """

    api_url = None
    download_url = None
    account_id = None
    authorization = None


CONFIG = Config()
