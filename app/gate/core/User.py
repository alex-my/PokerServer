# coding:utf8
from app.util.common import func
from app.util.defines import dbname
from app.util.driver import dbexecute


class User(object):

    def __init__(self, account_id=0, channel_id=0, dynamic_id=0, uuid=None):
        self._account_id = account_id
        self._dynamic_id = dynamic_id
        self._channel = 0
        self._uuid = uuid
        self._name = ''
        self._head_frame = ''
        self._head_icon = ''
        self._sex = 0
        self._room_id = 0
        self._room_type = 0
        self._gold = 0
        self._proxy_id = 0
        self._month = 0
        self._month_recharge = 0
        self._all_recharge = 0
        self._month_proxy_recharge = 0
        self._all_proxy_recharge = 0
        self._point = 0                 # 废弃
        self._poker_point = 0           # 扑克总积分
        self._mahjong_point = 0         # 麻将总积分
        self._gold_point = 0            # 金币总积分
        self._ip = ''
        self._port = 0
        self._is_lock = False           # 是否被锁定
        self._lock_expire = 0           # 锁定结束日期
        self._is_gm = False             # 是否是GM账号
        self._node_name = None          # game节点名称

        self._play_history = dict()     # 游戏记录

        self._record_room_id = 0
        self._record_room_type = 0

    def init_user(self, data):
        if not data:
            return False
        self._account_id = data.get('account_id')
        self._uuid = data.get('uuid')
        self._channel = data.get('cid')
        self._is_lock = data.get('locked')
        self._lock_expire = data.get('locked_expire')
        self._name = data.get('name')
        self._head_frame = data.get('head_frame')
        self._head_icon = data.get('head_icon')
        self._sex = data.get('sex')
        self._room_id = data.get('room_id', 0)
        self._room_type = data.get('room_type', 0)
        self._gold = data.get('gold', 0)
        self._proxy_id = data.get('proxy_id', 0)
        self._month = data.get('month', 0)
        self._month_recharge = data.get('month_recharge', 0)
        self._all_recharge = data.get('all_recharge', 0)
        self._month_proxy_recharge = data.get('month_proxy_recharge', 0)
        self._all_proxy_recharge = data.get('all_proxy_recharge', 0)

        self._poker_point = data.get('poker_point', 0)
        self._mahjong_point = data.get('mahjong_point', 0)
        self._gold_point = data.get('gold_point', 0)
        return True

    def init_history(self, data):
        self._play_history = data
        self.get_play_history_list()

    @property
    def account_id(self):
        return self._account_id

    @property
    def dynamic_id(self):
        return self._dynamic_id

    @dynamic_id.setter
    def dynamic_id(self, _id):
        self._dynamic_id = _id

    @property
    def uuid(self):
        return self._uuid

    @property
    def name(self):
        return self._name

    @property
    def head_frame(self):
        return self._head_frame

    @property
    def head_icon(self):
        return self._head_icon

    @property
    def sex(self):
        return self._sex

    @property
    def ip(self):
        return self._ip

    @property
    def room_id(self):
        return self._room_id

    @room_id.setter
    def room_id(self, _id):
        self._room_id = _id

    @property
    def room_type(self):
        return self._room_type

    @room_type.setter
    def room_type(self, _type):
        self._room_type = _type

    @property
    def record_room_id(self):
        return self._record_room_id

    @record_room_id.setter
    def record_room_id(self, _id):
        self._record_room_id = _id

    @property
    def record_room_type(self):
        return self._record_room_type

    @record_room_type.setter
    def record_room_type(self, _type):
        self._record_room_type = _type

    @property
    def gold(self):
        return self._gold

    @property
    def proxy_id(self):
        return self._proxy_id

    @proxy_id.setter
    def proxy_id(self, _proxy_id):
        self._proxy_id = _proxy_id

    @property
    def month(self):
        return self._month

    @month.setter
    def month(self, _month):
        self._month = _month

    @property
    def month_recharge(self):
        return self._month_recharge

    @month_recharge.setter
    def month_recharge(self, _value):
        self._month_recharge += _value

    @property
    def all_recharge(self):
        return self._all_recharge

    @all_recharge.setter
    def all_recharge(self, _value):
        self._all_recharge += _value

    @property
    def month_proxy_recharge(self):
        return self._month_proxy_recharge

    @month_proxy_recharge.setter
    def month_proxy_recharge(self, _value):
        self._month_proxy_recharge += _value

    @property
    def all_proxy_recharge(self):
        return self._all_proxy_recharge

    @all_proxy_recharge.setter
    def all_proxy_recharge(self, _value):
        self._all_proxy_recharge += _value

    @property
    def point(self):
        return self._point

    @property
    def poker_point(self):
        return self._poker_point

    @poker_point.setter
    def poker_point(self, _point):
        self._poker_point += _point

    @property
    def mahjong_point(self):
        return self._mahjong_point

    @mahjong_point.setter
    def mahjong_point(self, _point):
        self._mahjong_point += _point

    @property
    def gold_point(self):
        return self._gold_point

    @gold_point.setter
    def gold_point(self, _point):
        self._gold_point += _point

    def disconnect(self):
        pass

    def is_lock(self):
        # TODO: 时间验证
        return self._is_lock

    def is_lock_forever(self):
        return self._is_lock

    @property
    def lock_expire(self):
        return func.time_to_stamp(self._lock_expire)

    @lock_expire.setter
    def lock_expire(self, t):
        self._lock_expire = t

    @property
    def node_name(self):
        return self._node_name

    @node_name.setter
    def node_name(self, name):
        self._node_name = name

    def sync_information(self, **kwargs):
        if kwargs.get('name'):
            self._name = kwargs.get('name')
        if kwargs.get('sex'):
            self._sex = kwargs.get('sex')
        if kwargs.get('head_frame'):
            self._head_frame = kwargs.get('head_frame')
        if kwargs.get('head_icon'):
            self._head_icon = kwargs.get('head_icon')

    def record_address(self, _address):
        self._ip, self._port = _address if _address else ('', 0)

    def check_gold(self, count):
        return self._gold >= count

    def award_gold(self, count):
        self._gold += count
        if self._gold >= 999999999:
            self._gold = 999999999

    def spend_gold(self, count):
        self._gold -= count
        if self._gold < 0:
            self._gold = 0

    def check_point(self, count):
        return self._point >= count

    def award_point(self, count):
        self._point += count
        if self._point >= 999999999:
            self._point = 999999999

    def spend_point(self, count):
        self._point -= count
        if self._point < 0:
            self._point = 0

    def add_play_history(self, history_data):
        history_list = self._play_history.setdefault('history_list', [])
        history_list.append(history_data)

    def get_play_history_list(self):
        history_list = self._play_history.get('history_list', [])
        if len(history_list) > 100:
            history_list = history_list[len(history_list) / 2:]
            self._play_history['history_list'] = history_list
        return history_list

    def user_lost(self):
        self._room_id = self._record_room_id
        self._room_type = self._record_room_type

    def user_save(self):
        # DB_ACCOUNT
        dbexecute.update_record(
            table=dbname.DB_ACCOUNT,
            where={'account_id': self._account_id},
            data=self.get_save_data())
        # DB_HISTORY
        dbexecute.update_record(
            table=dbname.DB_HISTORY,
            where={'account_id': self._account_id},
            data=self.get_history_data()
        )

    def get_save_data(self):
        return {
            'name': self._name,
            'head_frame': self._head_frame,
            'head_icon': self._head_icon,
            'room_id': self._room_id,
            'room_type': self._room_type,
            'gold': self._gold,
            'proxy_id': self._proxy_id,
            'month': self._month,
            'month_recharge': self._month_recharge,
            'all_recharge': self._all_recharge,
            'month_proxy_recharge': self._month_proxy_recharge,
            'all_proxy_recharge': self._all_proxy_recharge,
            'poker_point': self._poker_point,
            'gold_point': self._gold_point,
            'mahjong_point': self._mahjong_point
        }

    def get_history_data(self):
        return {
            'data': func.transform_object_to_pickle(self._play_history)
        }

