# coding:utf8
from app.game.core.PlayerManager import PlayerManager
from app.game.core.RoomManager import RoomManager
from app.game.action import send, play
from app.util.common import func
from app.util.defines import content


def poker_publish(dynamic_id, cards):
    """
    玩家出牌
    :param dynamic_id:
    :param cards:
    :return:
    """
    account_id = PlayerManager().query_account_id(dynamic_id)
    if not account_id:
        send.system_notice(dynamic_id, content.ENTER_DYNAMIC_ID_UN_EQUAL)
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
    player = room.get_player(account_id)
    if not player:
        send.system_notice(dynamic_id, content.ROOM_UN_ENTER)
        return
    card_list = [card_id for card_id in cards]
    func.log_info('[poker_publish] account_id: {}, dynamic_id: {}, card_list: {}'.format(
        account_id, dynamic_id, card_list
    ))
    if not check_poker_publish_valid(player, card_list):
        send.system_notice(dynamic_id, content.PLAY_CARD_UN_VALID)
        return
    player.cards_publish(card_list)
    room.calc_next_execute_account_id()
    room.record_last(account_id, card_list)
    # 判断牌局是否结束
    if player.is_card_clear():
        next_execute_id = 0
    else:
        next_execute_id = room.execute_account_id
    send.publish_poker_to_self(dynamic_id)
    for _player in room.players:
        send.publish_poker_to_room(_player.dynamic_id, account_id, next_execute_id, card_list, _player.card_list)
    # 判断是否有炸弹
    if check_card_bomb(card_list):
        bomb(account_id, room)
        player.bomb_count = 1
    dynamic_id_list = room.get_room_dynamic_id_list()
    # 判断牌是否少量(需要提醒其他玩家)
    if card_list and check_card_few(player):
        card_few(account_id, player.get_card_count(), dynamic_id_list)
    # 牌局结束处理
    if player.is_card_clear():
        room.win_account_id = account_id
        all_player_info = room.room_point_change()
        room.room_reset()
        send.game_over(account_id, all_player_info, dynamic_id_list)
        # 判断该房间是否失效(达到可玩的局数上限)
        if room.is_full_rounds():
            play.remove_room(room)


def check_poker_publish_valid(player, cards):
    card_list = player.card_list
    for card_id in cards:
        if card_id not in card_list:
            return False
    # TODO: 不能小于上次
    return True


def check_card_bomb(cards):
    if cards and len(cards) == 4 and cards.count(cards[0]) == 4:
        return True
    return False


def bomb(account_id, room):
    change_point = 10
    for _account_id in room.room_ready_list:
        _player = room.get_player(_account_id)
        if _account_id == account_id:
            _player.point_change(change_point * (room.player_count - 1))
        else:
            _player.point_change(-change_point)
    dynamic_id_list = room.get_room_dynamic_id_list()
    send.send_poker_bomb(account_id, change_point, dynamic_id_list)


def check_card_few(player):
    return player.is_card_few()


def card_few(account_id, card_count, dynamic_id_list):
    send.send_few_card_count(dynamic_id_list, account_id, card_count)


