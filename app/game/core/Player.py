# coding:utf8
"""
玩家
"""


class Player(object):

    def __init__(self, **kwargs):
        self._account_id = kwargs.get('account_id', 0)
        self._room_id = kwargs.get('room_id', 0)
        self._position = kwargs.get('position', 0)
        self._dynamic_id = 0
        self._name = kwargs.get('name', 0)
        self._head_frame = kwargs.get('head_frame', '')
        self._head_icon = kwargs.get('head_icon', '')
        self._sex = kwargs.get('sex', 0)
        self._ip = kwargs.get('ip', '')
        self._point = kwargs.get('point', 0)      # 总分
        self._status = 0
        self._cards = dict()                # {card: flag, ...}, flag: True 已经打出, False: 未打出

        self._statistic_point = 0           # 本轮积分变化
        self._statistic_win_count = 0       # 本轮赢的场数
        self._statistic_lose_count = 0      # 本轮输的场数
        self._statistic_max_point = 0       # 本轮单场最高积分

    def _get_player_save_base_data(self):
        return {
            'account_id': self._account_id,
            'room_id': self._room_id,
            'position': self._position,
            'name': self._name,
            'head_frame': self._head_frame,
            'head_icon': self._head_icon,
            'sex': self._sex,
            'point': self._point,
            'status': self._status,
            'cards': self._cards,
            'statistic_point': self._statistic_point,
            'statistic_win_count': self._statistic_win_count,
            'statistic_lose_count': self._statistic_lose_count,
            'statistic_max_point': self._statistic_max_point,
        }

    def _parse_player_base_data(self, base_data):
        if not base_data:
            return
        self._account_id = int(base_data['account_id'])
        self._room_id = int(base_data['room_id'])
        self._position = int(base_data['position'])
        self._name = base_data['name']
        self._head_frame = base_data['head_frame']
        self._head_icon = base_data['head_icon']
        self._sex = int(base_data['sex'])
        self._point = int(base_data['point'])
        self._status = int(base_data['status'])
        self._cards = base_data['cards']
        self._statistic_point = base_data['statistic_point']
        self._statistic_win_count = base_data['statistic_win_count']
        self._statistic_lose_count = base_data['statistic_lose_count']
        self._statistic_max_point = base_data['statistic_max_point']

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

    def add_card(self, card_id):
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

    def cards_publish(self, cards):
        for card_id in cards:
            self._cards[card_id] = True

    def card_publish(self, card_id):
        if card_id in self._cards:
            self._cards[card_id] = True

    def card_publish_list(self, card_id_list):
        for card_id in card_id_list:
            if card_id in self._cards:
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
