class BaseBucket:
    def __init__(self, context: object, bucket_id: str) -> None:
        self.context = context
        self.bucket_id = bucket_id


class BaseFile(BaseBucket):
    def __init__(self, file_id: str, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.file_id = file_id


class BasePart:
    def __init__(self, file: object, context: object,
                 part_number: int = 0) -> None:
        self._file = file
        self.context = context
        self.part_number = part_number
        self.sha1s = []
        self.sha1s_append = self.sha1s.append
