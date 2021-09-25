from typing import List, Dict, Union, cast
from datetime import datetime
from urllib import parse

from .utils import encode_name


ENCODING = "utf-8"


class CorSettings:
    """
    Parameters
    ----------
    name : str
    origins : list
    allowed_headers : list
    operations : list
    expose_headers : list
    max_age : int
    """

    def __init__(self, name: str, origins: list, allowed_headers: list,
                 operations: list, expose_headers: list, max_age: int) -> None:
        self.payload = {
            "corsRuleName": encode_name(name),
            "allowedOrigins": origins,
            "allowedHeaders": allowed_headers,
            "allowedOperations": operations,
            "exposeHeaders": expose_headers,
            "maxAgeSeconds": max_age
        }


class LifecycleSettings:
    """
    Parameters
    ----------
    hiding_to_delete : int
    uploading_to_hide : int
    prefix : str
    """

    def __init__(self, hiding_to_delete: int,
                 uploading_to_hide: int, prefix: str) -> None:
        self.payload = {
            "daysFromHidingToDeleting": hiding_to_delete,
            "daysFromUploadingToHiding": uploading_to_hide,
            "fileNamePrefix": prefix
        }


class BucketUpdateSettings:
    """
    Parameters
    ----------
    private : bool, optional
        by default True
    info : str, optional
        by default None
    cors : List[CorSettings], optional
        by default None
    lifecycle : LifecycleSettings, optional
        by default None
    """

    def __init__(self, private: bool = True,
                 info: str = None, cors: List[CorSettings] = None,
                 lifecycle: LifecycleSettings = None) -> None:
        self.payload: Dict[str, Union[str, dict, list]] = {
            "bucketType": "allPrivate" if private else "allPublic"
        }

        if info is not None:
            self.payload["bucketInfo"] = info

        if lifecycle is not None:
            self.payload["lifecycleRules"] = lifecycle.payload

        if cors is not None:
            self.payload["corsRules"] = []
            cors_append = self.payload["corsRules"].append

            for cor in cors:
                cors_append(cor.payload)


class BucketSettings(BucketUpdateSettings):
    """
    Parameters
    ----------
    name : str
    private : bool, optional
        by default None
    info : str, optional
        by default None
    cors : List[CorSettings], optional
        by default None
    lifecycle : LifecycleSettings, optional
        by default None
    """

    def __init__(self, name: str, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.payload["bucketName"] = encode_name(name)


class KeySettings:
    """
    Parameters
    ----------
    capabilities : list
    name : str
    duration : int, optional
        by default None
    bucket_id : str, optional
        by default None
    prefix : str, optional
        by default None
    """

    def __init__(self, capabilities: list, name: str,
                 duration: int = None, bucket_id: str = None,
                 prefix: str = None) -> None:
        self.payload = {
            "capabilities": capabilities,
            "keyName": encode_name(name)
        }

        if duration is not None:
            self.payload["validDurationInSeconds"] = duration
        if bucket_id is not None:
            self.payload["bucketId"] = bucket_id
        if prefix is not None:
            self.payload["namePrefix"] = prefix


class FileSettings:
    """
    Parameters
    ----------
    start_name : str, optional
        by default None
    limit : int, optional
        by default 100
    prefix : str, optional
        by default ""
    delimiter : str, optional
        by default None
    """

    def __init__(self, start_name: str = None,
                 limit: int = 100, prefix: str = "",
                 delimiter: str = None) -> None:
        self.payload = {}

        if start_name is not None:
            self.payload["startFileName"] = encode_name(
                start_name, replace=False)
        if limit is not None:
            self.payload["maxFileCount"] = limit
        if prefix is not None:
            self.payload["prefix"] = prefix
        if delimiter is not None:
            self.payload["delimiter"] = delimiter


class DownloadSettings:
    """
    Parameters
    ----------
    range : str, optional
        by default None
    disposition : str, optional
        by default None
    language : str, optional
        by default None
    expires : datetime, optional
        by default None
    cache_control : str, optional
        by default None
    encoding : str, optional
        by default None
    content_type : str, optional
        by default None
    """

    def __init__(self, range: str = None, disposition: str = None,
                 language: str = None, expires: datetime = None,
                 cache_control: str = None, encoding: str = None,
                 content_type: str = None) -> None:
        self.headers = {}
        self.parameters = {}

        if range is not None:
            self.headers["Range"] = range
        if disposition is not None:
            self.parameters["b2ContentDisposition"] = disposition
        if language is not None:
            self.parameters["b2ContentLanguage"] = language
        if expires is not None:
            self.parameters["b2Expires"] = expires.timestamp() * 1000
        if cache_control is not None:
            self.parameters["b2CacheControl"] = cache_control
        if encoding is not None:
            self.parameters["b2ContentEncoding"] = encoding
        if content_type is not None:
            self.parameters["b2ContentType"] = content_type


class UploadSettings:
    """
    Parameters
    ----------
    name : str
    content_type : str, optional
        by default "b2/x-auto"
    last_modified : datetime, optional
        by default None
    disposition : str, optional
        by default None
    language : str, optional
        by default None
    expires : datetime, optional
        by default None
    cache_control : str, optional
        by default None
    encoding : str, optional
        by default None
    custom_headers : Dict[str, str], optional
        by default None
    """

    def __init__(self, name: str, content_type: str = "b2/x-auto",
                 last_modified: datetime = None, disposition: str = None,
                 language: str = None, expires: datetime = None,
                 cache_control: str = None, encoding: str = None,
                 custom_headers: Dict[str, str] = None) -> None:

        # Needed for bucket.upload_file
        self._name = name
        self._content_type = content_type

        self.headers: Dict[str, Union[str, float]] = {
            "X-Bz-File-Name": parse.quote(encode_name(name, replace=False)),
            "Content-Type": content_type
        }

        if last_modified is not None:
            self.headers[
                "X-Bz-Info-src_last_modified_millis"
            ] = last_modified.timestamp() * 1000

        if disposition is not None:
            self.headers["X-Bz-Info-b2-content-disposition"] = disposition

        if language is not None:
            self.headers["X-Bz-Info-b2-content-language"] = language

        if expires is not None:
            self.headers["X-Bz-Info-b2-expires"] = expires.timestamp() * 1000

        if cache_control is not None:
            self.headers["X-Bz-Info-b2-cache-control"] = cache_control

        if encoding is not None:
            self.headers["X-Bz-Info-b2-content-encoding"] = encoding

        if custom_headers is not None:
            for header, value in custom_headers.items():
                self.headers["X-Bz-Info-{}".format(header)] = value


class PartSettings:
    """
    Parameters
    ----------
    name : str
    content_type : str, optional
        by default "b2/x-auto"
    last_modified : datetime, optional
        by default None
    sha1 : str, optional
        by default None
    """

    def __init__(self, name: str, content_type: str = "b2/x-auto",
                 last_modified: datetime = None, sha1: str = None) -> None:
        self.payload: Dict[str, Union[dict, str, float]] = {
            "fileName": encode_name(name, replace=False),
            "contentType": content_type
        }

        if last_modified is not None:
            self.payload["fileInfo"] = {
                "src_last_modified_millis": last_modified.timestamp() * 1000
            }

        if sha1 is not None:
            if "fileInfo" not in self.payload:
                self.payload["fileInfo"] = {
                    "large_file_sha1": sha1
                }
            else:
                self.payload["fileInfo"] = {
                    "large_file_sha1": sha1,
                    **cast(dict, self.payload["fileInfo"])
                }


class CopyFileSettings:
    """
    Parameters
    ----------
    name : str
    content_type : str, optional
        by default None
    destination_bucket_id : str, optional
        by default None
    range : str, optional
        by default None
    directive : str, optional
        by default None
    info : dict, optional
        by default None
    """

    def __init__(self, name: str, content_type: str = None,
                 destination_bucket_id: str = None, range: str = None,
                 directive: str = None, info: dict = None) -> None:
        self.payload: Dict[str, Union[str, int, dict]] = {
            "fileName": encode_name(name, replace=False),
        }

        if content_type is not None:
            self.payload["contentType"] = content_type
        if destination_bucket_id is not None:
            self.payload["destinationBucketId"] = destination_bucket_id
        if range is not None:
            self.payload["range"] = range
        if directive is not None:
            self.payload["metadataDirective"] = directive
        if info is not None:
            self.payload["fileInfo"] = info


class CopyPartSettings:
    """
    Parameters
    ----------
    file_id : str
    range : str, optional
        by default None
    """

    def __init__(self, file_id: str, range: str = None) -> None:
        self.payload: Dict[str, Union[str, int]] = {
            "largeFileId": file_id
        }

        if range is not None:
            self.payload["range"] = range
