# coding:utf8
from app.game.core.Player import Player
from app.util.defines import status


class PlayerPoker(Player):

    def __init__(self, **kwargs):
        super(PlayerPoker, self).__init__(**kwargs)

        self._statistic_bomb_count = 0      # 本轮炸弹场数

    def get_player_save_data(self):
        return {
            'base_data': super(PlayerPoker, self)._get_player_save_base_data().items(),
            'local_data': self._get_player_save_local_data().items()
        }

    def _get_player_save_local_data(self):
        return {
            'statistic_bomb_count': self._statistic_bomb_count
        }

    def parse_player_data(self, data):
        if not data:
            return
        super(PlayerPoker, self)._parse_player_base_data(dict(data.get('base_data', [])))
        self._parse_player_local_data(dict(data.get('local_data', [])))

    def _parse_player_local_data(self, local_data):
        if not local_data:
            return
        self._statistic_bomb_count = local_data['statistic_bomb_count']

    @property
    def bomb_count(self):
        return self._statistic_bomb_count

    @bomb_count.setter
    def bomb_count(self, _count):
        self._statistic_bomb_count += _count

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
            'account_id': self.account_id,
            'point_change': self._statistic_point,
            'win_count': self._statistic_win_count,
            'lose_count': self._statistic_lose_count,
            'bomb_count': self._statistic_bomb_count,
            'max_point': self._statistic_max_point
        }
