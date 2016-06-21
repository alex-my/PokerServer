# coding:utf8
from app.game.core.Player import Player
from app.util.defines import status, games


class PlayerPoker(Player):

    def __init__(self, **kwargs):
        super(PlayerPoker, self).__init__(**kwargs)

        self._statistic_bomb_count = 0      # 本轮炸弹场数
        self._dispatch_cards = []           # 玩家出的牌 [[card_id, ...], ...]

    @property
    def bomb_count(self):
        return self._statistic_bomb_count

    @bomb_count.setter
    def bomb_count(self, _count):
        self._statistic_bomb_count += _count

    def more_bigger_bomb(self, bomb_list):
        if not bomb_list:
            return False
        bomb_index = games.POKER_CONFIG[bomb_list[0]]['card_index']
        card_list = self.card_list
        for card_id in card_list:
            conf = games.POKER_CONFIG.get(card_id)
            if not conf:
                continue
            card_index = conf['card_index']
            if card_index > bomb_index:
                cur_list = conf['cur_list']
                if self.is_all_card_in(cur_list, card_list):
                    return True
        return False

    @property
    def disptach_cards(self):
        return self._dispatch_cards

    @disptach_cards.setter
    def disptach_cards(self, card_list):
        if card_list:
            self._dispatch_cards.append(card_list)

    @property
    def close_cards(self):
        card_list = self._dispatch_cards
        card_list.append(self.card_list)
        return card_list

    @staticmethod
    def is_all_card_in(card_id_list, card_list):
        for card_id in card_id_list:
            if card_id not in card_list:
                return False
        return True

    def get_data(self):
        card_count = self.get_card_count()
        _status = self.status
        if card_count == 1:
            _status = status.PLAYER_STATUS_WARN
        return {
            'position': self.position,
            'account_id': self.account_id,
            'name': self.name,
            'head_frame': self.head_frame,
            'head_icon': self.head_icon,
            'sex': self.sex,
            'ip': self.ip,
            'point': self.point,
            'status': _status
        }

    def is_card_few(self):
        return self.get_card_count() == 1

    def get_statistic_data(self):
        return {
            'account_id': self._account_id,
            'point_change': self._statistic_point,
            'win_count': self._statistic_win_count,
            'lose_count': self._statistic_lose_count,
            'bomb_count': self._statistic_bomb_count,
            'max_point': self._statistic_max_point
        }

    def player_reset(self):
        self._cards = dict()
        self._dispatch_cards = []

    def is_special_card(self):
        special_card_id = games.POKER_SPECIAL_CARD
        return special_card_id in self._cards
