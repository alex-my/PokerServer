# coding:utf8
from firefly.utils.singleton import Singleton

from app.util.common import func
from app.util.defines import rule


class OnlineMatchManager:

    __metaclass__ = Singleton

    def __init__(self):
        self._match_room = dict()        # {room_type: [account_id, ...], ...}

    def add_match_user(self, room_type, account_id):
        # 强制删除
        self.remove_user(account_id)
        match_list = self._match_room.setdefault(room_type, [])
        if account_id not in match_list:
            match_list.append(account_id)

    def is_match_success(self, room_type):
        match_count = len(self._match_room.get(room_type, []))
        need_count = self.get_match_need_count(room_type) - 1  # 不包括自己
        return match_count >= need_count

    @staticmethod
    def get_match_need_count(room_type):
        return rule.rule_configs.get(room_type, dict()).get('player_count', 9999999)

    def get_match_list(self, room_type):
        return self._match_room.get(room_type, [])

    def remove_match_list(self, room_type, delete_id_list):
        match_list = self.get_match_list(room_type)
        for account_id in delete_id_list:
            if account_id in match_list:
                match_list.remove(account_id)

    def remove_user(self, account_id):
        for match_list in self._match_room.values():
            if account_id in match_list:
                match_list.remove(account_id)

