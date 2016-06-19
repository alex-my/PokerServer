# coding:utf8
import copy
import operator
from app.game.core.PlayerManager import PlayerManager
from app.game.core.RoomManager import RoomManager
from app.game.action import send, roomfull
from app.util.common import func
from app.util.defines import content, games


def dispatch_mahjong_card(dynamic_id, from_start):
    account_id = PlayerManager().query_account_id(dynamic_id)
    if not account_id:
        send.system_notice(dynamic_id, content.ENTER_DYNAMIC_LOGIN_EXPIRE)
        return
    dispatch_mahjong_card_account(account_id, dynamic_id, from_start)


def dispatch_mahjong_card_account(account_id, dynamic_id, from_start):
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
    func.log_info('[game] dispatch_mahjong_card_account room_id: {}, room_type: {}, account_id: {}'.format(
        room_id, room.room_type, account_id
    ))
    card_id = room.pop_card()
    func.log_info('[game] dispatch_mahjong_card_account account_id: {}, card_id: {}, card_name: {}'.format(
        account_id, card_id, room.get_mahjong_name(card_id)
    ))
    calc_mahjong_next_position(room, from_start)
    operator_list = []
    card_list = player.card_list
    if check_mahjong_drawn(card_id, card_list):
        operator_list.append(games.MAH_OPERATOR_DRAWN)
    if check_mahjong_dark_kong(card_id, card_list):
        operator_list.append(games.MAH_OPERATOR_KONG_DARK)
    if check_mahjong_pong_kong(card_id, player.pong_list):
        operator_list.append(games.MAH_OPERATOR_KONG_LIGHT)
    player.add_card(card_id)
    player_operators = dict()
    all_operators = dict()
    # record operator to room
    if operator_list:
        player_operators[account_id] = operator_list
        for _operator in operator_list:
            all_operators[_operator] = [[player.account_id, player.position]]
    room.operators = (player_operators, all_operators)
    send.dispatch_mahjong_card(dynamic_id, card_id, operator_list)
    dynamic_id_list = room.get_room_dynamic_id_list()
    send.broad_mahjong_dispatch_card(dynamic_id_list, account_id)


def mahjong_publish(dynamic_id, card_id):
    if not isinstance(card_id, int) or card_id <= 0 or card_id > 108:
        send.system_notice(dynamic_id, content.SYSTEM_ARGUMENT_ERROR)
        return
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
        func.log_info('[mahjong_publish] account_id: {}, execute_account_id: {} un turn'.format(
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
    func.log_info('[mahjong_publish] account_id: {}, dynamic_id: {}, card_id: {}, card_name: {}'.format(
            account_id, dynamic_id, card_id, room.get_mahjong_name(card_id)
    ))
    if not check_mahjong_publish_valid(player, card_id):
        send.system_notice(dynamic_id, content.PLAY_CARD_UN_VALID)
        return

    player_operators = dict()   # {account_id: [operator, ...], ...}
    operators = dict()          # {operator: [[account_id, position], ...], ...}

    def _add_operator_log(_account_id, _position, _operator, ops):
        _l = ops.setdefault(_operator, [])
        _l.append([_account_id, _position])

    win_flag = False
    for _player in room.players:
        if _player.account_id == account_id:
            continue
        _player_card_list = _player.card_list
        operator_list = []
        func.log_info('[game] mahjong_publish account_id: {} check card_list: {}'.format(_player.account_id, _player_card_list))
        if check_mahjong_win(room, card_id, _player_card_list):
            win_flag = True
            operator_list.append(games.MAH_OPERATOR_WIN)
            _add_operator_log(_player.account_id, _player.position, games.MAH_OPERATOR_WIN, operators)
        # if check_mahjong_chow(card_id, _player_card_list):
        #     operator_list.append(games.MAH_OPERATOR_CHOW)
        #     _add_operator_log(_player.account_id, _player.position, games.MAH_OPERATOR_CHOW, operators)
        if check_mahjong_pong(card_id, _player_card_list):
            operator_list.append(games.MAH_OPERATOR_PONG)
            _add_operator_log(_player.account_id, _player.position, games.MAH_OPERATOR_PONG, operators)
        if check_mahjong_light_kong(card_id, _player_card_list) or check_mahjong_pong_kong(card_id, _player.pong_list):
            operator_list.append(games.MAH_OPERATOR_KONG_LIGHT)
            _add_operator_log(_player.account_id, _player.position, games.MAH_OPERATOR_KONG_LIGHT, operators)
        player_operators[_player.account_id] = operator_list

    room.record_last(account_id, [card_id])
    room.operators = (player_operators, operators)
    player.card_publish(card_id)
    # select operator_account_id
    operator_account_id = select_mahjong_operator_account_id(operators, account_id, player.position)
    send.publish_mahjong_to_self(dynamic_id)
    for _player in room.players:
        send.publish_mahjong_to_room(_player, account_id, _player.card_list, card_id,
                                     operator_account_id, player_operators.get(_player.account_id, []))
    func.log_info('[game] mahjong_publish operator_account_id: {}, player_operators: {}, operators: {}'.format(
        operator_account_id, player_operators, operators
    ))
    if not operators:
        if room.is_card_clear() and not win_flag:
            mahjong_operator_win(room, player, 0, games.MAH_OPERATOR_NO)
        else:
            dispatch_next_card(room)


def mahjong_operator(dynamic_id, player_operator, cards):
    card_list = [card_id for card_id in cards]
    func.log_info('[game] mahjong_operator player_operator: {}, card_list: {}'.format(
        player_operator, card_list
    ))
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
    player = room.get_player(account_id)
    if not player:
        send.system_notice(dynamic_id, content.ROOM_UN_ENTER)
        return
    func.log_info('[game] mahjong_operator account_id: {}, dynamic_id: {}, player_operator: {}, card_list: {}'.format(
        account_id, dynamic_id, player_operator, card_list
    ))
    last_card_id = 0
    last_cards = room.last_cards
    if last_cards:
        last_card_id = last_cards[0]
    if player_operator not in [games.MAH_OPERATOR_NONE, games.MAH_OPERATOR_WIN, games.MAH_OPERATOR_DRAWN]:
        if not card_list:
            send.system_notice(dynamic_id, content.PLAY_PLEASE_SELECT_CARD)
            return
        if last_card_id not in card_list:
            send.system_notice(dynamic_id, content.PLAY_LAST_CARD_NOT_IN)
            return
    player_operators, all_operators = room.operators
    if account_id not in player_operators:
        send.system_notice(dynamic_id, content.PLAY_OPERATOR_UN_ABLE)
        return
    operator_list = player_operators[account_id]
    if player_operator != games.MAH_OPERATOR_NONE and player_operator not in operator_list:
        send.system_notice(dynamic_id, content.PLAY_OPERATOR_NO_RIGHT)
        return
    if player_operator == games.MAH_OPERATOR_NONE:
        mahjong_operator_none(room, player)
    elif player_operator in [games.MAH_OPERATOR_WIN, games.MAH_OPERATOR_DRAWN]:
        mahjong_operator_win(room, player, last_card_id, player_operator)
    elif player_operator == games.MAH_OPERATOR_CHOW:
        raise
    elif player_operator == games.MAH_OPERATOR_PONG:
        mahjong_operator_pong(room, player, card_list, last_card_id)
    elif player_operator in [games.MAH_OPERATOR_KONG_LIGHT, games.MAH_OPERATOR_KONG_DARK]:
        mahjong_operator_kong(room, player, card_list, last_card_id, player_operator)


def select_mahjong_operator_account_id(operators, execute_account_id, execute_position):
    if not operators:
        return 0
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


def check_mahjong_win(room, card_id, cards):
    if room.allow_normal_win():
        return _check_mahjong_win(card_id, cards)
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
    return _check_mahjong_win(card_id, card_list)


def _check_mahjong_win(card_id, cards):
    card_list = [card_id] + cards
    card_list.sort()
    func.log_info('[game] _check_mahjong_win card_list: {}'.format(card_list))
    # 统计
    all_card_gather = dict()

    for card_id in card_list:
        conf = games.MAH_CONFIG[card_id]
        card_gather = all_card_gather.setdefault(conf['card_type'], dict())
        card_gather[conf['card_index']] = card_gather.get(conf['card_index'], 0) + 1

    door_list = []
    for card_type, info in all_card_gather.items():
        l = [[_id, _count, card_type] for _id, _count in info.items() if _count >= 2]
        if l:
            door_list.extend(l)
    func.log_info('[game] _check_mahjong_win all_card_gather: {}'.format(all_card_gather))
    func.log_info('[game] _check_mahjong_win door_list: {}'.format(door_list))

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

        for _card_index, _card_count in _gather.iteritems():
            if _card_count == 0:
                continue
            if _card_count <= 3:
                _match(_card_index, _card_count, _gather)
            elif _card_count == 4:
                _gather[_card_index] = 1
                _match(_card_index, 1, _gather)

    for door_id, _, door_card_type in door_list:
        func.log_info('\n[game] _check_mahjong_win door_id: {}'.format(door_id))
        all_gather = copy.deepcopy(all_card_gather)
        win_flag = True
        for _type, _card_gather in all_gather.items():
            if _type == door_card_type and door_id in _card_gather:
                _card_gather[door_id] -= 2
            func.log_info(
                '================\n[game] _check_mahjong_win _pre_treatment pre _gather: {}'.format(_card_gather))
            _pre_treatment(_card_gather)
            func.log_info('[game] _check_mahjong_win _pre_treatment now _gather: {}\n'.format(_card_gather))
            for _c in _card_gather.values():
                if _c > 0 and _c != 3:
                    win_flag = False
                    break
            if not win_flag:
                break
        func.log_info('[game] _check_mahjong_win all_gather now: {}'.format(all_gather))
        if win_flag:
            func.log_info('[game] _check_mahjong_win +++++++++++++++++ door_id: {} WIN +++++++++++++++'.format(
                door_id))
            return True
    return False


def mahjong_operator_none(room, player):
    room.del_operators(player.account_id)
    player_operators, all_operators = room.operators
    next_flag = True
    if all_operators:
        func.log_info('[game] mahjong_operator_none player_operators: {}'.format(player_operators))
        func.log_info('[game] mahjong_operator_none all_operators: {}'.format(all_operators))
        operator_account_id = select_mahjong_operator_account_id(all_operators, player.account_id, player.position)
        func.log_info('[game] mahjong_operator_none account_id: {}, position: {}, operator_account_id: {}'.format(
            player.account_id, player.position, operator_account_id
        ))
        for _account_id, operator_list in player_operators.items():
            if not operator_list:
                continue
            _player = room.get_player(_account_id)
            operator_able = _account_id == operator_account_id
            if operator_able:
                next_flag = False
            send.send_mahjong_operator_select(_player.dynamic_id, operator_able, operator_list)
    if next_flag:
        dispatch_next_card(room)
        send.send_mahjong_operator([player], player.account_id, games.MAH_OPERATOR_NONE, [])


def dispatch_next_card(room):
    room.calc_next_execute_account_id()
    # _player = PlayerManager().query_dynamic_id(room.execute_account_id)
    _player = room.get_player(room.execute_account_id)
    dispatch_mahjong_card_account(_player.account_id, _player.dynamic_id, True)


def mahjong_operator_win(room, player, last_card_id, player_operator):
    room.win_account_id = player.account_id
    if player_operator == games.MAH_OPERATOR_WIN:
        room.lose_account_id = room.last_account_id
    elif player_operator == games.MAH_OPERATOR_DRAWN:
        room.lose_account_id = player.account_id
    elif player_operator == games.MAH_OPERATOR_NO:
        room.win_account_id = 0
        room.lose_account_id = 0
    else:
        raise Exception('[game] mahjong_operator_win player_operator: {} un exist'.format(
            player_operator
        ))
    mahjong_close(room, room.win_account_id, last_card_id, player_operator)


def mahjong_operator_pong(room, player, card_list, last_card_id):
    dynamic_id_list = room.get_room_dynamic_id_list()
    player.pong_list = card_list
    player.card_publish_list(card_list)
    send.send_mahjong_operator(dynamic_id_list, player.account_id, games.MAH_OPERATOR_PONG, card_list)
    room.execute_account_id = player.account_id     # 需要出一张牌
    send.broad_mahjong_dispatch_card(dynamic_id_list, player.account_id)
    del room.operators


def mahjong_operator_kong(room, player, card_list, last_card_id, player_operator):
    dynamic_id_list = room.get_room_dynamic_id_list()
    player.kong_list = card_list
    player.card_publish_list(card_list)
    send.send_mahjong_operator(dynamic_id_list, player.account_id, player_operator, card_list)
    room.execute_account_id = player.account_id     # 需要补一张牌
    dispatch_mahjong_card_account(player.account_id, player.dynamic_id, False)
    del room.operators


def calc_mahjong_next_position(room, from_start):
    if from_start:
        room.mahjong_start = 1
    else:
        room.mahjong_end = 1


def mahjong_close(room, win_account_id, win_card_id, win_status):
    room.win_account_id = win_account_id
    # 结算本局
    all_player_info = room.room_mahjong_close(win_status)
    # 上传本局记录
    send.sync_play_history(room)
    room.room_reset()
    dynamic_id_list = room.get_room_dynamic_id_list()
    send.game_over_mahjong(win_account_id, room.lose_account_id, win_card_id, win_status, all_player_info, dynamic_id_list)
    if room.is_full_rounds():
        roomfull.remove_room(room)

