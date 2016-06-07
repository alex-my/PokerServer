# coding:utf8
from app.game.core.Room import Room
from app.util.common import func
from app.util.defines import dbname, games, status
from app.util.driver import dbexecute


class RoomMahjong(Room):

    def __init__(self):
        super(RoomMahjong, self).__init__()
        self._player_operators = dict()   # {account_id: [operator, ...], ...}
        self._operators = dict()          # {operator: [[account_id, position], ...], ...}
        self._craps_list = []
        self._start_num = 0
        self._end_num = 0
        self._maker_account_id = 0

    def get_original_execute(self):
        if self._maker_account_id == 0:
            self._maker_account_id = self._ready_list[0]
        self._execute_account_id = self._maker_account_id
        self.calc_next_execute_account_id()
        return self._execute_account_id

    @property
    def operators(self):
        return self._player_operators, self._operators

    @operators.setter
    def operators(self, operator_list):
        _player_operators, _operators = operator_list
        self._player_operators, self._operators = _player_operators, _operators

    @operators.deleter
    def operators(self):
        self._player_operators, self._operators = dict(), dict()

    def del_operators(self, account_id):
        if account_id in self._player_operators:
            del self._player_operators[account_id]
        new_operators = dict()
        for player_operator, l in self._operators.items():
            new_l = [[_account_id, _position] for _account_id, _position in l if _account_id != account_id]
            if new_l:
                new_operators[player_operator] = new_l
        self._operators = new_operators

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
        return self._start_num

    @mahjong_start.setter
    def mahjong_start(self, _num):
        self._start_num += _num

    @property
    def mahjong_end(self):
        return self._end_num

    @mahjong_end.setter
    def mahjong_end(self, _num):
        self._end_num += _num

    @property
    def maker_account_id(self):
        return self._maker_account_id

    @maker_account_id.setter
    def maker_account_id(self, _account_id):
        self._maker_account_id = _account_id

    @staticmethod
    def get_mahjong_name(card):
        return games.MAH_CONFIG.get(card, {}).get('name', card)

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
            'mahjong_start_num': self._start_num,
            'mahjong_end_num': self._end_num,
            'craps': self._craps_list,
            'maker_account_id': self._maker_account_id
        }

    def room_reset(self):
        for player in self._players.values():
            player.status = status.PLAYER_STATUS_NORMAL
            player.player_reset()

        self._start_num = 0
        self._end_num = 0

        self._ready_list = []
        self._execute_account_id = 0
        self._last_account_id = 0
        self._last_cards = []
        self._rounds += 1

    def room_point_change(self):
        # TODO: change poker to mahjong
        unit_count, player_count = self._config['unit_count'], self._config['player_count']
        card_full_count = unit_count / player_count

        all_player_info = dict()
        win_player = None
        win_point = 0
        for _account_id in self._player_list:
            _player = self.get_player(_account_id)
            left_card_count = _player.get_card_count()
            all_player_info[_player.account_id] = left_card_count
            if _account_id != self._pre_win_account_id:
                if left_card_count >= card_full_count:
                    _player.point_change(-card_full_count * 2)
                    win_point += card_full_count * 2
                elif left_card_count > 1:
                    _player.point_change(-left_card_count)
                    win_point += left_card_count
                _player.lose_count = 1
            else:
                win_player = _player
                _player.win_count = 1
        if win_player and win_point > 0:
            win_player.point_change(win_point)
        return all_player_info

    def room_save(self):
        dbexecute.update_record(
                table=dbname.DB_ROOM,
                where={'room_id': self._room_id},
                data=self.get_save_data())

    def get_save_data(self):
        data = {
            'base_data': self._get_base_save_data().items(),
            'local_data': self._get_local_data().items()
        }
        return {
            'data': func.pack_data(data)
        }

    def _get_local_data(self):
        return {
            'player_operators': self._player_operators.items(),
            'operators': self._operators.items(),
            'craps_list': self._craps_list,
            'start_num': self._start_num,
            'end_num': self._end_num,
            'make_account_id': self._maker_account_id
        }

    def _parse_data(self, data):
        if not data:
            return
        super(RoomMahjong, self)._parse_data(dict(data.get('base_data', [])))
        self._parse_local_data(dict(data.get('local_data', [])))

    def _parse_local_data(self, local_data):
        if not local_data:
            return

        player_operators = dict(local_data['player_operators'])
        self._player_operators = dict()
        for str_account_id, o_list in player_operators.items():
            self._player_operators[int(str_account_id)] = o_list

        operators = dict(local_data['operators'])
        self._operators = dict()
        for str_operator, info in operators.items():
            self._operators[int(str_operator)] = info

        self._craps_list = local_data['craps_list']
        self._start_num = int(local_data['start_num'])
        self._end_num = int(local_data['end_num'])
        self._maker_account_id = int(local_data['make_account_id'])
