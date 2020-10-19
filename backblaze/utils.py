from datetime import datetime, timedelta

from .models.file import UploadUrlModel

from .cache import Cache


def format_route_name(name: str) -> str:
    """Used to format route name.

    Parameters
    ----------
    name : str

    Returns
    -------
    str
    """

    return name.replace("Route", "").lower()


class UploadUrlCache:
    def __init__(self, bucket_id: str, file_id: str = None) -> None:
        """Used to handled cached upload URLs.

        Parameters
        ----------
        bucket_id : str
        file_id : str, optional
            by default None

        Notes
        -----
        If file_id passed Cache.upload_parts_urls is used
        instead of Cache.upload_urls.
        """

        if not file_id:
            self.upload_cache = Cache.upload_urls
            self.index = bucket_id
        else:
            self.upload_cache = Cache.upload_parts_urls
            self.index = bucket_id + file_id

    def find(self) -> UploadUrlModel:
        """Looks for cached item.

        Returns
        -------
        UploadUrlModel
        """

        if self.index in self.upload_cache:
            if datetime.now() >= self.upload_cache[self.index]["expires"]:
                self.upload_cache.pop(self.index, None)
            else:
                return self.upload_cache[self.index]["model"]

    def save(self, upload_model: UploadUrlModel) -> UploadUrlModel:
        """Saves upload model into cache.

        Parameters
        ----------
        upload_model : UploadUrlModel

        Returns
        -------
        UploadUrlModel
        """

        self.upload_cache[self.index] = {
            "expires": datetime.now() + timedelta(hours=23, minutes=50),
            "model": upload_model
        }

        return upload_model

    def delete(self) -> None:
        """Deletes upload out of the cache.
        """

        self.upload_cache.pop(self.index, None)


def encode_name(name: str, encoding: str = "utf-8",
                replace: bool = True) -> str:
    """Used to encode names correctly for b2.

    Parameters
    ----------
    name : str
    encoding : str, optional
        by default "utf-8"
    replace : bool, optional
        by default True

    Returns
    -------
    str
    """

    if replace:
        name = name.replace(" ", "-")

    return name.encode(encoding).decode(encoding)
