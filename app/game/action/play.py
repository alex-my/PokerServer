# coding:utf8
from twisted.internet import reactor
from app.game.core.PlayerManager import PlayerManager
from app.game.core.RoomManager import RoomManager
from app.game.action import send, mahjong, change, roomfull
from app.util.common import func
from app.util.defines import content, operators, origins, rule, status


def user_operator(dynamic_id, operator):
    if operator in [operators.USER_OPERATOR_READY, operators.USER_OPERATOR_SWITCH]:
        result = user_ready(dynamic_id, operator)
    elif operator == operators.USER_OPERATOR_OFFLINE:
        result = user_leave(dynamic_id, operator)
    elif operator == operators.USER_OPERATOR_CLOSE:
        result = user_close(dynamic_id, operator)
    else:
        result = False
    if result:
        send.user_operator(dynamic_id, operator)


def user_ready(dynamic_id, operator):
    account_id = PlayerManager().query_account_id(dynamic_id)
    if not account_id:
        send.system_notice(dynamic_id, content.ENTER_DYNAMIC_LOGIN_EXPIRE)
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
    func.log_info('[game] user ready room_id: {}, account_id: {}, flag: {}'.format(
        room_id, account_id, room.is_all_ready()
    ))

    if operator == operators.USER_OPERATOR_SWITCH:
        room.switch_account_id = account_id
    notice_all_room_user_operator(room, account_id, operators.USER_OPERATOR_READY)
    if room.is_all_ready():
        func.log_info('[game] all ready room_id: {}'.format(room.room_id))
        # 创建者必须在房间中
        if not room.is_online_match():
            if not check_owner_in(room):
                notice_owner_must_in(room)
                return False
        # 在线匹配需要扣除保证金
        reduce_bail_gold(room)
        # 判断是否由玩家切牌
        if check_switch(room):
            switch_cards(room)
        spend_room_per_price(room)
        dispatch_cards_to_room(room)
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
    notice_all_room_user_operator(room, account_id, operate)
    player = room.get_player(account_id)
    if player:
        player.status = operators.USER_OPERATOR_OFFLINE
    room.drop_player(account_id)
    return True


def user_close(dynamic_id, operate):
    account_id = PlayerManager().query_account_id(dynamic_id)
    if not account_id:
        send.system_notice(dynamic_id, content.ENTER_DYNAMIC_LOGIN_EXPIRE)
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
    if room.is_online_match():
        send.system_notice(dynamic_id, content.ROOM_UN_CLOSE_ONLINE_MATCH)
        return
    if not room.is_close_t_valid():
        room.clear_close()
    room.add_close_agree(account_id)
    if room.is_room_close_able():
        if room.is_creater_agree_close():
            notice_all_room_user_operator(room, account_id, operate)
            if not room.is_room_start():
                room_price = get_room_price(room)
                back_origin = get_room_close_origin(room)
                change.award_gold(room.owner_account_id, room_price, back_origin)
                func.log_info('[game] user_close account_id: {}, room_price: {}, back_origin: {}, room: {}'.format(
                    account_id, room_price, back_origin, room.get_room_brief()
                ))
            send.system_notice_room(room, content.ROOM_CLOSE_NOW)
            roomfull.remove_room(room)
        else:
            send.system_notice_room(room, content.ROOM_CLOSE_OWNER)
    elif room.is_room_close_first():
        notice_all_room_user_operator(room, account_id, operators.USER_OPERATOR_CLOSE)
    return True


def user_switch_over(dynamic_id):
    account_id = PlayerManager().query_account_id(dynamic_id)
    if not account_id:
        send.system_notice(dynamic_id, content.ENTER_DYNAMIC_LOGIN_EXPIRE)
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
    if room.is_room_dispatch_able():
        dispatch_poker_to_room(room)
        return True
    return False


def notice_all_room_user_operator(room, account_id, operator):
    dynamic_id_list = room.get_room_dynamic_id_list()
    print 'Alex notice_all_room_user_operator dynamic_id_list: ', dynamic_id_list
    send.dispatch_user_operator(account_id, operator, dynamic_id_list)


def check_owner_in(room):
    return True
    # return room.is_owner_in()


def notice_owner_must_in(room):
    dynamic_id_list = room.get_room_dynamic_id_list()
    for dynamic_id in dynamic_id_list:
        send.system_notice(dynamic_id, content.PLAY_OWNER_MUST_IN)


def check_switch(room):
    return room.switch_account_id > 0


def switch_cards(room):
    reactor.callLater(15, do_check_switch, room.room_id)
    notice_all_room_user_operator(room, room.switch_account_id, operators.USER_OPERATOR_SWITCH)


def do_check_switch(room_id):
    func.log_info('[game] do_check_switch room_id: {}'.format(room_id))
    room = RoomManager().get_room(room_id)
    if room:
        if room.room_type not in rule.GAME_LIST_POKER_PDK:
            raise KeyError('[game] do_check_switch room_id: {}, room_type: {} un do_check_switch'.format(
                room_id, room.room_type
            ))
        if room.is_room_dispatch_able():
            dispatch_poker_to_room(room)


def dispatch_cards_to_room(room):
    if room.room_type in rule.GAME_LIST_POKER_PDK:
        if not check_switch(room):
            dispatch_poker_to_room(room)
    elif room.room_type in rule.GAME_LIST_MAHJONG:
        dispatch_mahjong_to_room(room)


def dispatch_poker_to_room(room):
    func.log_info('[game] dispatch_poker_to_room')
    room.random_cards()
    room.choose_special_account_id()
    room.room_player_status(status.PLAYER_STATUS_NORMAL)
    execute_account_id = room.get_original_execute()
    room.execute_account_id = execute_account_id
    ready_list = room.room_ready_list
    for account_id in ready_list:
        player = room.get_player(account_id)
        if player:
            send.player_dispatch_cards(execute_account_id, player)


def dispatch_mahjong_to_room(room):
    func.log_info('[game] dispatch_mahjong_to_room')
    room.random_cards()
    execute_account_id = room.get_original_execute()
    room.room_player_status(status.PLAYER_STATUS_NORMAL)
    craps_1 = func.random_get(1, 6)
    craps_2 = func.random_get(1, 6)
    room.craps = [craps_1, craps_2]
    original_count = room.original_count * room.player_count
    room.mahjong_start = original_count
    room.mahjong_end = 1
    if room.rounds <= 1:
        room.maker_account_id = execute_account_id
    mahjong_craps = {
        'maker_account_id': execute_account_id,
        'craps': [craps_1, craps_2],
        'mahjong_start_num': room.mahjong_start,
        'mahjong_end_num': room.mahjong_end
    }
    ready_list = room.room_ready_list
    for account_id in ready_list:
        player = room.get_player(account_id)
        send.send_mahjong_craps(player.dynamic_id, **mahjong_craps)
        send.player_dispatch_cards(execute_account_id, player)
        if player.account_id == execute_account_id:
            mahjong.dispatch_mahjong_card(player.dynamic_id, True)


def get_room_price(room):
    room_type = room.room_type
    max_rounds = room.max_rounds
    return rule.rule_configs.get(room_type, {}).get('room_price', {}).get(max_rounds, 0)


def get_room_close_origin(room):
    room_type = room.room_type
    if room_type == rule.GAME_TYPE_PDK:
        origin = origins.ORIGIN_BACK_ROOM_PDK
    elif room_type == rule.GAME_TYPE_ZZMJ:
        origin = origins.ORIGIN_BACK_ROOM_ZZMJ
    elif room_type == rule.GAME_TYPE_PDK2:
        origin = origins.ORIGIN_BACK_ROOM_PDK2
    else:
        raise KeyError('[game] get_room_close_origin room_id: {}, room_type: {}, max_rounds: {}'.format(
            room.room_id, room_type, room.max_rounds
        ))
    return origin


def spend_room_per_price(room):
    if room.room_type in rule.GAME_LIST_POKER_PDK:
        price = rule.POKER_PER_PRICE
        origin = origins.ORIGIN_OPEN_ROOM_PDK
    elif room.room_type in rule.GAME_LIST_MAHJONG:
        price = rule.MAHJONG_PER_PRICE
        origin = origins.ORIGIN_OPEN_ROOM_ZZMJ
    else:
        raise KeyError('[game] spend_room_per_price unknown room_type: {}'.format(
            room.room_type
        ))
    for account_id in room.room_ready_list:
        change.spend_gold(account_id, price, origin)


def reduce_bail_gold(room):
    if room.is_online_match():
        for player in room.players:
            change.spend_gold(player.account_id, rule.ONLINE_MATCH_BAIL, origins.ORIGIN_ONLINE_MATCH_BAIL)
        _content = content.PLAY_ONLINE_MATCH_BAIL_REDUCE.format(rule.ONLINE_MATCH_BAIL)
        send.system_notice_room(room, _content)
