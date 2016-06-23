# coding:utf8
from app.game.core.Room import Room
from app.game.action import change
from app.util.common import func
from app.util.defines import dbname, status, games, origins
from app.util.driver import dbexecute


class RoomPoker(Room):

    def __init__(self):
        super(RoomPoker, self).__init__()
        self._dispatch_turn = []            # 玩家出牌顺序 [account_id, ...]
        self._special_account_id = 0        # 猴子玩法中的拥有着ID

    @property
    def special_account_id(self):
        return self._special_account_id

    def choose_special_account_id(self):
        if self._room_help == games.HELP_POKER_SPECIAL:
            for player in self._players.values():
                if player.is_special_card():
                    self._special_account_id = player.account_id
                    break
        else:
            self._special_account_id = 0

    def is_special(self, account_id):
        if self._room_help == games.HELP_POKER_SPECIAL and account_id == self._special_account_id:
            return True
        return False

    @property
    def operators(self):
        return {}, {}

    def get_original_execute(self):
        if self._pre_win_account_id == 0:
            # HeiTao3
            for player in self._players.values():
                if 1 in player.card_list:
                    self._pre_win_account_id = player.account_id
                    break
        return self._pre_win_account_id

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
            'max_rounds': self._max_rounds
        }

    def room_reset(self):
        for player in self._players.values():
            player.status = status.PLAYER_STATUS_NORMAL
            player.player_reset()
        self._cards = []
        self._ready_list = []
        self._execute_account_id = 0
        self._last_account_id = 0
        self._last_cards = []
        self._switch_account_id = 0
        self._rounds += 1
        self._dispatch_turn = []

    def add_dispatch_turn(self, account_id):
        if account_id not in self._dispatch_turn:
            self._dispatch_turn.append(account_id)

    def room_point_change(self):
        unit_count, player_count = self._config['unit_count'], self._config['player_count']
        card_full_count = unit_count / player_count

        all_player_info = dict()
        win_player = None
        win_point = 0
        if self.is_special(self._pre_win_account_id):
            special_ratio = 2
        else:
            special_ratio = 1
        turn_list = self._dispatch_turn
        for _account_id in self._player_list:
            if _account_id not in turn_list:
                turn_list.append(_account_id)
            _player = self.get_player(_account_id)
            left_card_count = _player.get_card_count()
            change_point = 0
            if _account_id != self._pre_win_account_id:
                if self.is_special(_account_id):
                    special_dec_ratio = 2
                else:
                    special_dec_ratio = 1

                if left_card_count >= card_full_count:
                    full_point = card_full_count * 2 * special_ratio * special_dec_ratio
                    change_point = (-full_point)
                    win_point += full_point
                elif left_card_count > 1:
                    dec_point = left_card_count * special_ratio * special_dec_ratio
                    change_point = -dec_point
                    win_point += dec_point
                else:
                    change_point = 0
                _player.lose_count = 1
                _player.point_change(change_point)
                if self.is_online_match():
                    change.spend_gold(_account_id, -change_point, origins.ORIGIN_ONLINE_MATCH)
                    _player.last_change_gold = -change_point
            else:
                win_player = _player
                _player.win_count = 1

            all_player_info[_player.account_id] = {
                'left_card_count': left_card_count,
                'disptach_cards': _player.close_cards,
                'change_point': change_point
            }
        if win_player and win_point > 0:
            win_player.point_change(win_point)
            if self.is_online_match():
                change.award_gold(win_player.account_id, win_point, origins.ORIGIN_ONLINE_MATCH)
                win_player.last_change_gold = win_point
            info = all_player_info[win_player.account_id]
            info['change_point'] = win_point

        _info = []
        for _account_id in turn_list:
            _info.append(
                [_account_id, all_player_info[_account_id]]
            )
        return _info

    def room_save(self):
        dbexecute.update_record(
                table=dbname.DB_ROOM,
                where={'room_id': self._room_id},
                data=self.get_save_data())

    def get_save_data(self):
        return {'data': func.transform_object_to_pickle(self)}
