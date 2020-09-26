from typing import List


class CorSettings:
    payload = {}

    def __init__(self, name: str, origins: list, allowed_headers: list,
                 operations: list, expose_headers: list, max_age: int) -> None:

        self.payload["corsRuleName"] = name
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

        self.payload["bucketName"] = name
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
