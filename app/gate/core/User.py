# coding:utf8
from app.util.common import func


class User(object):

    def __init__(self, account_id=0, channel_id=0, dynamic_id=0, uuid=None):
        self._account_id = account_id
        self._dynamic_id = dynamic_id
        self._channel = 0
        self._uuid = uuid
        self._name = ''
        self._head_frame = 0
        self._head_icon = 0
        self._sex = 0
        self._room_id = 0
        self._room_type = 0
        self._gold = 0
        self._point = 0
        self._ip = ''
        self._is_lock = False   # 是否被锁定
        self._lock_expire = 0   # 锁定结束日期
        self._is_gm = False     # 是否是GM账号
        self._node_name = None  # game节点名称

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
        self._gold = data.get('gold')
        self._point = data.get('point')
        return True

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
    def gold(self):
        return self._gold

    @property
    def point(self):
        return self._point

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

    def check_gold(self, count):
        return self._gold >= count

    def spend_gold(self, count):
        self._gold -= count
        if self._gold < 0:
            self._gold = 0

    def check_point(self, count):
        return self._point >= count

    def spend_point(self, count):
        self._point -= count
        if self._point < 0:
            self._point = 0

