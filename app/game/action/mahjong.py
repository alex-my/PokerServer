# coding:utf8
import copy
import operator
from app.game.core.PlayerManager import PlayerManager
from app.game.core.RoomManager import RoomManager
from app.game.action import send, roomfull
from app.util.common import func
from app.util.defines import content, games, status


def dispatch_mahjong_card(dynamic_id, from_start):
    account_id = PlayerManager().query_account_id(dynamic_id)
    if not account_id:
        func.log_error('[game] dispatch_mahjong_card ENTER_DYNAMIC_LOGIN_EXPIRE, dynamic_id: {}'.format(
                dynamic_id))
        send.system_notice(dynamic_id, content.ENTER_DYNAMIC_LOGIN_EXPIRE)
        return
    dispatch_mahjong_card_account(account_id, dynamic_id, from_start)


def dispatch_mahjong_card_account(account_id, dynamic_id, from_start):
    room_manager = RoomManager()
    room_id = room_manager.query_player_room_id(account_id)
    if not room_id:
        func.log_error('[game] dispatch_mahjong_card_account ROOM_UN_EXIST, account_id: {}'.format(
                account_id))
        send.system_notice(dynamic_id, content.ROOM_UN_EXIST)
        return
    room = room_manager.get_room(room_id)
    if not room:
        func.log_error('[game] dispatch_mahjong_card_account ROOM_UN_FIND, account_id: {}, room_id: {}'.format(
                account_id, room_id))
        send.system_notice(dynamic_id, content.ROOM_UN_FIND)
        return
    player = room.get_player(account_id)
    if not player:
        func.log_error('[game] dispatch_mahjong_card_account ROOM_UN_ENTER, account_id: {}, room_id: {}'.format(
                account_id, room_id))
        send.system_notice(dynamic_id, content.ROOM_UN_ENTER)
        return
    func.log_info('[game] dispatch_mahjong_card_account room_id: {}, room_type: {}, account_id: {}'.format(
        room_id, room.room_type, account_id
    ))
    card_id = room.pop_card()
    if card_id == -1:
        mahjong_operator_win(room, player, 0, games.MAH_OPERATOR_NO)
        return
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
        operator_list.append(games.MAH_OPERATOR_KONG_PONG_SELF)
    player.add_card(card_id)
    player_operators = dict()
    all_operators = dict()
    # record operator to room
    if operator_list:
        player_operators[account_id] = operator_list
        for _operator in operator_list:
            all_operators[_operator] = [[player.account_id, player.position]]
        func.log_info('[game] dispatch_mahjong_card_account account_id: {}, player_operators: {}, all_operators: {}'.format(
            account_id, player_operators, all_operators
        ))
    room.operators = (player_operators, all_operators)
    func.log_info('[game] dispatch_mahjong_card_account account_id: {}, card_id: {}'.format(account_id, card_id))
    player.last_dispatch_card_id = card_id
    send.dispatch_mahjong_card(dynamic_id, card_id, operator_list)
    dynamic_id_list = room.get_room_dynamic_id_list()
    send.broad_mahjong_dispatch_card(dynamic_id_list, account_id)


def mahjong_publish(dynamic_id, card_id):
    if not isinstance(card_id, int) or card_id <= 0 or card_id > 108:
        func.log_error('[game] mahjong_publish SYSTEM_ARGUMENT_ERROR, dynamic_id: {}, card_id: {}'.format(
                dynamic_id, card_id))
        send.system_notice(dynamic_id, content.SYSTEM_ARGUMENT_ERROR)
        return
    account_id = PlayerManager().query_account_id(dynamic_id)
    if not account_id:
        func.log_error('[game] mahjong_publish ENTER_DYNAMIC_LOGIN_EXPIRE, dynamic_id: {}, card_id: {}'.format(
                dynamic_id, card_id))
        send.system_notice(dynamic_id, content.ENTER_DYNAMIC_LOGIN_EXPIRE)
        return
    room_manager = RoomManager()
    room_id = room_manager.query_player_room_id(account_id)
    if not room_id:
        func.log_error('[game] mahjong_publish ROOM_UN_EXIST, account_id: {}, card_id: {}'.format(
                account_id, card_id))
        send.system_notice(dynamic_id, content.ROOM_UN_EXIST)
        return
    room = room_manager.get_room(room_id)
    if not room:
        send.system_notice(dynamic_id, content.ROOM_UN_FIND)
        return
    if account_id != room.execute_account_id:
        func.log_error('[game] mahjong_publish PLAY_UN_TURN, account_id: {}, execute_account_id: {}, card_id: {}'.format(
                account_id, room.execute_account_id, card_id))
        send.system_notice(dynamic_id, content.PLAY_UN_TURN)
        return
    if not room.is_all_in():
        func.log_error('[game] mahjong_publish PLAY_ALL_IN, account_id: {}, card_id: {}, room_id: {}'.format(
                account_id, card_id, room_id))
        send.system_notice(dynamic_id, content.PLAY_ALL_IN)
        return
    player = room.get_player(account_id)
    if not player:
        func.log_error('[game] mahjong_publish ROOM_UN_ENTER, account_id: {}, card_id: {}, room_id: {}'.format(
                account_id, card_id, room_id))
        send.system_notice(dynamic_id, content.ROOM_UN_ENTER)
        return
    func.log_info('[mahjong_publish] account_id: {}, dynamic_id: {}, card_id: {}, card_name: {}'.format(
            account_id, dynamic_id, card_id, room.get_mahjong_name(card_id)
    ))
    if not check_mahjong_publish_valid(player, card_id):
        func.log_error('[game] mahjong_publish PLAY_CARD_UN_VALID, account_id: {}, card_id: {}, card_list: {}'.format(
                account_id, card_id, player.card_list))
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
        func.log_info('-' * 50)
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
        if check_mahjong_light_kong(card_id, _player_card_list):
            operator_list.append(games.MAH_OPERATOR_KONG_LIGHT)
            _add_operator_log(_player.account_id, _player.position, games.MAH_OPERATOR_KONG_LIGHT, operators)
        if check_mahjong_pong_kong(card_id, _player.pong_list):
            operator_list.append(games.MAH_OPERATOR_KONG_PONG_OTHER)
            _add_operator_log(_player.account_id, _player.position, games.MAH_OPERATOR_KONG_LIGHT, operators)
        player_operators[_player.account_id] = operator_list
        func.log_info('-' * 50)

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
        if room.is_card_clear():
            if not win_flag:
                mahjong_operator_win(room, player, 0, games.MAH_OPERATOR_NO)
        else:
            dispatch_next_card(room)


def mahjong_operator(dynamic_id, player_operator, cards):
    card_list = [card_id for card_id in cards]
    account_id = PlayerManager().query_account_id(dynamic_id)
    if not account_id:
        func.log_error('[game] mahjong_operator account_id is unvalid, dynamic_id: {}'.format(dynamic_id))
        send.system_notice(dynamic_id, content.ENTER_DYNAMIC_LOGIN_EXPIRE)
        return
    room_manager = RoomManager()
    room_id = room_manager.query_player_room_id(account_id)
    if not room_id:
        func.log_error('[game] mahjong_operator room_id is unvalid, dynamic_id: {}, account_id: {}'.format(
                dynamic_id, account_id))
        send.system_notice(dynamic_id, content.ROOM_UN_EXIST)
        return
    room = room_manager.get_room(room_id)
    if not room:
        func.log_error('[game] mahjong_operator room is unvalid, dynamic_id: {}, account_id: {}, room_id: {}'.format(
                dynamic_id, account_id, room_id))
        send.system_notice(dynamic_id, content.ROOM_UN_FIND)
        return
    player = room.get_player(account_id)
    if not player:
        func.log_error('[game] mahjong_operator player is unvalid, dynamic_id: {}, account_id: {}, room_id: {}'.format(
                dynamic_id, account_id, room_id))
        send.system_notice(dynamic_id, content.ROOM_UN_ENTER)
        return
    player.status_ex = status.PLAYER_STATUS_FRONT   # 冗余
    func.log_info('[game] mahjong_operator account_id: {}, dynamic_id: {}, player_operator: {}, card_list: {}'.format(
        account_id, dynamic_id, player_operator, card_list
    ))
    last_card_id = 0
    last_cards = room.last_cards
    if last_cards:
        last_card_id = last_cards[0]
    if player_operator not in [games.MAH_OPERATOR_NONE, games.MAH_OPERATOR_WIN, games.MAH_OPERATOR_DRAWN]:
        if not card_list:
            func.log_error('[game] mahjong_operator PLAY_PLEASE_SELECT_CARD, account_id: {}, room_id: {}'.format(
                    account_id, room_id))
            send.system_notice(dynamic_id, content.PLAY_PLEASE_SELECT_CARD)
            return
        if last_card_id not in card_list:
            if not (player_operator in [games.MAH_OPERATOR_KONG_DARK, games.MAH_OPERATOR_KONG_PONG_SELF] and player.last_dispatch_card_id in card_list):
                func.log_error('[game] mahjong_operator PLAY_LAST_CARD_NOT_IN, account_id: {}, room_id: {}'.format(
                        account_id, room_id))
                send.system_notice(dynamic_id, content.PLAY_LAST_CARD_NOT_IN)
                return
    player_operators, all_operators = room.operators
    func.log_info('[game] mahjong_operator player_operators: {}'.format(player_operators))
    func.log_info('[game] mahjong_operator all_operators: {}'.format(all_operators))
    # if account_id not in player_operators:
    #     func.log_error('[game] mahjong_operator PLAY_OPERATOR_UN_ABLE, account_id: {}, room_id: {}'.format(
    #             account_id, room_id))
    #     send.system_notice(dynamic_id, content.PLAY_OPERATOR_UN_ABLE)
    #     return
    # operator_list = player_operators[account_id]
    # if player_operator != games.MAH_OPERATOR_NONE and player_operator not in operator_list:
    #     func.log_error('[game] mahjong_operator PLAY_OPERATOR_NO_RIGHT, account_id: {}, room_id: {}'.format(
    #             account_id, room_id))
    #     send.system_notice(dynamic_id, content.PLAY_OPERATOR_NO_RIGHT)
    #     return
    if player_operator == games.MAH_OPERATOR_NONE:
        mahjong_operator_none(room, player)
    elif player_operator in [games.MAH_OPERATOR_WIN, games.MAH_OPERATOR_DRAWN]:
        if player_operator == games.MAH_OPERATOR_DRAWN:
            last_card_id = player.last_dispatch_card_id
        mahjong_operator_win(room, player, last_card_id, player_operator)
    elif player_operator == games.MAH_OPERATOR_CHOW:
        raise
    elif player_operator == games.MAH_OPERATOR_PONG:
        if not check_mahjong_pong_valid(player, card_list):
            cards_info = games.get_mahjong_name(card_list)
            func.log_error('[game] mahjong_operator PLAY_MAHJONG_PONG_UNVALID, account_id: {}, room_id: {}, cards: {}'.format(
                    account_id, room_id, cards_info))
            send.system_notice(dynamic_id, content.PLAY_MAHJONG_PONG_UNVALID.format(cards_info))
            return
        mahjong_operator_pong(room, player, card_list)
        remove_mahjong_from_others(room, card_list)
    elif player_operator in games.MAH_OPERATOR_KONG_LIST:
        if not check_mahjong_kong_valid(player, card_list):
            cards_info = games.get_mahjong_name(card_list)
            func.log_error('[game] mahjong_operator PLAY_MAHJONG_KONG_UNVALID, account_id: {}, room_id: {}, cards: {}'.format(
                    account_id, room_id, cards_info))
            send.system_notice(dynamic_id, content.PLAY_MAHJONG_KONG_UNVALID.format(cards_info))
            return
        mahjong_operator_kong(room, player, card_list, player_operator)
        remove_mahjong_from_others(room, card_list)


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
    for pong_list in all_pong_list:
        all_in = True
        for _card_id in pong_list:
            if _card_id not in cur_list:
                all_in = False
                break
        if all_in:
            pong_kong_able = True
            break
    func.log_info('[game] check_mahjong_pong_kong card_id: {}, all_pong_list: {}, pong_kong_able: {}'.format(
            card_id, all_pong_list, pong_kong_able))
    return pong_kong_able


def check_mahjong_drawn(card_id, card_list):
    return _check_mahjong_win(card_id, card_list)


def _check_mahjong_win(card_id, cards):
    card_list = [card_id] + cards
    card_list.sort()
    func.log_info('[game] _check_mahjong_win card_list: {}'.format(card_list))
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
        func.log_info('[game] _check_mahjong_win door_id: {}'.format(door_id))
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
    if player.account_id == room.execute_account_id:
        func.log_info('[game] mahjong_operator_none player is executer')
        send.send_mahjong_operator([player.dynamic_id], player.account_id, games.MAH_OPERATOR_NONE, [])
        return
    player_operators, all_operators = room.operators
    next_flag = True
    if all_operators:
        func.log_info('[game] mahjong_operator_none player_operators: {}'.format(player_operators))
        func.log_info('[game] mahjong_operator_none all_operators: {}'.format(all_operators))
        # 冗余检查
        last_all_operators = dict()
        for _o, info_list in all_operators.items():
            last_info_list = []
            for _id, _position in info_list:
                if _id not in player_operators or _o not in player_operators[_id]:
                    continue
                last_info_list.append([_id, _position])
            if last_info_list:
                last_all_operators[_o] = last_info_list
        if last_all_operators:
            operator_account_id = select_mahjong_operator_account_id(last_all_operators, player.account_id, player.position)
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
        else:
            next_flag = False
    if next_flag:
        send.send_mahjong_operator([player.dynamic_id], player.account_id, games.MAH_OPERATOR_NONE, [])
    else:
        dispatch_next_card(room)
        del room.operators


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


def check_mahjong_pong_valid(player, card_list):
    if not card_list or len(card_list) != 3:
        return False
    card_id = card_list[0]
    cur_list = games.MAH_CONFIG[card_id]['cur_list']
    exist_list = player.card_list
    exist_count = 0
    for _card_id in card_list:
        if _card_id not in cur_list:
            return False
        if _card_id in exist_list:
            exist_count += 1
    if exist_count < 2:
        return False
    return True


def mahjong_operator_pong(room, player, card_list):
    func.log_info('[game] mahjong_operator_pong account_id: {}, card_list: {}'.format(
        player.account_id, card_list
    ))
    dynamic_id_list = room.get_room_dynamic_id_list()
    player.pong_list = card_list
    player.card_publish_list(card_list)
    send.send_mahjong_operator(dynamic_id_list, player.account_id, games.MAH_OPERATOR_PONG, card_list)
    room.execute_account_id = player.account_id     # 需要出一张牌
    send.broad_mahjong_dispatch_card(dynamic_id_list, player.account_id)
    del room.operators


def check_mahjong_kong_valid(player, card_list):
    if not card_list or len(card_list) != 4:
        return False
    card_id = card_list[0]
    cur_list = games.MAH_CONFIG[card_id]['cur_list']
    exist_list = player.card_list
    pong_list = player.pong_list
    func.log_info('[game] check_mahjong_kong_valid account_id: {}, exist_list: {}'.format(
            player.account_id, exist_list))
    func.log_info('[game] check_mahjong_kong_valid account_id: {}, pong_list: {}'.format(
            player.account_id, pong_list))
    exist_pong_list = []
    for _p in pong_list:
        exist_pong_list.extend(_p)
    exist_count = 0
    for _card_id in card_list:
        if _card_id not in cur_list:
            return False
        if _card_id in exist_list or _card_id in exist_pong_list:
            exist_count += 1
    func.log_info('[game] check_mahjong_kong_valid account_id: {}, exist_count: {}'.format(
            player.account_id, exist_count))
    if exist_list < 3:
        return False
    return True


def mahjong_operator_kong(room, player, card_list, player_operator):
    func.log_info('[game] mahjong_operator_kong account_id: {}, card_list: {}, player_operator: {}'.format(
        player.account_id, card_list, player_operator
    ))
    dynamic_id_list = room.get_room_dynamic_id_list()
    player.kong_list = card_list
    player.card_publish_list(card_list)
    send.send_mahjong_operator(dynamic_id_list, player.account_id, player_operator, card_list)
    room.execute_account_id = player.account_id     # 需要补一张牌
    dispatch_mahjong_card_account(player.account_id, player.dynamic_id, False)
    del room.operators
    mahjong_point_changes(room, player.account_id, player_operator)


def mahjong_point_changes(room, account_id, player_operator):
    change_list = []
    if player_operator == games.MAH_OPERATOR_KONG_DARK:
        base_point = 2
        for _player in room.players:
            if _player.account_id != account_id:
                change_point = -base_point
            else:
                change_point = base_point * (room.player_count - 1)
            _player.point_change(change_point)
            change_list.append({
                'account_id': _player.account_id,
                'point_change': change_point,
                'current_point': _player.point,
                'change_origin': player_operator
            })
    elif player_operator in [games.MAH_OPERATOR_KONG_LIGHT, games.MAH_OPERATOR_KONG_PONG_SELF]:
        base_point = 1
        for _player in room.players:
            if _player.account_id != account_id:
                change_point = -base_point
            else:
                change_point = base_point * (room.player_count - 1)
            _player.point_change(change_point)
            change_list.append({
                'account_id': _player.account_id,
                'point_change': change_point,
                'current_point': _player.point,
                'change_origin': player_operator
            })
    elif player_operator == games.MAH_OPERATOR_KONG_PONG_OTHER:
        base_point = 3
        player_list = [account_id, room.last_account_id]
        for _account_id in player_list:
            _player = room.get_player(_account_id)
            if _player:
                if _account_id == account_id:
                    change_point = base_point
                else:
                    change_point = -base_point
                _player.point_change(change_point)
                change_list.append({
                    'account_id': _player.account_id,
                    'point_change': change_point,
                    'current_point': _player.point,
                    'change_origin': player_operator
                })
    if change_list:
        dynamic_id_list = room.get_room_dynamic_id_list()
        send.mahjong_point_changes(dynamic_id_list, change_list)


def remove_mahjong_from_others(room, card_list):
    for player in room.players:
        player.others_list = card_list


def calc_mahjong_next_position(room, from_start):
    if from_start:
        room.mahjong_start = 1
    else:
        room.mahjong_end = 1


def mahjong_close(room, win_account_id, win_card_id, win_status):
    room.win_account_id = win_account_id
    all_player_info = room.room_mahjong_close(win_status)
    send.sync_play_history(room)
    roomfull.back_bail_gold(room)
    room.room_reset()
    dynamic_id_list = room.get_room_dynamic_id_list()
    send.game_over_mahjong(win_account_id, room.lose_account_id, win_card_id, win_status, all_player_info, dynamic_id_list)
    if room.is_full_rounds():
        roomfull.remove_room(room)

