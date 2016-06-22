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

        self._last_change_point = 0         # 上一次变化积分

        self._short_message_t = 0
        self._voice_message_t = 0

    @property
    def short_message_t(self):
        return self._short_message_t

    @short_message_t.setter
    def short_message_t(self, _t):
        self._short_message_t = _t

    @property
    def voice_message_t(self):
        return self._voice_message_t

    @voice_message_t.setter
    def voice_message_t(self, _t):
        self._voice_message_t = _t

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
        self._last_change_point = _point
        self._point += _point
        self._statistic_point += _point
        if _point > self._statistic_max_point:
            self._statistic_max_point = _point

    def get_per_history(self):
        return {
            'account_id': self._account_id,
            'name': self._name,
            'point_changes': self._last_change_point,
            'room_point': self._statistic_point,
            'all_point': self._point
        }

