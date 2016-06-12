# coding:utf8
from app.game.core.Player import Player
from app.util.common import func
from app.util.defines import status


class PlayerMahjong(Player):

    def __init__(self, **kwargs):
        super(PlayerMahjong, self).__init__(**kwargs)

        self._pong_list = []    # 碰 [[card_id, card_id, card_id], ...]
        self._kong_list = []    # 杠 [[card_id, card_id, card_id, card_id], ...]
        self._chow_list = []    # 吃 [[card_id, card_id, card_id], ...]

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
    def pre_list(self):
        return [card_id for card_id, flag in self._cards.items() if flag]

    def player_reset(self):
        self._cards = dict()
        self._pong_list = []
        self._kong_list = []
        self._chow_list = []

    def get_player_save_data(self):
        return {
            'base_data': super(PlayerMahjong, self)._get_player_save_base_data().items(),
            'local_data': self._get_player_save_local_data().items()
        }

    def _get_player_save_local_data(self):
        return {
            'pong_list': self._pong_list,
            'kong_list': self._kong_list,
            'chow_list': self._chow_list
        }

    def parse_player_data(self, data):
        if not data:
            return
        super(PlayerMahjong, self)._parse_player_base_data(dict(data.get('base_data', [])))
        self._parse_player_local_data(dict(data.get('local_data', [])))

    def _parse_player_local_data(self, local_data):
        if not local_data:
            return
        self._pong_list = local_data['pong_list']
        self._kong_list = local_data['kong_list']
        self._chow_list = local_data['chow_list']

    def get_data(self):
        card_count = self.get_card_count()
        _status = self.status
        if card_count <= 1:
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
            'status': _status,
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
            'win_count': self._statistic_win_count,
            'lose_count': self._statistic_lose_count,
            'max_point': self._statistic_max_point
        }
