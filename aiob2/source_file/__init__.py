from .copy import Copy


class SourceFile:
    def __init__(self, source_file_id):
        self.source_file_id = source_file_id

    @property
    def copy(self):
        return Copy(source_file_id=self.source_file_id)
