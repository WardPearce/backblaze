from datetime import datetime


class KeyModel:
    def __init__(self, data):
        self.key_name = data["keyName"]
        self.application_key_id = data["applicationKeyId"]
        self.capabilities = data["capabilities"]
        self.account_id = data["accountId"]

        if data["expirationTimestamp"]:
            self.expires = datetime.utcfromtimestamp(
                data["expirationTimestamp"] / 1000
            )
        else:
            self.expires = False

        self.bucket_id = data["bucketId"]
        self.name_prefix = data["namePrefix"]
        self.options = data["options"]
