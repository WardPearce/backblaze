from create import Create
from list import List
from delete import Delete

class Account(object):
    def __init__(self, account_id, obj):
        self.obj = obj
        self.account_id = account_id

    @property
    def create(self):
        """ Create object """
        
        return Create(account_id=self.account_id, obj=self.obj)

    @property
    def list(self):
        """ List Object """

        return List(account_id=self.account_id, obj=self.obj)

    @property
    def delete(self):
        """ Delete Object """

        return Delete(account_id=self.account_id, obj=self.obj)