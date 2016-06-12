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
        self._maker_account_id = 0        # 庄家帐号ID
        self._lose_account_id = 0         # 放炮的玩家帐号ID

    def get_original_execute(self):
        if self._maker_account_id == 0:
            self._maker_account_id = self._player_list[0]
        # next maker_account_id which position next to current maker_account_id
        self._execute_account_id = self._maker_account_id
        self.calc_next_execute_account_id()
        return self._execute_account_id

    @property
    def lose_account_id(self):
        return self._lose_account_id

    @lose_account_id.setter
    def lose_account_id(self, _id):
        self._lose_account_id = _id

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

        self._cards = []
        self._ready_list = []
        self._execute_account_id = 0
        self._last_account_id = 0
        self._last_cards = []
        self._rounds += 1

    def room_mahjong_close(self, win_status):
        all_player_info = dict()
        if win_status == games.MAH_OPERATOR_WIN:
            _point = 10
        elif win_status == games.MAH_OPERATOR_DRAWN:
            _point = 20
        else:
            _point = 10
        for account_id, player in self._players.items():
            old_point = player.point
            if account_id == self.win_account_id:
                player.point_change(_point)
                player.win_count = 1
            elif account_id == self.lose_account_id:
                player.point_change(-_point)
                player.lose_count = 1
            change_point = player.point - old_point
            all_player_info[account_id] = {
                'award_cards': player.get_award_cards(),
                'cards': player.card_list,
                'point_change': change_point,
                'current_point': player.point
            }
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
