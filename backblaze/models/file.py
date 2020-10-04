from datetime import datetime


class FileModel:
    """
    Attributes
    ----------
    account_id : str
    action : str
    bucket_id : str
    content_length : int
    content_sha1 : str
    content_md5 : str
    content_type : str
    file_id : str
    file_info : str
    file_name : str
    timestamp : datetime
    """

    def __init__(self, data) -> None:
        self.account_id = data["accountId"]
        self.action = data["action"]
        self.bucket_id = data["bucketId"]
        self.content_length = data["contentLength"]
        self.content_sha1 = data["contentSha1"]
        self.content_md5 = data["contentMd5"]
        self.content_type = data["contentType"]
        self.file_id = data["fileId"]
        self.file_info = data["fileInfo"]
        self.file_name = data["fileName"]
        self.timestamp = datetime.utcfromtimestamp(
            data["uploadTimestamp"] / 1000
        )


class FileDeleteModel:
    """
    Attributes
    ----------
    file_id : str
    file_name : str
    """

    def __init__(self, data) -> None:
        self.file_id = data["fileId"]
        self.file_name = data["fileName"]


class PartModel:
    """
    Attributes
    ----------
    file_id : str
    part_number : int
    content_length : int
    content_sha1 : str
    content_md5 : str
    timestamp : datetime
    """

    def __init__(self, data) -> None:
        self.file_id = data["fileId"]
        self.part_number = data["partNumber"]
        self.content_length = data["contentLength"]
        self.content_sha1 = data["contentSha1"]
        self.content_md5 = data["contentMd5"]
        self.timestamp = datetime.utcfromtimestamp(
            data["uploadTimestamp"] / 1000
        )


class UploadUrlModel:
    """
    Attributes
    ----------
    authorization_token : str
    upload_url : str
    file_id : str
    bucket_id : str
    """

    def __init__(self, data) -> None:
        self.authorization_token = data["authorizationToken"]
        self.upload_url = data["uploadUrl"]
        self.file_id = data["fileId"] if "fileId" in data else None
        self.bucket_id = data["bucketId"] if "bucketId" in data else None


class PartCancelModel:
    """
    Attributes
    ----------
    file_id : str
    account_id : str
    bucket_id : str
    file_name : str
    """

    def __init__(self, data) -> None:
        self.file_id = data["fileId"]
        self.account_id = data["accountId"]
        self.bucket_id = data["bucketId"]
        self.file_name = data["fileName"]
