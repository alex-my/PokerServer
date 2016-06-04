# coding:utf8
from firefly.utils.singleton import Singleton

from app.util.common import func


class UserManager:

    __metaclass__ = Singleton

    def __init__(self):
        self._users = dict()            # {account_id: User, ...}
        self._users_dynamic = dict()    # {dynamic_id: User, ...}
        self._verify_key = dict()       # {account_id: verify_key, ...}
        self._address = dict()          # {account_id: address, ...}

    def add_user(self, user):
        account_id = user.account_id
        old_user = self.get_user(account_id)
        if old_user:
            self.drop_user(old_user)
        self._users[account_id] = user
        self._users_dynamic[user.dynamic_id] = user

    def get_all_users(self):
        return self._users

    def get_user(self, account_id):
        return self._users.get(account_id)

    def get_user_by_dynamic(self, dynamic_id):
        return self._users_dynamic.get(dynamic_id)

    def drop_user_id(self, account_id):
        user = self.get_user(account_id)
        if user:
            self.drop_user(user)

    def drop_user_dynamic(self, dynamic_id):
        user = self.get_user_by_dynamic(dynamic_id)
        if user:
            self.drop_user(user)

    def drop_user(self, user):
        if user:
            user.disconnect()
            try:
                del self._users[user.account_id]
                del self._users_dynamic[user.dynamic_id]
            except Exception as e:
                func.log_error('{}'.format(e.message), func.__function_pos__())

    def record_verify_key(self, account_id, verify_key, address):
        self._verify_key[account_id] = verify_key
        self._address[account_id] = address if address else ('', 0)

    def check_verify_key(self, account_id, verify_key):
        return verify_key is not None and self._verify_key.get(account_id) == verify_key

    def get_user_address(self, account_id):
        return self._address.get(account_id, ('', 0))
