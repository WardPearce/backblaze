class BucketTypes:
    public = "allPublic"
    private = "allPrivate"


class GetDowloadAuthModel:
    def __init__(self, data):
        self.bucket_id = data["bucketId"]
        self.file_name_prefix = data["fileNamePrefix"]
        self.authorization_token = data["authorizationToken"]


class GetUploadUrlModel:
    def __init__(self, data):
        self.bucket_id = data["bucketId"]
        self.upload_url = data["uploadUrl"]
        self.authorization_token = data["authorizationToken"]


class BucketModel:
    def __init__(self, data):
        self.account_id = data["accountId"]
        self.bucket_id = data["bucketId"]
        self.bucket_name = data["bucketName"]

        if data["bucketType"] == "allPrivate":
            self.bucket_type = BucketTypes.private
        else:
            self.bucket_type = BucketTypes.public

        self.bucket_info = data["bucketInfo"]
        self.cors_rules = data["corsRules"]
        self.lifecycle_rules = data["lifecycleRules"]
        self.revision = data["revision"]
        self.options = data["options"]
