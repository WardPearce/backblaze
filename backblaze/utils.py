from datetime import datetime, timedelta

from .models.file import UploadUrlModel

from .cache import Cache


def format_route_name(name: str) -> str:
    return name.replace("Route", "").lower()


class UploadUrlCache:
    def __init__(self, bucket_id: str, file_id: str = None) -> None:
        if not file_id:
            self.upload_cache = Cache.upload_urls
            self.index = bucket_id
        else:
            self.upload_cache = Cache.upload_parts_urls
            self.index = bucket_id + file_id

    def find(self) -> UploadUrlModel:
        if self.index in self.upload_cache:
            if datetime.now() >= self.upload_cache[self.index]["expires"]:
                self.upload_cache.pop(self.index, None)
            else:
                return self.upload_cache[self.index]["model"]

    def save(self, upload_model: UploadUrlModel) -> UploadUrlModel:
        self.upload_cache[self.index] = {
            "expires": datetime.now() + timedelta(hours=23, minutes=50),
            "model": upload_model
        }

        return upload_model


def encode_name(name: str, encoding: str = "utf-8",
                replace: bool = True) -> str:
    if replace:
        name = name.replace(" ", "-")

    return name.encode(encoding).decode(encoding)
