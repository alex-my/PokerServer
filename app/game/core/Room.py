# coding:utf8
"""
房间
"""
import random
from app.game.core.PlayerManager import PlayerManager
from app.game.core.PlayerMahjong import PlayerMahjong
from app.game.core.PlayerPoker import PlayerPoker
from app.util.common import func
from app.util.defines import rule, status


class Room(object):

    def __init__(self):
        self._room_id = 0
        self._room_type = 0
        self._max_rounds = 10           # 房间允许回合数
        self._create_time = 0           # 创建时间
        self._account_id = 0            # 创建者
        self._data = dict()
        self._config = None
        self._player_list = []          # [account_id, ...]         # 进入房间的玩家
        self._ready_list = []           # [account_id, ...]
        self._players = dict()          # {account_id: Player, ...}     # 该房间的玩家对象
        self._execute_account_id = 0    # 当前执行的玩家
        self._last_account_id = 0       # 上次执行的玩家
        self._last_cards = []           # 上次执行的牌
        self._pre_win_account_id = 0    # 上次赢的玩家ID
        self._rounds = 1                # 房间回合数
        self._cards = []                # 所有牌

    def init(self, result):
        self._room_id = result.get('room_id')
        self._room_type = result.get('room_type')
        self._max_rounds = result.get('rounds')
        self._create_time = result.get('create_time')
        self._account_id = result.get('account_id')
        data = result.get('data')
        if data:
            data = func.unpack_data(data)
        else:
            data = []
        self._data = dict(data)
        self._config = rule.rule_configs[self.room_type]

    @property
    def room_id(self):
        return self._room_id

    @property
    def room_type(self):
        return self._room_type

    @property
    def owner_account_id(self):
        return self._account_id

    @property
    def room_ready_list(self):
        return self._ready_list

    @property
    def room_account_id_list(self):
        return self._player_list

    @property
    def players(self):
        return self._players.values()

    @property
    def execute_account_id(self):
        return self._execute_account_id

    @execute_account_id.setter
    def execute_account_id(self, _account_id):
        self._execute_account_id = _account_id

    @property
    def win_account_id(self):
        return self._pre_win_account_id

    @win_account_id.setter
    def win_account_id(self, _id):
        self._pre_win_account_id = _id

    @property
    def player_count(self):
        return self._config['player_count']

    @property
    def original_count(self):
        return self._config['original_count']

    @property
    def rounds(self):
        return self._rounds

    @property
    def max_rounds(self):
        return self._max_rounds

    def is_room_full(self, account_id):
        if len(self._player_list) >= self._config['player_count']:
            for _account_id in self._player_list:
                if _account_id == account_id:
                    return False
            return True
        return False

    def player_enter(self, **kwargs):
        dynamic_id, account_id = kwargs['dynamic_id'], kwargs['account_id']
        position = self.get_player_position(account_id)
        if account_id not in self._player_list:
            kwargs['position'] = position
            kwargs['room_id'] = self._room_id
            player = self._create_player(**kwargs)
            player.dynamic_id = dynamic_id
            self.add_player(player)
            self._player_list.append(account_id)
            player.status = status.PLAYER_STATUS_NORMAL
        else:
            player = self.get_player(account_id)
            if player:
                player.dynamic_id = dynamic_id
                player.room_id = self._room_id
                player.position = position
                player.status = status.PLAYER_STATUS_NORMAL

    def _create_player(self, **kwargs):
        if self._room_type == rule.GAME_TYPE_PDK:
            return PlayerPoker(**kwargs)
        elif self._room_type == rule.GAME_TYPE_ZZMJ:
            return PlayerMahjong(**kwargs)
        raise Exception('[game] Room _create_player unvalid room_type: {}'.format(self._room_type))

    def add_player(self, player):
        self._players[player.account_id] = player

    def get_player(self, account_id):
        return self._players.get(account_id)

    def get_player_position(self, account_id):
        for index, _id in enumerate(self._player_list):
            if _id == account_id:
                return index + 1
        return len(self._player_list) + 1

    def player_ready(self, account_id):
        if account_id not in self._ready_list:
            self._ready_list.append(account_id)
            player = self.get_player(account_id)
            if player:
                player.status = status.PLAYER_STATUS_READY

    def is_all_ready(self):
        return len(self._ready_list) >= self._config['player_count']

    def is_owner_in(self):
        return self._account_id in self._player_list and self._account_id in self._ready_list

    def random_cards(self):
        unit_count, player_count = self._config['unit_count'], self._config['player_count']
        un_except = self._config.get('un_except', [])
        self._cards = [_id for _id in range(1, unit_count + 1) if _id not in un_except]
        random.shuffle(self._cards)
        # dispatch to all player
        original_count = self._config['original_count']
        dispatch_list = []
        for index in xrange(player_count):
            card_list = self._cards[index * original_count: (index + 1) * original_count]
            account_id = self._ready_list[index]
            player = self.get_player(account_id)
            player.cards = card_list
            dispatch_list.extend(card_list)
        cards = [card_id for card_id in self._cards if card_id not in dispatch_list]
        self._cards = cards

    def room_player_status(self, _status):
        for player in self._players.values():
            player.status = _status

    def calc_next_execute_account_id(self):
        cur_id = self._execute_account_id
        for index, account_id in enumerate(self._player_list):
            if account_id == self._execute_account_id:
                if index == len(self._player_list) - 1:
                    self._execute_account_id = self._player_list[0]
                else:
                    self._execute_account_id = self._player_list[index + 1]
                func.log_info('[game] calc_next_execute_account_id cur_id: {}, next_id: {}, player_list: {}, index: {}'.format(
                    cur_id, self._execute_account_id, self._player_list, index
                ))
                break

    def record_last(self, account_id, cards):
        if cards:
            self._last_account_id, self._last_cards = account_id, cards

    def get_room_dynamic_id_list(self, un_expect_account_id=None):
        player_manager = PlayerManager()
        dynamic_id_list = []
        for _account_id in self._player_list:
            dynamic_id = player_manager.query_dynamic_id(_account_id)
            if un_expect_account_id and _account_id == un_expect_account_id:
                continue
            dynamic_id_list.append(dynamic_id)
        return dynamic_id_list

    def is_full_rounds(self):
        return self._rounds > self._max_rounds

    def drop_player(self, account_id):
        player = self.get_player(account_id)
        player.status = status.PLAYER_STATUS_OFFLINE
        if account_id in self._ready_list:
            self._ready_list.remove(account_id)

    def get_room_statistic(self):
        statistic_list = []
        for player in self._players.values():
            statistic_list.append(player.get_statistic_data())
        # TODO: sorted
        for info in statistic_list:
            info['rank'] = 1
        return statistic_list
