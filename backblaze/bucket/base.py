class BaseBucket:
    def __init__(self, context: object, bucket_id: str) -> None:
        self.context = context
        self.bucket_id = bucket_id


class BaseFile(BaseBucket):
    def __init__(self, file_id: str, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.file_id = file_id
