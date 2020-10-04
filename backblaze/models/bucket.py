from typing import Generator


class LifecycleModel:
    """
    Attributes
    ----------
    hiding_to_delete : int
    uploading_to_hide : int
    prefix : str
    """

    def __init__(self, data: dict) -> None:
        self.hiding_to_delete = data["daysFromHidingToDeleting"]
        self.uploading_to_hide = data["daysFromUploadingToHiding"]
        self.prefix = data["fileNamePrefix"]


class CorModel:
    """
    Attributes
    ----------
    name : str
    origins : list
    allowed_headers : list
    operations : list
    expose_headers : list
    max_age : int
    """

    def __init__(self, data: dict) -> None:
        self.name = data["corsRuleName"]
        self.origins = data["allowedOrigins"]
        self.allowed_headers = data["allowedHeaders"]
        self.operations = data["allowedOperations"]
        self.expose_headers = data["exposeHeaders"]
        self.max_age = data["maxAgeSeconds"]


class BucketModel:
    """
    Attributes
    ----------
    bucket_id : str
    name : str
    type : str
    info : str
    revision : str
    options : list
    lifecycle : list
    """

    def __init__(self, data: dict) -> None:
        self.bucket_id = data["bucketId"]
        self.name = data["bucketName"]
        self.type = data["bucketType"]
        self.info = data["bucketInfo"]
        self.revision = data["revision"]
        self.options = data["options"]
        self.lifecycle = LifecycleModel(
            data["lifecycleRules"]) if data["lifecycleRules"] else None

        self.__cors = data["corsRules"]

    def cors(self) -> Generator[CorModel, None, None]:
        """Lists cors on server.

        Yields
        -------
        CorModel
            Holds data on cors.
        """

        for cor in self.__cors:
            yield CorModel(cor)
