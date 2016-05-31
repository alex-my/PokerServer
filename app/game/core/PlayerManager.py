# coding:utf8
from firefly.utils.singleton import Singleton


class PlayerManager:

    __metaclass__ = Singleton

    def __init__(self):
        self._dynamic_id = dict()   # {account_id: dynamic_id, ...}
        self._account_id = dict()   # {dynamic_id: account_id, ...}

    def record_player(self, dynamic_id, account_id):
        self._dynamic_id[account_id] = dynamic_id
        self._account_id[dynamic_id] = account_id

    def query_account_id(self, dynamic_id):
        return self._account_id.get(dynamic_id)

    def query_dynamic_id(self, account_id):
        return self._dynamic_id.get(account_id)


