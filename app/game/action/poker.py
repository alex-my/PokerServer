# coding:utf8
from app.game.core.PlayerManager import PlayerManager
from app.game.core.RoomManager import RoomManager
from app.game.action import send, roomfull
from app.util.common import func
from app.util.defines import content, games, status


def poker_publish(dynamic_id, cards):
    account_id = PlayerManager().query_account_id(dynamic_id)
    if not account_id:
        send.system_notice(dynamic_id, content.ENTER_DYNAMIC_LOGIN_EXPIRE)
        return
    room_manager = RoomManager()
    room_id = room_manager.query_player_room_id(account_id)
    if not room_id:
        send.system_notice(dynamic_id, content.ROOM_UN_EXIST)
        return
    room = room_manager.get_room(room_id)
    if not room:
        send.system_notice(dynamic_id, content.ROOM_UN_FIND)
        return
    if account_id != room.execute_account_id:
        func.log_info('[poker_publish] account_id: {}, execute_account_id: {} un turn'.format(
                account_id, room.execute_account_id))
        send.system_notice(dynamic_id, content.PLAY_UN_TURN)
        return
    if not room.is_all_in():
        send.system_notice(dynamic_id, content.PLAY_ALL_IN)
        return
    player = room.get_player(account_id)
    if not player:
        send.system_notice(dynamic_id, content.ROOM_UN_ENTER)
        return
    player.status_ex = status.PLAYER_STATUS_FRONT   # 冗余
    card_list = [card_id for card_id in cards]
    func.log_info('[poker_publish] account_id: {}, dynamic_id: {}, card_list: {}'.format(
        account_id, dynamic_id, card_list
    ))
    if not check_poker_publish_valid(player, card_list):
        send.system_notice(dynamic_id, content.PLAY_CARD_UN_VALID)
        return
    player.cards_publish(card_list)
    room.add_dispatch_turn(account_id)
    room.calc_next_execute_account_id()
    room.record_last(account_id, card_list)
    if player.is_card_clear():
        next_execute_id = 0
    else:
        next_execute_id = room.execute_account_id
    send.publish_poker_to_self(dynamic_id)
    for _player in room.players:
        send.publish_poker_to_room(_player.dynamic_id, account_id, next_execute_id, card_list, _player.card_list)
    if check_card_bomb(card_list):
        bomb(account_id, card_list, room)
        player.bomb_count = 1
    dynamic_id_list = room.get_room_dynamic_id_list()
    if card_list and check_card_few(player):
        card_few(account_id, player.get_card_count(), dynamic_id_list)
    player.disptach_cards = card_list
    if player.is_card_clear():
        room.win_account_id = account_id
        all_player_info = room.room_point_change()
        send.sync_play_history(room)
        room.room_reset()
        send.poker_game_over(account_id, all_player_info, dynamic_id_list)
        roomfull.back_bail_gold(room)
        if room.is_full_rounds():
            roomfull.remove_room(room)


def check_poker_publish_valid(player, cards):
    card_list = player.card_list
    for card_id in cards:
        if card_id not in card_list:
            return False
    return True


def check_card_bomb(cards):
    if cards and len(cards) == 4:
        card_id = cards[0]
        conf = games.POKER_CONFIG.get(card_id)
        if conf:
            cur_list = conf['cur_list']
            for _card_id in cards:
                if _card_id not in cur_list:
                    return False
            return True
    return False


def bomb(account_id, card_list, room):
    for _player in room.players:
        if _player.account_id == account_id:
            continue
        if _player.more_bigger_bomb(card_list):
            func.log_info('[game] bomb is return here')
            return
    if room.is_special(account_id):
        change_point = 20
    else:
        change_point = 10
    win_point = 0
    bomb_change_list = []
    for _account_id in room.room_ready_list:
        _player = room.get_player(_account_id)
        if _account_id == account_id:
            continue
        if room.is_special(_account_id):
            special_point = 2
            func.log_info('[game] bomb _account_id: {} is special'.format(_account_id))
        else:
            special_point = 1
            func.log_info('[game] bomb _account_id: {} is not special'.format(_account_id))
        total_point = change_point * special_point
        win_point += total_point
        _player.point_change(-total_point)
        bomb_change_list.append({
            'account_id': _account_id,
            'point_changes': -total_point,
            'current_point': _player.point
        })
    win_player = room.get_player(account_id)
    win_player.point_change(win_point)
    bomb_change_list.append({
        'account_id': account_id,
        'point_changes': win_point,
        'current_point': win_player.point
    })

    dynamic_id_list = room.get_room_dynamic_id_list()
    send.send_poker_bomb(bomb_change_list, dynamic_id_list)


def check_card_few(player):
    return player.is_card_few()


def card_few(account_id, card_count, dynamic_id_list):
    send.send_few_card_count(dynamic_id_list, account_id, card_count)


