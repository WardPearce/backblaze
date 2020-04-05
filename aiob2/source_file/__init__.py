from .copy import Copy

class SourceFile(object):
    def __init__(self, source_file_id, obj):
        self.obj = obj
        self.source_file_id = source_file_id

    @property
    def copy(self):
        return Copy(source_file_id=self.source_file_id, obj=self.obj)