# coding:utf8
from app.game.gameservice import request_gate_node
from app.game.core.PlayerManager import PlayerManager
from app.game.core.RoomManager import RoomManager
from app.game.action import send, mahjong
from app.util.common import func
from app.util.defines import content, operators, rule, status


def user_operator(dynamic_id, operator):
    if operator == operators.USER_OPERATOR_READY:
        result = user_ready(dynamic_id, operator)
    elif operator == operators.USER_OPERATOR_OFFLINE:
        result = user_leave(dynamic_id, operator)
    elif operator == operators.USER_OPERATOR_CLOSE:
        result = user_close(dynamic_id, operator)
    elif operator == operators.USER_OPERATOR_SWITCH:
        result = user_switch(dynamic_id)
    else:
        result = False
    if result:
        send.user_operator(dynamic_id, operator)


def user_ready(dynamic_id, operator):
    account_id = PlayerManager().query_account_id(dynamic_id)
    if not account_id:
        send.system_notice(dynamic_id, content.ENTER_DYNAMIC_ID_UN_EQUAL)
        return False
    room_manager = RoomManager()
    room_id = room_manager.query_player_room_id(account_id)
    if not room_id:
        send.system_notice(dynamic_id, content.ROOM_UN_ENTER)
        return False
    room = room_manager.get_room(room_id)
    if not room:
        send.system_notice(dynamic_id, content.ROOM_UN_FIND)
        return False
    room.player_ready(account_id)
    if room.is_all_ready():
        func.log_info('[game] all ready room_id: {}'.format(room.room_id))
        # 创建者必须在房间中
        if not check_owner_in(room):
            notice_owner_must_in(room)
            return
        # 判断是否由玩家切牌
        if check_switch(room):
            switch_cards(room)
        dispatch_cards_to_room(room)
    notice_all_room_user_operator(room, account_id, operator)
    return True


def user_leave(dynamic_id, operate):
    account_id = PlayerManager().query_account_id(dynamic_id)
    room_manager = RoomManager()
    room_id = room_manager.query_player_room_id(account_id)
    if not room_id:
        return False
    room = room_manager.get_room(room_id)
    if not room:
        return False
    player = room.get_player(account_id)
    if player:
        player.status = operators.USER_OPERATOR_OFFLINE
    room.drop_player(account_id)
    notice_all_room_user_operator(room, account_id, operate)
    return True


def user_close(dynamic_id, operate):
    account_id = PlayerManager().query_account_id(dynamic_id)
    if not account_id:
        send.system_notice(dynamic_id, content.ENTER_DYNAMIC_ID_UN_EQUAL)
        return False
    room_manager = RoomManager()
    room_id = room_manager.query_player_room_id(account_id)
    if not room_id:
        send.system_notice(dynamic_id, content.ROOM_UN_ENTER)
        return False
    room = room_manager.get_room(room_id)
    if not room:
        send.system_notice(dynamic_id, content.ROOM_UN_FIND)
        return False
    if account_id != room.owner_account_id:
        send.system_notice(dynamic_id, content.ROOM_CLOSE_OWNER)
        return
    notice_all_room_user_operator(room, account_id, operate)
    remove_room(room)
    return True


def user_switch(dynamic_id):
    account_id = PlayerManager().query_account_id(dynamic_id)
    if not account_id:
        send.system_notice(dynamic_id, content.ENTER_DYNAMIC_ID_UN_EQUAL)
        return False
    room_manager = RoomManager()
    room_id = room_manager.query_player_room_id(account_id)
    if not room_id:
        send.system_notice(dynamic_id, content.ROOM_UN_ENTER)
        return False
    room = room_manager.get_room(room_id)
    if not room:
        send.system_notice(dynamic_id, content.ROOM_UN_FIND)
        return False
    room.switch_account_id = account_id
    return True


def notice_all_room_user_operator(room, account_id, operator):
    dynamic_id_list = room.get_room_dynamic_id_list()
    send.dispatch_user_operator(account_id, operator, dynamic_id_list)


def check_owner_in(room):
    return room.is_owner_in()


def notice_owner_must_in(room):
    dynamic_id_list = room.get_room_dynamic_id_list()
    for dynamic_id in dynamic_id_list:
        send.system_notice(dynamic_id, content.PLAY_OWNER_MUST_IN)


def check_switch(room):
    return room.switch_account_id > 0


def switch_cards(room):
    notice_all_room_user_operator(room, room.switch_account_id, operators.USER_OPERATOR_SWITCH)


def remove_room(room):
    # 从gate节点移除该房间
    request_gate_node('remove_room', room.room_id)
    # 计算本论统计信息
    statistic_list = room.get_room_statistic()
    # 将统计信息下发玩家
    dynamic_id_list = room.get_room_dynamic_id_list()
    send.send_room_full(dynamic_id_list, statistic_list)
    # 从RoomManager移除房间信息
    RoomManager().drop_room(room)


def dispatch_cards_to_room(room):
    if room.room_type == rule.GAME_TYPE_PDK:
        dispatch_poker_to_room(room)
    elif room.room_type == rule.GAME_TYPE_ZZMJ:
        dispatch_mahjong_to_room(room)


def dispatch_poker_to_room(room):
    func.log_info('[game] dispatch_poker_to_room')
    room.random_cards()
    room.room_player_status(status.PLAYER_STATUS_NORMAL)
    execute_account_id = room.get_original_execute()
    room.execute_account_id = execute_account_id
    for player in room.players:
        send.player_dispatch_cards(execute_account_id, player)


def dispatch_mahjong_to_room(room):
    func.log_info('[game] dispatch_mahjong_to_room')
    room.random_cards()
    execute_account_id = room.get_original_execute()
    room.room_player_status(status.PLAYER_STATUS_NORMAL)
    craps_1 = func.random_get(1, 6)
    craps_2 = func.random_get(1, 6)
    room.craps = [craps_1, craps_2]
    maker_player = room.get_player(execute_account_id)
    start_position, start_cover, end_position, end_cover = calc_mahjong_position(
            craps_1 + craps_2, maker_player.position)
    room.mahjong_start = start_position, start_cover
    room.mahjong_end = end_position, end_cover
    if room.rounds <= 1:
        room.maker_account_id = execute_account_id
    mahjong_craps = {
        'maker_account_id': execute_account_id,
        'craps': [craps_1, craps_2],
        'mahjong_start_position': start_position,
        'mahjong_start_cover': start_cover,
        'mahjong_end_position': end_position,
        'mahjong_end_cover': end_cover
    }
    for player in room.players:
        send.send_mahjong_craps(player.dynamic_id, **mahjong_craps)
        send.player_dispatch_cards(execute_account_id, player)
        if player.account_id == execute_account_id:
            mahjong.dispatch_mahjong_card(player.dynamic_id)


def calc_mahjong_position(craps_point, maker_position):
    # TODO: calc_mahjong_position
    return 0, 0, 0, 0
