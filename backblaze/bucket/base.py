class BaseBucket:
    def __init__(self, context: object, bucket_id: str) -> None:
        self.context = context
        self.bucket_id = bucket_id


class BaseFile(BaseBucket):
    def __init__(self, context: object, bucket_id: str, file_id: str):
        super().__init__(context, bucket_id)

        self.file_id = file_id
