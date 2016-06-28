# coding:utf8
from app.util.common import func
from app.util.defines import games, rule


class RoomProxy(object):

    def __init__(self):
        self._room_id = 0
        self._room_type = 0
        self._room_help = 0
        self._rounds = 0
        self._create_time = 0
        self._account_id = 0
        self._node_name = 0
        self._account_id_list = []

    def init(self, result):
        self._room_id = result.get('room_id')
        self._room_type = result.get('room_type')
        self._rounds = result.get('rounds', 10)
        self._create_time = result.get('create_time')
        self._account_id = result.get('account_id')

    def create(self, room_id, room_type, rounds, account_id, create_t):
        self._room_id = room_id
        self._room_type = room_type
        self._rounds = rounds
        self._account_id = account_id
        self._create_time = create_t

    @property
    def room_id(self):
        return self._room_id

    @property
    def room_type(self):
        return self._room_type

    @property
    def room_help(self):
        return self._room_help

    @room_help.setter
    def room_help(self, _help_value):
        self._room_help = _help_value

    @property
    def room_rounds(self):
        return self._rounds

    @property
    def create_time(self):
        return self._create_time

    @property
    def account_id(self):
        return self._account_id

    @property
    def node_name(self):
        return self._node_name

    @node_name.setter
    def node_name(self, name):
        self._node_name = name

    @property
    def account_id_list(self):
        return self._account_id_list

    @account_id_list.setter
    def account_id_list(self, _id):
        if _id not in self._account_id_list:
            self._account_id_list.append(_id)

    def is_online_match(self):
        return self._room_help == games.HELP_ONLINE_MATCH

    def is_expire(self):
        return func.time_get() - self._create_time >= rule.ROOM_EXPIRE

