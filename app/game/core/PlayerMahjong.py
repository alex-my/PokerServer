# coding:utf8
from app.game.core.Player import Player
from app.util.common import func


class PlayerMahjong(Player):

    def __init__(self, **kwargs):
        super(PlayerMahjong, self).__init__(**kwargs)

        self._statistic_drawn_count = 0     # 自摸的场数
        self._statistic_help_count = 0      # 放炮的场数

        self._pong_list = []    # 碰 [[card_id, card_id, card_id], ...]
        self._kong_list = []    # 杠 [[card_id, card_id, card_id, card_id], ...]
        self._chow_list = []    # 吃 [[card_id, card_id, card_id], ...]
        self._others_list = []  # 其他玩家吃,碰,杠. 这样的排不能出现在己方的已经出的牌中 [card_id, ...]

    @property
    def drawn_count(self):
        raise KeyError('[game] PlayerMahjong drawn_count unable to call here')

    @drawn_count.setter
    def drawn_count(self, _count):
        self._statistic_drawn_count += _count

    @property
    def help_count(self):
        raise KeyError('[game] PlayerMahjong help_count unable to call here')

    @help_count.setter
    def help_count(self, _count):
        self._statistic_help_count += _count

    @property
    def pong_list(self):
        return self._pong_list

    @pong_list.setter
    def pong_list(self, _list):
        if _list:
            func.log_info('[game] add pong_list account_id: {}, _list: {}'.format(
                self._account_id, _list
            ))
            self._pong_list.append(_list)

    @property
    def kong_list(self):
        return self._kong_list

    @kong_list.setter
    def kong_list(self, _list):
        if _list:
            func.log_info('[game] add kong_list account_id: {}, _list: {}'.format(
                self._account_id, _list
            ))
            self._kong_list.append(_list)
            for index, _l in enumerate(self._pong_list):
                for _card_id in _l:
                    if _card_id in _list:
                        del self._pong_list[index]
                        break

    @property
    def others_list(self):
        return self._others_list

    @others_list.setter
    def others_list(self, _card_list):
        for card_id in _card_list:
            if card_id in self._cards and card_id not in self._others_list:
                self._others_list.append(card_id)

    @property
    def pre_list(self):
        return [card_id for card_id, flag in self._cards.items() if flag and card_id not in self._others_list]

    def player_reset(self):
        self._cards = dict()
        self._pong_list = []
        self._kong_list = []
        self._chow_list = []

    def _get_player_save_local_data(self):
        return {
            'pong_list': self._pong_list,
            'kong_list': self._kong_list,
            'chow_list': self._chow_list
        }

    def _parse_player_local_data(self, local_data):
        if not local_data:
            return
        self._pong_list = local_data['pong_list']
        self._kong_list = local_data['kong_list']
        self._chow_list = local_data['chow_list']

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
            'status': self.status,
            'pre_cards': self.pre_list,
            'award_cards': self.get_award_cards(),
            'card_count': self.get_card_count()
        }

    def get_award_cards(self):
        return self._pong_list + self._kong_list + self._chow_list

    def get_statistic_data(self):
        return {
            'account_id': self.account_id,
            'point_change': self._statistic_point,
            'max_point': self._statistic_max_point,
            'drawn_count': self._statistic_drawn_count,
            'win_count': self._statistic_win_count,
            'lose_count': self._statistic_lose_count,
            'help_count': self._statistic_help_count
        }

