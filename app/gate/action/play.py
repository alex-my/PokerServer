# coding:utf8
from app.gate.core.UserManager import UserManager
from app.util.common import func
from app.util.defines import rule, games


def add_play_history(account_id_list, history_data):
    user_manager = UserManager()
    room_type = history_data['room_type']
    room_help = history_data['room_help']
    all_change_point = history_data['all_change_point']       # {account_id: last_change_point, ...}
    all_change_gold = history_data['all_change_gold']
    for account_id in account_id_list:
        user = user_manager.get_user(account_id)
        if not user:
            func.log_error('[gate] add_play_history account_id: {} lost history data'.format(account_id))
            return
        change_point = all_change_point.get(account_id, 0)
        sync_game_point(user, room_type, change_point)
        if room_help == games.HELP_ONLINE_MATCH:
            gold_point = all_change_gold.get(account_id, 0)
            sync_game_gold_point(user, gold_point)
        user.add_play_history(history_data)
        func.log_info('[gate] account_id: {} get play history'.format(account_id))


def sync_game_point(user, room_type, change_point):
    if room_type in rule.GAME_LIST_POKER_PDK:
        user.poker_point = change_point
    elif room_type in rule.GAME_LIST_MAHJONG:
        user.mahjong_point = change_point
    else:
        raise KeyError('[gate] sync_game_point room_type: {} unexist'.format(room_type))


def sync_game_gold_point(user, point):
    user.gold_point = point


