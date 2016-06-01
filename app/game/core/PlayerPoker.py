# coding:utf8
from app.game.core.Player import Player


class PlayerPoker(Player):

    def __init__(self, **kwargs):
        super(PlayerPoker, self).__init__(**kwargs)

        self._statistic_bomb_count = 0      # 本轮炸弹场数

    @property
    def bomb_count(self):
        return self._statistic_bomb_count

    @bomb_count.setter
    def bomb_count(self, _count):
        self._statistic_bomb_count += _count

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
