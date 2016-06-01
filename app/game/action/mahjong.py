# coding:utf8
import copy
from app.game.core.PlayerManager import PlayerManager
from app.game.core.RoomManager import RoomManager
from app.game.action import send, play
from app.util.common import func
from app.util.defines import content, games


def dispatch_mahjong_card(dynamic_id):
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
    card_id = room.pop_card()
    player.add_card(card_id)
    send.dispatch_mahjong_card(dynamic_id, card_id)


def mahjong_publish(dynamic_id, card_id):
    if not isinstance(card_id, int) or card_id <= 0 or card_id > 108:
        send.system_notice(dynamic_id, content.SYSTEM_ARGUMENT_ERROR)
        return
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
    func.log_info('[mahjong_publish] account_id: {}, dynamic_id: {}, card_id: {}, card_name: {}'.format(
            account_id, dynamic_id, card_id, room.get_mahjong_name(card_id)
    ))
    if not check_mahjong_publish_valid(player, card_id):
        send.system_notice(dynamic_id, content.PLAY_CARD_UN_VALID)
        return


def check_mahjong_publish_valid(player, card_id):
    return card_id in player.card_list


def check_mahjong_win(card_id, cards):
    card_list = [card_id] + cards
    card_list.sort()
    func.log_info('[game] check_mahjong_win card_list: {}'.format(card_list))
    # 统计
    all_card_gather = dict()

    for card_id in card_list:
        conf = games.MAH_CONFIG[card_id]
        card_gather = all_card_gather.setdefault(conf['card_type'], dict())
        card_gather[conf['card_index']] = card_gather.get(conf['card_index'], 0) + 1

    door_list = []
    for info in all_card_gather.values():
        l = [[_id, _count] for _id, _count in info.items() if _count >= 2]
        if l:
            door_list.extend(l)
    func.log_info('[game] check_mahjong_win all_card_gather: {}'.format(all_card_gather))
    func.log_info('[game] check_mahjong_win door_list: {}'.format(door_list))

    if not door_list:
        return False

    def _pre_treatment(_gather):
        def _match(match_index, match_count, _g):
            next_1_count = _g.get(match_index + 1, 0)
            next_2_count = _g.get(match_index + 2, 0)
            min_next_count = min(next_1_count, next_2_count)
            if min_next_count > 0:
                min_count = min(min_next_count, match_count)
                _g[match_index] -= min_count
                _g[match_index + 1] -= min_count
                _g[match_index + 2] -= min_count

        for _card_index, _card_count in _gather.items():
            if _card_count == 0:
                continue
            if _card_count <= 3:
                _match(_card_index, _card_count, _gather)
            elif _card_count == 4:
                _gather[_card_index] = 1
                _match(_card_index, 1, _gather)

    for door_id, _ in door_list:
        func.log_info('\n[game] check_mahjong_win \ndoor_id: {}'.format(door_id))
        all_gather = copy.deepcopy(all_card_gather)
        win_flag = True
        for _type, _card_gather in all_gather.items():
            if door_id in _card_gather:
                _card_gather[door_id] -= 2
            func.log_info('[game] check_mahjong_win _pre_treatment pre _gather: {}'.format(_card_gather))
            _pre_treatment(_card_gather)
            func.log_info('[game] check_mahjong_win _pre_treatment now _gather: {}'.format(_card_gather))
            for _c in _card_gather.values():
                if _c > 0:
                    win_flag = False
                    break
            if not win_flag:
                break
        func.log_info('[game] check_mahjong_win all_gather now: {}'.format(all_gather))
        if win_flag:
            print '[game] check_mahjong_win +++++++++++++++++ door_id: {}, door_count: {} WIN +++++++++++++++'.format(
                    door_id)
            return True
    return False


def check_mahjong_chow(card_id, card_list):
    conf = games.MAH_CONFIG[card_id]
    pre_list, next_list = conf['pre_list'], conf['next_list']
    pre_able, next_able = False, False
    for _id in card_list:
        if not pre_able and _id in pre_list:
            pre_able = True
        elif not next_able and _id in next_list:
            next_able = True
        elif next_able and pre_able:
            break
    return pre_able and next_able


def check_mahjong_pong(card_id, card_list):
    cur_list = games.MAH_CONFIG[card_id]['cur_list']
    pong_count = 0
    for _id in cur_list:
        if _id == card_id:
            continue
        if _id in card_list:
            pong_count += 1
            if pong_count >= 2:
                break
    return pong_count >= 2


def check_mahjong_dark_kong(card_id, card_list):
    cur_list = games.MAH_CONFIG[card_id]['cur_list']
    dark_kong_able = True
    for _id in cur_list:
        if _id == card_id:
            continue
        if _id not in card_list:
            dark_kong_able = False
            break
    return dark_kong_able


def check_mahjong_light_kong(card_id, card_list):
    cur_list = games.MAH_CONFIG[card_id]['cur_list']
    light_kong_able = True
    for _id in cur_list:
        if _id == card_id:
            continue
        if _id not in card_list:
            light_kong_able = False
            break
    return light_kong_able


def check_mahjong_pong_kong(card_id, all_pong_list):
    cur_list = games.MAH_CONFIG[card_id]['cur_list']
    pong_kong_able = False
    check_cur_list = [_id for _id in cur_list if _id != card_id]
    for pong_list in all_pong_list:
        if pong_list == check_cur_list:
            pong_kong_able = True
            break
    return pong_kong_able


def check_mahjong_drawn(card_id, card_list):
    return check_mahjong_win(card_id, card_list)

