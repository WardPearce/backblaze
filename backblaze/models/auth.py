class AllowedModel:
    """
    Attributes
    ----------
    bucket_id : str
    bucket_name : str
    capabilities : str
    prefix : str
    """

    def __init__(self, data: dict) -> None:
        self.bucket_id = data["bucketId"]
        self.bucket_name = data["bucketName"]
        self.capabilities = data["capabilities"]
        self.prefix = data["namePrefix"]


class AuthModel:
    """
    Attributes
    ----------
    minimum_part_size : int
    recommended_part_size : int
    account_id : int
    allowed : AllowedModel
    api_url : str
    authorization_token : str
    download_url : str
    """

    def __init__(self, data: dict) -> None:
        self.minimum_part_size = data["absoluteMinimumPartSize"]
        self.recommended_part_size = data["recommendedPartSize"]
        self.account_id = data["accountId"]
        self.allowed = AllowedModel(data["allowed"])
        self.api_url = data["apiUrl"]
        self.authorization_token = data["authorizationToken"]
        self.download_url = data["downloadUrl"]
