from .create import Create
from .list import List

from .resources import CONFIG


class Account:
    def __init__(self, account_id):
        if account_id:
            self.account_id = account_id
        else:
            self.account_id = CONFIG.account_id

    @property
    def create(self):
        """ Create object """

        return Create(account_id=self.account_id)

    @property
    def list(self):
        """ List Object """

        return List(account_id=self.account_id)
