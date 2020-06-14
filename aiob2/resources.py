class Sessions:
    AIOHTTP = None


SESSIONS = Sessions()


class Config:
    """ Contains infomation from auth request. """

    api_url = None
    download_url = None
    account_id = None
    authorization = None
    max_cache = None
    chunk_size = None


CONFIG = Config()
