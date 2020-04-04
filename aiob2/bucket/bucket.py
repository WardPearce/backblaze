from upload import Upload
from file import File

class Bucket(object):
    def __init__(self, bucket_id, obj):
        self.obj = obj
        self.bucket_id = bucket_id

    @property
    def upload(self):
        """ Upload object """

        return Upload(bucket_id=self.bucket_id, obj=self.obj)

    def file(self, file_name=None):
        """ File object 
                - file_name, not required.
        """

        return File(bucket_id=self.bucket_id, file_name=file_name, obj=self.obj)