class BaseBucket:
    def __init__(self, context: object, bucket_id: str) -> None:
        self.context = context
        self.bucket_id = bucket_id
