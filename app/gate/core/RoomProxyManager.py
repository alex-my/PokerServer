# coding:utf8
from firefly.utils.singleton import Singleton
from app.gate.gateservice import request_all_game_node
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

    @property
    def rooms(self):
        return self._rooms

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
        hold_count = 0
        calc_count = 0
        while True:
            room_id = func.random_get(100001, 999999)
            if room_id not in self._rooms:
                return room_id
            hold_count += 1
            calc_count += 1
            if calc_count == 20:
                self.clear_unvalid_room()
            elif calc_count > 2000:
                return -1

    def clear_unvalid_room(self):
        t = func.time_get()
        expire_t = t - 365 * 24 * 3600          # 玩家正常创建的房间保存1年
        online_expire_t = t - 60 * 24 * 3600    # 在线匹配房间保存2个月
        delete_id_list = []
        for room_id, room in self._rooms.iteritems():
            if not room:
                delete_id_list.append(room_id)
                continue
            if room.is_online_match() and room.create_time <= online_expire_t:
                delete_id_list.append(room_id)
            elif room.create_time <= expire_t:
                delete_id_list.append(room_id)
        # 通知game节点删除
        request_all_game_node('remove_unvalid_room', delete_id_list)
        # 本节点删除, 数据库删除
        for room_id in delete_id_list:
            try:
                sql = 'delete from {} where room_id={}'.format(dbname.DB_ROOM, room_id)
                dbexecute.execute(sql)
            except Exception as e:
                func.log_error('[gate] RoomProxyManager clear_unvalid_room db room_id: {}, failed: {}'.format(
                    room_id, e.message
                ))
            try:
                if room_id in self._rooms:
                    del self._rooms[room_id]
            except Exception as e1:
                func.log_error('[gate] RoomProxyManager clear_unvalid_room cache room_id: {}, failed: {}'.format(
                    room_id, e1.message
                ))

