# coding:utf8
from app.game.gameservice import request_gate_node
from app.game.core.PlayerManager import PlayerManager
from app.game.core.RoomManager import RoomManager
from app.game.action import send, play, mahjong
from app.util.common import func
from app.util.defines import content, operators, rule, status


def enter_room(**kwargs):
    func.log_info('[game] enter_room: {}'.format(kwargs))
    dynamic_id, account_id, room_id = kwargs['dynamic_id'], kwargs['account_id'], kwargs['room_id']
    room_manager = RoomManager()
    room = room_manager.get_room(room_id)
    if not room:
        send.system_notice(dynamic_id, content.ROOM_UN_FIND)
        return
    if room.is_room_full(account_id):
        func.log_warn('[game] room: {}, user_id: {} is full'.format(room_id, account_id))
        send.system_notice(dynamic_id, content.ROOM_FULL_USER)
        return
    room.player_enter(**kwargs)
    PlayerManager().record_player(dynamic_id, account_id)
    room_manager.add_player_room(account_id, room_id)
    player_operators, all_operators = room.operators
    operator_account_id = 0
    if all_operators:
        _execute_player = room.get_player(room.execute_account_id)
        if _execute_player:
            operator_account_id = mahjong.select_mahjong_operator_account_id(
                all_operators, _execute_player.account_id, _execute_player.position)
    func.log_info('[game] enter_room dynamic_id: {}, account_id: {}, room_id: {}, operator_account_id: {}, player_operators: {}, all_operators: {}'.format(
            dynamic_id, account_id, room_id, operator_account_id, player_operators, all_operators))
    request_gate_node('enter_room_gate', account_id, dynamic_id, kwargs['_node_name'], room_id,
                      room.get_room_data(account_id), operator_account_id, player_operators)
    dynamic_id_list = room.get_room_dynamic_id_list(account_id)
    if dynamic_id_list:
        player = room.get_player(account_id)
        func.log_info('[game] enter_room, account_id: {}, dynamic_i_list: {}'.format(
            account_id, dynamic_id_list
        ))
        if room.room_type in rule.GAME_LIST_POKER_PDK:
            send.broad_player_enter_poker(dynamic_id_list, player.get_data())
        elif room.room_type in rule.GAME_LIST_MAHJONG:
            send.broad_player_enter_mahjong(dynamic_id_list, player.get_data(),
                                            operator_account_id, player_operators.get(account_id))
        else:
            raise KeyError('[game] enter_room, account_id: {}, room_id: {}, room_type: {} un exist'.format(
                account_id, room_id, room.room_type
            ))
        if room.is_all_in():
            send.broad_room_all_in(room.get_room_dynamic_id_list(), room.room_type)


def leave_room(dynamic_id):
    func.log_info('[game] leave_room dynamic_id: {}'.format(dynamic_id))
    play.user_operator(dynamic_id, operators.USER_OPERATOR_OFFLINE)


def remove_unvalid_room(delete_id_list):
    RoomManager().remove_rooms(delete_id_list)


def room_short_message(dynamic_id, message):
    account_id = PlayerManager().query_account_id(dynamic_id)
    if not account_id:
        send.system_notice(dynamic_id, content.ENTER_DYNAMIC_LOGIN_EXPIRE)
        return
    room_manager = RoomManager()
    room_id = room_manager.query_player_room_id(account_id)
    if not room_id:
        send.system_notice(dynamic_id, content.ROOM_UN_ENTER)
        return
    room = room_manager.get_room(room_id)
    if not room:
        send.system_notice(dynamic_id, content.ROOM_UN_FIND)
        return
    player = room.get_player(account_id)
    if not player:
        func.log_error('[game] room_short_message player is unvalid, account_id: {}, room_id: {}'.format(
                account_id, room_id))
        send.system_notice(dynamic_id, content.ROOM_UN_ENTER)
        return
    t = func.time_get()
    if t - player.short_message_t < 4:
        send.system_notice(dynamic_id, content.ROOM_CHAT_TO_FREQUENT)
        return
    player.short_message_t = t
    send.short_message_to_self(dynamic_id, message)
    dynamic_id_list = room.get_room_dynamic_id_list()
    send.short_message_to_all(dynamic_id_list, account_id, message)


def room_voice_message(dynamic_id, voice_url):
    account_id = PlayerManager().query_account_id(dynamic_id)
    if not account_id:
        send.system_notice(dynamic_id, content.ENTER_DYNAMIC_LOGIN_EXPIRE)
        return
    room_manager = RoomManager()
    room_id = room_manager.query_player_room_id(account_id)
    if not room_id:
        send.system_notice(dynamic_id, content.ROOM_UN_ENTER)
        return
    room = room_manager.get_room(room_id)
    if not room:
        send.system_notice(dynamic_id, content.ROOM_UN_FIND)
        return
    player = room.get_player(account_id)
    if not player:
        func.log_error('[game] room_voice_message player is unvalid, account_id: {}, room_id: {}'.format(
                account_id, room_id))
        send.system_notice(dynamic_id, content.ROOM_UN_ENTER)
        return
    t = func.time_get()
    if t - player.voice_message_t < 4:
        send.system_notice(dynamic_id, content.ROOM_CHAT_TO_FREQUENT)
        return
    player.voice_message_t = t
    send.voice_message_to_self(dynamic_id, voice_url)
    dynamic_id_list = room.get_room_dynamic_id_list()
    send.voice_message_to_all(dynamic_id_list, account_id, voice_url)


def game_heart_tick_time_out(time_out_list):
    rooms = RoomManager().rooms
    for _room in rooms.itervalues():
        exist_list = _room.is_player_in(time_out_list)
        if exist_list:
            for account_id in exist_list:
                play.notice_all_room_user_operator(_room, account_id, status.PLAYER_STATUS_BACK)


