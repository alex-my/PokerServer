# coding:utf8
from app.game.core.Player import Player
from app.util.common import func


class PlayerMahjong(Player):

    def __init__(self, **kwargs):
        super(PlayerMahjong, self).__init__(**kwargs)

        self._pong_list = []    # 碰 [[card_id, card_id, card_id], ...]
        self._kong_list = []    # 杠 [[card_id, card_id, card_id, card_id], ...]
        self._chow_list = []    # 吃 [[card_id, card_id, card_id], ...]
        self._pre_cards = []    # 打出的 [card_id, ...]

    def get_player_save_data(self):
        return {
            'base_data': super(PlayerMahjong, self)._get_player_save_base_data().items(),
            'local_data': self._get_player_save_local_data().items()
        }

    def _get_player_save_local_data(self):
        return {
            'pong_list': self._pong_list,
            'kong_list': self._kong_list,
            'chow_list': self._chow_list,
            'pre_cards': self._pre_cards
        }

    def parse_player_data(self, data):
        if not data:
            return
        data = func.unpack_data(data)
        super(PlayerMahjong, self)._parse_player_base_data(dict(data.get('base_data', [])))
        self._parse_player_local_data(dict(data.get('local_data', [])))

    def _parse_player_local_data(self, local_data):
        if not local_data:
            return
        self._pong_list = local_data['pong_list']
        self._kong_list = local_data['kong_list']
        self._chow_list = local_data['chow_list']
        self._pre_cards = local_data['pre_cards']

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
            'pre_cards': self._pre_cards,
            'award_cards': self.get_award_cards()
        }

    def get_award_cards(self):
        return self._pong_list + self._kong_list + self._chow_list


