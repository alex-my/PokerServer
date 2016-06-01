# coding:utf8
import copy
import operator
from app.game.core.PlayerManager import PlayerManager
from app.game.core.RoomManager import RoomManager
from app.game.action import send, play
from app.util.common import func
from app.util.defines import content, games


def dispatch_mahjong_card(dynamic_id):
    """
    玩家获取一张牌
    :param dynamic_id:
    :return:
    """
    account_id = PlayerManager().query_account_id(dynamic_id)
    if not account_id:
        send.system_notice(dynamic_id, content.ENTER_DYNAMIC_ID_UN_EQUAL)
        return
    dispatch_mahjong_card_account(account_id, dynamic_id)


def dispatch_mahjong_card_account(account_id, dynamic_id):
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
    operator_list = []
    card_list = player.card_list
    if check_mahjong_drawn(card_id, card_list):
        operator_list.append(games.MAH_OPERATOR_DRAWN)
    if check_mahjong_dark_kong(card_id, card_list):
        operator_list.append(games.MAH_OPERATOR_KONG_DARK)
    player.add_card(card_id)
    send.dispatch_mahjong_card(dynamic_id, card_id, operator_list)


def mahjong_publish(dynamic_id, card_id):
    """
    玩家出牌
    :param dynamic_id:
    :param card_id:
    :return:
    """
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

    player_operators = dict()
    operators = dict()

    def _add_operator_log(_account_id, _position, _operator, ops):
        _l = ops.setdefault(_operator, [])
        _l.append([_account_id, _position])

    for _player in room.players:
        if _player.account_id == account_id:
            continue
        _player_card_list = _player.card_list
        operator_list = []
        if check_mahjong_win(card_id, _player_card_list):
            operator_list.append(games.MAH_OPERATOR_WIN)
            _add_operator_log(_player.account_id, _player.position, games.MAH_OPERATOR_WIN, operators)
        # if check_mahjong_chow(card_id, _player_card_list):
        #     operator_list.append(games.MAH_OPERATOR_CHOW)
        #     _add_operator_log(_player.account_id, _player.position, games.MAH_OPERATOR_CHOW, operators)
        if check_mahjong_pong(card_id, _player_card_list):
            operator_list.append(games.MAH_OPERATOR_PONG)
            _add_operator_log(_player.account_id, _player.position, games.MAH_OPERATOR_PONG, operators)
        if check_mahjong_light_kong(card_id, _player_card_list) or check_mahjong_pong_kong(card_id, _player):
            operator_list.append(games.MAH_OPERATOR_KONG_LIGHT)
            _add_operator_log(_player.account_id, _player.position, games.MAH_OPERATOR_KONG_LIGHT, operators)
        player_operators[_player] = operator_list

    room.calc_next_execute_account_id()
    room.record_last(account_id, card_id)
    room.operators = player_operators
    # select operator_account_id
    operator_account_id = select_mahjong_operator_account_id(operators, account_id, player.position)
    send.publish_mahjong_to_self(dynamic_id)
    for _player in room.players:
        send.publish_mahjong_to_room(_player, account_id, _player.card_list, card_id,
                                     operator_account_id, player_operators.get(_player.account_id, []))


def mahjong_operator(dynamic_id, operator, cards):
    """
    玩家操作
    :param dynamic_id:
    :param operator:
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
    func.log_info('[game] mahjong_operator account_id: {}, dynamic_id: {}, operator: {}, card_list: {}'.format(
        account_id, dynamic_id, operator, card_list
    ))
    if operator == games.MAH_OPERATOR_NONE:
        mahjong_operator_none(room, player)
    elif operator == games.MAH_OPERATOR_WIN:
        mahjong_operator_win(room, player)
    elif operator == games.MAH_OPERATOR_CHOW:
        pass
    elif operator == games.MAH_OPERATOR_PONG:
        mahjong_operator_pong(room, player, card_list)
    elif operator in [games.MAH_OPERATOR_KONG_LIGHT, games.MAH_OPERATOR_KONG_DARK]:
        mahjong_operator_kong(room, player, card_list)

    send.send_mahjong_operator(dynamic_id, account_id, operator, card_list)


def select_mahjong_operator_account_id(operators, execute_account_id, execute_position):
    # TODO: select_mahjong_operator_account_id
    if games.MAH_OPERATOR_WIN in operators:
        operator_account_list = operators[games.MAH_OPERATOR_WIN]
    elif games.MAH_OPERATOR_KONG_LIGHT in operators:
        operator_account_list = operators[games.MAH_OPERATOR_KONG_LIGHT]
    elif games.MAH_OPERATOR_PONG in operators:
        operator_account_list = operators[games.MAH_OPERATOR_PONG]
    elif games.MAH_OPERATOR_CHOW in operators:
        operator_account_list = operators[games.MAH_OPERATOR_CHOW]
    else:
        operator_account_list = []

    def _check_operator(_list):
        if not _list:
            return 0
        else:
            _list.append([execute_account_id, execute_position])
            _list.sort(key=operator.itemgetter(1))
            for index, l in enumerate(_list):
                _id, _p = l
                if _id == execute_account_id:
                    if _id == _list[-1][0]:
                        _execute_id = _list[0][0]
                    else:
                        _execute_id = _list[index + 1][0]
                    return _execute_id
        return 0
    return _check_operator(operator_account_list)


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


def mahjong_operator_none(room, player):
    operators = room.operators
    room.del_operators(player)
    if operators:
        operator_account_id = select_mahjong_operator_account_id(operators, player.account_id, player.position)
        for _player in room.players:
            if _player.account_id == player.account_id:
                continue
            operator_able = _player.account_id == operator_account_id
            send.send_mahjong_operator_select(_player.dynamic_id, operator_able,
                                              operators.get(_player.account_id, []))
    else:
        _player = PlayerManager().query_dynamic_id(room.execute_account_id)
        dispatch_mahjong_card_account(_player.account_id, _player.dynamic_id)


def mahjong_operator_win(room, player):
    pass


def mahjong_operator_pong(room, player, card_list):
    pass


def mahjong_operator_kong(room, player, card_list):
    pass

