from datetime import datetime


class KeyModel:
    """
    Attributes
    ----------
    key_name : str
    application_key_id : str
    capabilities : list
    account_id : str
    expires : datetime
        Not always given, may be None.
    bucket_id : str
    name_prefix : str
    options : list
    """

    def __init__(self, data) -> None:
        self.key_name = data["keyName"]
        self.application_key_id = data["applicationKeyId"]
        self.capabilities = data["capabilities"]
        self.account_id = data["accountId"]

        if data["expirationTimestamp"]:
            self.expires = datetime.utcfromtimestamp(
                data["expirationTimestamp"] / 1000
            )
        else:
            self.expires = None

        self.bucket_id = data["bucketId"]
        self.name_prefix = data["namePrefix"]
        self.options = data["options"]
