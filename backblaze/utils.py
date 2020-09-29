import typing

from datetime import datetime, timedelta

from .models.file import UploadUrlModel

from .cache import Cache


def format_route_name(name: str) -> str:
    return name.replace("Route", "").lower()


class UploadUrlCache:
    def __init__(self, bucket_id: str, parts: bool = False) -> None:
        if not parts:
            self.upload_cache = Cache.upload_urls
        else:
            self.upload_cache = Cache.upload_parts_urls

        self.bucket_id = bucket_id

    def find(self) -> UploadUrlModel:
        if self.bucket_id in self.upload_cache:
            if datetime.now() >= self.upload_cache[self.bucket_id]["expires"]:
                self.upload_cache.pop(self.bucket_id, None)
            else:
                return self.upload_cache[self.bucket_id]["model"]

    def save(self, upload_model: UploadUrlModel) -> UploadUrlModel:
        self.upload_cache[self.bucket_id] = {
            "expires": datetime.now() + timedelta(hours=23, minutes=50),
            "model": upload_model
        }

        return upload_model


def read_in_chunks(file, chunk_size: int = 1024
                   ) -> typing.Generator[bytes, None]:
    data = b""

    while data:
        data = file.read(chunk_size)
        if data:
            yield data


def encode_name(name: str, encoding: str = "utf-8") -> str:
    return name.replace(" ", "-").encode(encoding).decode(encoding)
