# coding:utf8
from app.game.core.Room import Room
from app.util.defines import games


class RoomMahjong(Room):

    def __init__(self):
        super(RoomMahjong, self).__init__()
        self._player_operators = dict()   # {account_id: [operator, ...], ...}
        self._operators = dict()          # {operator: [account_id, position], ...}
        self._craps_list = []
        self._start_position = None
        self._start_cover = True
        self._end_position = None
        self._end_cover = True
        self._maker_account_id = None

    @property
    def operators(self):
        return self._player_operators, self._operators

    @operators.setter
    def operators(self, _player_operators, _operators):
        self._player_operators, self._operators = _player_operators, _operators

    def pop_card(self):
        return self._cards.pop()

    def is_card_clear(self):
        return len(self._cards) == 0

    @property
    def craps(self):
        return self._craps_list

    @craps.setter
    def craps(self, _craps_list):
        self._craps_list = _craps_list

    @property
    def mahjong_start(self):
        return self._start_position, self._start_cover

    @mahjong_start.setter
    def mahjong_start(self, start_position, start_cover):
        self._start_position, self._start_cover = start_position, start_cover

    @property
    def mahjong_end(self):
        return self._end_position, self._end_cover

    @mahjong_end.setter
    def mahjong_end(self, end_position, end_cover):
        self._end_position, self._end_cover = end_position, end_cover

    @staticmethod
    def get_mahjong_name(card):
        return games.MAH_CONFIG.get(card, {}).get(card, card)

    def get_room_data(self, account_id):
        user_list = []
        for _player in self._players.values():
            user_list.append(_player.get_data())
        player = self.get_player(account_id)
        return {
            'user_room': user_list,
            'user_cards': player.card_list,
            'execute_account_id': self._execute_account_id,
            'last_account_id': self._last_account_id,
            'last_cards': self._last_cards,
            'user_id': self._account_id,
            'rounds': self._rounds,
            'max_rounds': self._max_rounds,
            'mahjong_start_position': self._start_position,
            'mahjong_start_cover': self._start_cover,
            'mahjong_end_position': self._end_position,
            'mahjong_end_cover': self._end_cover,
            'maker_account_id': self._maker_account_id
        }


