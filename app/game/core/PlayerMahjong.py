# coding:utf8
from app.game.core.Player import Player


class PlayerMahjong(Player):

    def __init__(self, **kwargs):
        super(PlayerMahjong, self).__init__(**kwargs)

        self._pong_list = []    # 碰 [[card_id, card_id, card_id], ...]
        self._kong_list = []    # 杠 [[card_id, card_id, card_id, card_id], ...]
        self._chow_list = []    # 吃 [[card_id, card_id, card_id], ...]
        self._pre_cards = []    # 打出的 [card_id, ...]

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


