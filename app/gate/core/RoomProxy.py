# coding:utf8


class RoomProxy(object):

    def __init__(self):
        self._room_id = 0
        self._room_type = 0
        self._rounds = 0
        self._create_time = 0
        self._account_id = 0
        self._node_name = 0
        self._account_id_list = []

    def init(self, result):
        self._room_id = result.get('room_id')
        self._room_type = result.get('room_type')
        self._rounds = result.get('rounds')
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

