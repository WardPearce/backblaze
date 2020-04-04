from .create import Create
from .list import List
from .delete import Delete

class Account(object):
    def __init__(self, obj):
        self.obj = obj

    @property
    def create(self):
        """ Create object """
        
        return Create(obj=self.obj)

    @property
    def list(self):
        """ List Object """

        return List(obj=self.obj)

    @property
    def delete(self):
        """ Delete Object """

        return Delete(obj=self.obj)