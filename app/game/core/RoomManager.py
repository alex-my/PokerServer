# coding:utf8
from firefly.utils.singleton import Singleton
from app.game.core.Room import Room
from app.util.defines import dbname
from app.util.driver import dbexecute
from app.util.common import func


class RoomManager:

    __metaclass__ = Singleton

    def __init__(self):
        self._rooms = dict()            # {room_id: Room, ...}
        self._player_room = dict()      # {account_id: room_id, ...}

    def add_room(self, room):
        self._rooms[room.room_id] = room

    def drop_room(self, room):
        room_id = room.room_id
        for account_id in room.room_account_id_list:
            if account_id in self._player_room and self._player_room[account_id] == room_id:
                del self._player_room[account_id]
        if room_id in self._rooms:
            del self._rooms[room_id]

    def get_room(self, room_id):
        room = self._rooms.get(room_id)
        if not room:
            try:
                room = self.query_room_from_db(room_id)
            except Exception as e:
                room = None
                func.log_exception('[RoomManager] get_room room_id: {} do not exist, error: {}'.format(
                    room_id, e.message
                ))
        return room

    def query_room_from_db(self, room_id):
        sql = 'select * from {} where room_id={}'.format(dbname.DB_ROOM, room_id)
        result = dbexecute.query_one(sql)
        if result:
            room = Room()
            room.init(result)
            self.add_room(room)
            return room
        else:
            return None

    def add_player_room(self, account_id, room_id):
        self._player_room[account_id] = room_id

    def drop_player_room(self, account_id):
        if account_id in self._player_room:
            del self._player_room[account_id]

    def query_player_room_id(self, account_id):
        return self._player_room.get(account_id)

