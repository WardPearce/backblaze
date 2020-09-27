from datetime import datetime


class FileModel:
    def __init__(self, data):
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
    def __init__(self, data):
        self.file_id = data["fileId"]
        self.file_name = data["fileName"]


class PartModel:
    def __init__(self, data):
        self.file_id = data["fileId"]
        self.part_number = data["partNumber"]
        self.content_length = data["contentLength"]
        self.content_sha1 = data["contentSha1"]
        self.content_md5 = data["contentMd5"]
        self.timestamp = datetime.utcfromtimestamp(
            data["uploadTimestamp"] / 1000
        )


class UploadUrlModel:
    def __init__(self, data):
        self.authorization_token = data["authorizationToken"]
        self.file_id = data["fileId"]
        self.upload_url = data["uploadUrl"]


class PartDeleteModel:
    def __init__(self, data):
        self.file_id = data["fileId"]
        self.account_id = data["accountId"]
        self.bucket_id = data["bucketId"]
        self.file_name = data["fileName"]
