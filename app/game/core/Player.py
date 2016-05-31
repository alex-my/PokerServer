# coding:utf8
"""
玩家
"""


class Player(object):

    def __init__(self, **kwargs):
        self._account_id = kwargs['account_id']
        self._room_id = kwargs['room_id']
        self._position = kwargs['position']
        self._dynamic_id = 0
        self._name = kwargs['name']
        self._head_frame = kwargs['head_frame']
        self._head_icon = kwargs['head_icon']
        self._sex = kwargs['sex']
        self._ip = kwargs['ip']
        self._point = kwargs['point']       # 总分
        self._status = 0
        self._cards = dict()                # {card: flag, ...}, flag: True 已经打出, False: 未打出

        self._statistic_point = 0           # 本轮积分变化
        self._statistic_win_count = 0       # 本轮赢的场数
        self._statistic_lose_count = 0      # 本轮输的场数
        self._statistic_bomb_count = 0      # 本轮炸弹场数
        self._statistic_max_point = 0       # 本轮单场最高积分

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
    def room_id(self):
        return self._room_id

    @room_id.setter
    def room_id(self, _id):
        self._room_id = _id

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, _position):
        self._position = _position

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
    def point(self):
        return self._point

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, _status):
        self._status = _status

    @property
    def card_list(self):
        return [card_id for card_id, flag in self._cards.items() if not flag]

    @property
    def cards(self):
        return self._cards

    @cards.setter
    def cards(self, card_list):
        self._cards = dict()
        for card_id in card_list:
            self._cards[card_id] = False

    @property
    def win_count(self):
        return self._statistic_win_count

    @win_count.setter
    def win_count(self, _count):
        self._statistic_win_count += _count

    @property
    def lose_count(self):
        return self._statistic_lose_count

    @lose_count.setter
    def lose_count(self, _count):
        self._statistic_lose_count += _count

    @property
    def bomb_count(self):
        return self._statistic_bomb_count

    @bomb_count.setter
    def bomb_count(self, _count):
        self._statistic_bomb_count += _count

    def card_publish(self, cards):
        for card_id in cards:
            self._cards[card_id] = True

    def is_card_clear(self):
        return len(self.card_list) == 0

    def get_card_count(self):
        return len(self.card_list)

    def player_reset(self):
        self._cards = dict()

    def point_change(self, _point):
        self._point += _point
        self._statistic_point += _point
        if _point > self._statistic_max_point:
            self._statistic_max_point = _point

    def get_data(self):
        return {
            'position': self.position,
            'account_id': self.account_id,
            'name': self.name,
            'head_frame': self.head_frame,
            'head_icon': self.head_icon,
            'sex': self.sex,
            'ip': self.ip,
            'point': self.point,
            'status': self.status
        }

    def is_card_few(self):
        return self.get_card_count() == 1

    def get_statistic_data(self):
        return {
            'account_id': self.account_id,
            'point_change': self._statistic_point,
            'win_count': self._statistic_win_count,
            'lose_count': self._statistic_lose_count,
            'bomb_count': self._statistic_bomb_count,
            'max_point': self._statistic_max_point
        }
