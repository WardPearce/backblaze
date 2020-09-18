class AllowedModel:
    def __init__(self, data: dict) -> None:
        self.bucket_id = data["bucketId"]
        self.bucket_name = data["bucketName"]
        self.capabilities = data["capabilities"]
        self.prefix = data["namePrefix"]


class AuthModel:
    def __init__(self, data: dict) -> None:
        self.minimum_part_size = data["absoluteMinimumPartSize"]
        self.recommended_part_size = data["recommendedPartSize"]
        self.account_id = data["accountId"]
        self.allowed = AllowedModel(data["allowed"])
        self.api_url = data["apiUrl"]
        self.auth_token = data["authorizationToken"]
        self.download_url = data["downloadUrl"]
