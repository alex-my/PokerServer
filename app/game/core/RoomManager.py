# coding:utf8
from firefly.utils.singleton import Singleton
from app.game.core.RoomMahjong import RoomMahjong
from app.game.core.RoomPoker import RoomPoker
from app.util.defines import dbname, rule
from app.util.driver import dbexecute
from app.util.common import func


class RoomManager:

    __metaclass__ = Singleton

    def __init__(self):
        self._rooms = dict()            # {room_id: Room, ...}
        self._player_room = dict()      # {account_id: room_id, ...}

    @property
    def rooms(self):
        return self._rooms

    def add_room(self, room):
        self._rooms[room.room_id] = room

    def drop_room(self, room):
        room_id = room.room_id
        for account_id in room.room_account_id_list:
            if account_id in self._player_room and self._player_room[account_id] == room_id:
                del self._player_room[account_id]
        try:
            if room_id in self._rooms:
                del self._rooms[room_id]
        except Exception as e:
            func.log_error('[game] drop_room room_id: {}, failed: {}'.format(
                room_id, e.message
            ))

    def remove_rooms(self, room_id_list):
        for room_id in room_id_list:
            try:
                if room_id in self._rooms:
                    del self._rooms[room_id]
            except Exception as e:
                func.log_error('[game] remove_rooms room_id: {}, failed: {}'.format(
                    room_id, e.message
                ))

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
            room = self._create_room(result.get('room_type'))
            if room:
                room.init(result)
                self.add_room(room)
            return room
        else:
            return None

    @staticmethod
    def _create_room(room_type):
        if room_type in rule.GAME_LIST_POKER_PDK:
            room = RoomPoker()
        elif room_type in rule.GAME_LIST_MAHJONG:
            room = RoomMahjong()
        else:
            raise KeyError('[gate] RoomManager _create_room room_type: {} un exist'.format(room_type))
        return room

    def add_player_room(self, account_id, room_id):
        self._player_room[account_id] = room_id

    def drop_player_room(self, account_id):
        if account_id in self._player_room:
            del self._player_room[account_id]

    def query_player_room_id(self, account_id):
        return self._player_room.get(account_id)



