# coding:utf8
from app.gate.core.UserManager import UserManager
from app.util.common import func
from app.util.defines import rule


def add_play_history(account_id_list, history_data):
    user_manager = UserManager()
    room_type = history_data['room_type']
    all_point = history_data['all_point']       # {account_id: point, ...}
    for account_id in account_id_list:
        user = user_manager.get_user(account_id)
        if not user:
            func.log_error('[gate] add_play_history account_id: {} lost history data'.format(account_id))
            return
        point = all_point.get(account_id, 0)
        sync_game_point(user, room_type, point)
        user.add_play_history(history_data)
        func.log_info('[gate] account_id: {} get play history'.format(account_id))


def sync_game_point(user, room_type, point):
    if room_type in rule.GAME_LIST_POKER_PDK:
        user.poker_point = point
    elif room_type in rule.GAME_LIST_MAHJONG:
        user.mahjong_point = point
    else:
        raise KeyError('[gate] sync_game_point room_type: {} unexist'.format(room_type))

