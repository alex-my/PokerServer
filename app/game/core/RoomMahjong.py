# coding:utf8
from app.game.core.Room import Room
from app.game.action import change
from app.util.common import func
from app.util.defines import dbname, games, status, origins, rule
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
        self._lose_account_id = 0

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

    def allow_normal_win(self):
        return self._room_help != games.HELP_MAHJONG_DRAWN

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
        if not self._cards:
            return -1
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
        if self._maker_account_id == 0:
            self._maker_account_id = self._player_list[0]
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
        self._switch_account_id = 0
        self._last_account_id = 0
        self._last_cards = []
        self._rounds += 1

        if self._maker_account_id != self._pre_win_account_id:
            next_execute_account_id = self.get_original_execute()
            self._maker_account_id = next_execute_account_id
            self._switch_account_id = self._maker_account_id

    def room_mahjong_close(self, win_status):
        all_player_info = dict()
        if win_status == games.MAH_OPERATOR_WIN:
            _point = 1
        elif win_status == games.MAH_OPERATOR_DRAWN:
            _point = 2
        else:
            _point = 0
        for account_id, player in self._players.items():
            old_point = player.point
            if account_id == self.win_account_id:
                if win_status == games.MAH_OPERATOR_DRAWN:
                    win_point = _point * 3
                else:
                    win_point = _point
                player.point_change(win_point)
                if self.is_online_match():
                    change_gold = win_point * rule.ONLINE_RATIO
                    change.award_gold(account_id, change_gold, origins.ORIGIN_ONLINE_MATCH)
                    player.last_change_gold = change_gold
                if win_status == games.MAH_OPERATOR_WIN:
                    player.win_count = 1
                else:
                    player.drawn_count = 1
            elif account_id == self.lose_account_id or win_status == games.MAH_OPERATOR_DRAWN:
                player.point_change(-_point)
                if self.is_online_match():
                    change_gold = _point * rule.ONLINE_RATIO
                    change.spend_gold(account_id, change_gold, origins.ORIGIN_ONLINE_MATCH)
                    player.last_change_gold = -change_gold
                player.lose_count = 1
                if account_id == self.lose_account_id:
                    player.help_count = 1
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
        return {'data': func.transform_object_to_pickle(self)}
