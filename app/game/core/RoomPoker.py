# coding:utf8
from app.game.core.Room import Room
from app.util.common import func
from app.util.defines import dbname, status
from app.util.driver import dbexecute


class RoomPoker(Room):

    def __init__(self):
        super(RoomPoker, self).__init__()

    @property
    def operators(self):
        return {}, {}

    def get_original_execute(self):
        return self._pre_win_account_id if self._pre_win_account_id > 0 else self._ready_list[0]

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

    def room_point_change(self):
        unit_count, player_count = self._config['unit_count'], self._config['player_count']
        card_full_count = unit_count / player_count

        all_player_info = dict()
        win_player = None
        win_point = 0
        for _account_id in self._player_list:
            _player = self.get_player(_account_id)
            left_card_count = _player.get_card_count()
            all_player_info[_player.account_id] = {
                'left_card_count': left_card_count,
                'disptach_cards': _player.close_cards
            }
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
        }
        return {
            'data': func.pack_data(data)
        }

    def _parse_data(self, data):
        if not data:
            return
        super(RoomPoker, self)._parse_data(dict(data.get('base_data', [])))

