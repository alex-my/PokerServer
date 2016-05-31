# coding:utf8
"""
game节点
"""
from app.util.defines import constant


class ServerNode(object):

    def __init__(self, node_name):
        self._node_name = node_name         # 节点名称
        self._rooms = set()                 # 玩家user_id集合

    def add_room(self, room_id):
        self._rooms.add(room_id)

    def del_room(self, room_id):
        self._rooms.remove(room_id)

    def reset_rooms(self, rooms):
        self._rooms = rooms

    def get_all_rooms(self):
        return self._rooms

    def get_rooms_count(self):
        return len(self._rooms)

    def is_full(self):
        return self.get_rooms_count() >= constant.SERVER_ROOM_COUNT_MAX

    @property
    def node_name(self):
        return self._node_name
