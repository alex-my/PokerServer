# coding:utf8
from app.game.core.Player import Player


class PlayerMahjong(Player):

    def __init__(self, **kwargs):
        super(PlayerMahjong, self).__init__(**kwargs)

        self._pong_list = []



