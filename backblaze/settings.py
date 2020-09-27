from typing import List, Dict
from datetime import datetime


class CorSettings:
    payload = {}

    def __init__(self, name: str, origins: list, allowed_headers: list,
                 operations: list, expose_headers: list, max_age: int) -> None:

        self.payload["corsRuleName"] = name.replace(" ", "-")
        self.payload["allowedOrigins"] = origins
        self.payload["allowedHeaders"] = allowed_headers
        self.payload["allowedOperations"] = operations
        self.payload["exposeHeaders"] = expose_headers
        self.payload["maxAgeSeconds"] = max_age


class LifecycleSettings:
    payload = {}

    def __init__(self, hiding_to_delete: int,
                 uploading_to_hide: int, prefix: str) -> None:

        self.payload["daysFromHidingToDeleting"] = hiding_to_delete
        self.payload["daysFromUploadingToHiding"] = uploading_to_hide
        self.payload["fileNamePrefix"] = prefix


class BucketSettings:
    payload = {}

    def __init__(self, name: str, private: bool = True,
                 info: str = None, cors: List[CorSettings] = None,
                 lifecycle: LifecycleSettings = None) -> None:

        self.payload["bucketName"] = name.replace(" ", "-")
        self.payload["bucketType"] = "allPrivate" if private else "allPublic"

        if info:
            self.payload["bucketInfo"] = info

        if lifecycle:
            self.payload["lifecycleRules"] = lifecycle.payload

        if cors:
            self.payload["corsRules"] = []
            cors_append = self.payload["corsRules"].append

            for cor in cors:
                cors_append(cor.payload)


class KeySettings:
    payload = {}

    def __init__(self, capabilities: list, name: str,
                 duration: int = None, bucket_id: str = None,
                 prefix: str = None) -> None:

        self.payload["capabilities"] = capabilities
        self.payload["keyName"] = name.replace(" ", "-")

        if duration:
            self.payload["validDurationInSeconds"] = duration

        if bucket_id:
            self.payload["bucketId"] = bucket_id

        if prefix:
            self.payload["namePrefix"] = prefix


class FileSettings:
    payload = {}

    def __init__(self, start_file_name: str = None,
                 limit: int = 100, prefix: str = "",
                 delimiter: str = None) -> None:

        if start_file_name:
            self.payload["startFileName"] = start_file_name

        if limit:
            self.payload["maxFileCount"] = limit

        if prefix:
            self.payload["prefix"] = prefix

        if delimiter:
            self.payload["delimiter"] = delimiter


class DownloadSettings:
    headers = {}
    parameters = {}

    def __init__(self, range: int = None, disposition: str = None,
                 language: str = None, expires: datetime = None,
                 cache_control: str = None, encoding: str = None,
                 content_type: str = None) -> None:

        if range:
            self.headers["Range"] = range

        if disposition:
            self.parameters["b2ContentDisposition"] = disposition

        if language:
            self.parameters["b2ContentLanguage"] = language

        if expires:
            self.parameters["b2Expires"] = expires.timestamp() * 1000

        if cache_control:
            self.parameters["b2CacheControl"] = cache_control

        if encoding:
            self.parameters["b2ContentEncoding"] = encoding

        if content_type:
            self.parameters["b2ContentType"] = content_type


class UploadSettings:
    headers = {}

    def __init__(self, name: str, content_type: str = "b2/x-auto",
                 last_modified: datetime = None, disposition: str = None,
                 language: str = None, expires: datetime = None,
                 cache_control: str = None, encoding: str = None,
                 custom_headers: Dict[str, str] = None) -> None:

        self.headers["X-Bz-File-Name"] = name
        self.headers["Content-Type"] = content_type

        if last_modified:
            self.headers["X-Bz-Info-src_last_modified_millis"
                         ] = last_modified.timestamp() * 1000

        if disposition:
            self.headers["X-Bz-Info-b2-content-disposition"] = disposition

        if language:
            self.headers["X-Bz-Info-b2-content-language"] = language

        if expires:
            self.headers["X-Bz-Info-b2-expires"] = expires.timestamp() * 1000

        if cache_control:
            self.headers["X-Bz-Info-b2-cache-control"] = cache_control

        if encoding:
            self.headers["X-Bz-Info-b2-content-encoding"] = encoding

        if custom_headers:
            for header, value in custom_headers.items():
                self.headers["X-Bz-Info-{}".format(header)] = value
