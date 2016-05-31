# coding:utf8
from firefly.utils.singleton import Singleton
from app.gate.core.RoomProxy import RoomProxy
from app.util.common import func
from app.util.defines import dbname, rule
from app.util.driver import dbexecute


class RoomProxyManager:

    __metaclass__ = Singleton

    def __init__(self):
        self._rooms = dict()            # {room_id: RoomProxy, ...}
        self._user_rooms = dict()       # {account_id: {room_type: room_id, ...}, ...}
        self._rules = dict()            # {}

    def load_all_room(self):
        sql = 'select * from {}'.format(dbname.DB_ROOM)
        results = dbexecute.query_all(sql)
        if not results:
            return

        for result in results:
            room = RoomProxy()
            room.init(result)
            self.add_room(room)

    def load_configs(self):
        for game_type, conf in rule.rule_configs.iteritems():
            self._rules[game_type] = {
                'price': conf['room_price']
            }

    def add_room(self, room):
        if not room:
            return
        self._rooms[room.room_id] = room
        user_rooms = self._user_rooms.setdefault(room.account_id, {})
        user_rooms[room.room_type] = room.room_id
        self._user_rooms[room.account_id] = user_rooms

    def remove_room(self, room_id, room_type, account_id):
        if room_id in self._rooms:
            del self._rooms[room_id]
        if account_id in self._user_rooms:
            user_rooms = self._user_rooms[account_id]
            if room_type in user_rooms and user_rooms[room_type] == room_id:
                del user_rooms[room_type]

    def get_room(self, room_id):
        return self._rooms.get(room_id)

    def get_user_rooms(self, account_id):
        return self._user_rooms.get(account_id, {})

    def get_user_special_room(self, account_id, room_type):
        room_id = self.get_user_rooms(account_id).get(room_type, 0)
        if room_id > 0:
            return self.get_room(room_id)
        else:
            return None

    def get_all_rules(self):
        return self._rules

    def get_room_price(self, game_type, rounds):
        price = -1
        conf = self._rules.get(game_type)
        if conf:
            room_price = conf['price']
            price = room_price.get(rounds, -1)
        return price

    def generator_room_id(self):
        while True:
            room_id = func.random_get(100001, 999999)
            if room_id not in self._rooms:
                return room_id

