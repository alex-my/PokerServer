# coding:utf8
from app.gate.gateservice import request_child_node
from app.gate.core.NodeManager import NodeManager
from app.gate.core.UserManager import UserManager
from app.gate.core.OnlineMatchManager import OnlineMatchManager
from app.gate.core.RoomProxyManager import RoomProxyManager
from app.gate.core.RoomProxy import RoomProxy
from app.gate.action import send, change
from app.util.common import func
from app.util.defines import content, dbname, rule, origins, games
from app.util.driver import dbexecute


def _get_open_room_origin(room_type):
    if room_type == rule.GAME_TYPE_PDK:
        origin = origins.ORIGIN_OPEN_ROOM_PDK
    elif room_type == rule.GAME_TYPE_ZZMJ:
        origin = origins.ORIGIN_OPEN_ROOM_ZZMJ
    elif room_type == rule.GAME_TYPE_PDK2:
        origin = origins.ORIGIN_OPEN_ROOM_PDK2
    else:
        origin = origins.ORIGIN_UNKNOWN
    return origin


def create_room(dynamic_id, room_type, rounds, help_value):
    """
    create room
    :param dynamic_id:
    :param room_type:
    :param rounds:
    :param help_value:
    :return:
    """
    if not help_value:
        help_value = 0
    func.log_info('[game] create_room room_type: {}, rounds: {}, help_value: {}'.format(room_type, rounds, help_value))
    if not room_type or not rounds:
        send.system_notice(dynamic_id, content.SYSTEM_ARGUMENT_LACK)
        return
    if room_type not in rule.rule_configs:
        send.system_notice(dynamic_id, content.ROOM_TYPE_UN_FIND)
        return
    user = UserManager().get_user_by_dynamic(dynamic_id)
    if not user:
        send.system_notice(dynamic_id, content.ENTER_DYNAMIC_LOGIN_EXPIRE)
        return
    room_manager = RoomProxyManager()
    # check repeated create
    old_room = room_manager.get_user_special_room(user.account_id, room_type)
    if old_room:
        send.system_notice(dynamic_id, content.ROOM_TYPE_EXIST.format(old_room.room_id))
        return
    # check price
    room_price = room_manager.get_room_price(room_type, rounds)
    if room_price < 0:
        send.system_notice(dynamic_id, content.ROOM_UN_FIND_ROUNDS.format(rounds))
        return
    open_origin = _get_open_room_origin(room_type)
    if not user.check_gold(room_price):
        send.system_notice(dynamic_id, content.GOLD_LACK)
        return
    change.spend_gold(user, room_price, open_origin)
    node = _get_best_game_node(dynamic_id)
    if not node:
        return
    room = _create_room(user.account_id, room_type, help_value, rounds)
    if not room:
        send.system_notice(dynamic_id, content.ROOM_CREATE_FAILED)
        return
    room.room_help = help_value
    room.node_name = node.node_name
    room_manager.add_room(room)
    send.create_room(dynamic_id, room.room_id, room.room_type, room.room_help, rounds)


def _get_best_game_node(dynamic_id, repeated=True):
    node_manager = NodeManager()
    node_list = node_manager.get_all_nodes_list()
    if node_list:
        node_manager.init_nodes(True)
        node_list = node_manager.get_all_nodes_list()
        if not node_list:
            send.system_notice(dynamic_id, content.LOGIN_SERVER_UN_OPEN)
            return None
    sort_node_list = sorted(node_list, reverse=False, key=lambda _node: _node.get_rooms_count())
    node = sort_node_list[0]
    if not node.is_full():
        return node
    if repeated:
        return _get_best_game_node(False)
    send.system_notice(dynamic_id, content.LOGIN_SERVER_FULL)
    return None


def _create_room(account_id, room_type, room_help, rounds):
    room_id = RoomProxyManager().generator_room_id()
    if room_id <= 0:
        return None
    room = RoomProxy()
    t = func.time_get()
    insert_data = {
        'room_id': room_id,
        'room_type': room_type,
        'room_help': room_help,
        'rounds': rounds,
        'create_time': t,
        'account_id': account_id,
        'data': func.transform_object_to_pickle(None)
    }
    result = dbexecute.insert_record(**{'table': dbname.DB_ROOM, 'data': insert_data})
    if result > 0:
        room.create(room_id, room_type, rounds, account_id, t)
        return room
    return None


def enter_room(dynamic_id, room_id):
    """
    enter or resume room
    :param dynamic_id:
    :param room_id:
    :return:
    """
    if not room_id:
        send.system_notice(dynamic_id, content.SYSTEM_ARGUMENT_LACK)
        return
    user = UserManager().get_user_by_dynamic(dynamic_id)
    if not user:
        send.system_notice(dynamic_id, content.ENTER_DYNAMIC_LOGIN_EXPIRE)
        return
    room = RoomProxyManager().get_room(room_id)
    if not room:
        send.system_notice(dynamic_id, content.ROOM_UN_EXIST)
        return
    # check expire time
    if room.is_expire():
        send.system_notice(dynamic_id, content.ROOM_EXPIRE)
        return
    # check price
    if not check_room_price(user, room):
        return
    # check online match bail price
    if room.is_online_match():
        if not user.check_gold(rule.ONLINE_MATCH_MIN_GOLD):
            send.system_notice(dynamic_id, content.GOLD_LACK_ONLINE_MATCH.format(rule.ONLINE_MATCH_MIN_GOLD))
            return
    if not room.node_name:
        node = _get_best_game_node(dynamic_id)
        if not node:
            return
        room.node_name = node.node_name
    node_name = room.node_name

    request_child_node(node_name, 'enter_room_game', dynamic_id=dynamic_id, _node_name=node_name,
                       account_id=user.account_id, room_id=room_id, name=user.name, head_frame=user.head_frame,
                       head_icon=user.head_icon, sex=user.sex, ip=user.ip)


def enter_room_confirm(account_id, dynamic_id, node_name, room_id, room_data, operator_account_id, player_operators):
    user = UserManager().get_user(account_id)
    if not user:
        send.system_notice(dynamic_id, content.ENTER_DYNAMIC_LOGIN_EXPIRE)
        return
    room = RoomProxyManager().get_room(room_id)
    if not room:
        send.system_notice(dynamic_id, content.ROOM_UN_EXIST)
        return
    # bind user to special node
    user.node_name = node_name
    user.record_room_id = room.room_id
    user.record_room_type = room.room_type
    room.account_id_list = user.account_id
    if room.room_type in rule.GAME_LIST_POKER_PDK:
        send.enter_poker_room(user.dynamic_id, room_id, room.room_type, room.room_help, room_data)
    elif room.room_type in rule.GAME_LIST_MAHJONG:
        send.enter_mahjong_room(user.dynamic_id, room_id, room_data, operator_account_id, player_operators)


def remove_room_id(account_id, room_id):
    user = UserManager().get_user(account_id)
    if not user:
        func.log_info('[gate] remove_room_id un find account_id: {}, room_id: {}'.format(
            account_id, room_id
        ))
        return
    if user.record_room_id == room_id:
        user.record_room_id = 0
        user.record_room_type = 0
    if user.room_id == room_id:
        user.room_id = 0
        user.room_type = 0


def remove_room(room_id):
    """
    删除房间
    :param room_id:
    :return:
    """
    room_manager = RoomProxyManager()
    user_manager = UserManager()
    room = room_manager.get_room(room_id)
    account_id_list = room.account_id_list
    for account_id in account_id_list:
        user = user_manager.get_user(account_id)
        if user and (user.room_type == room.room_type or user.record_room_type == room.room_type):
            user.room_id = 0
            user.room_type = 0
            user.record_room_id = 0
            user.record_room_type = 0
            user.node_name = None
    RoomProxyManager().remove_room(room_id, room.room_type, room.account_id)
    sql = 'delete from {} where room_id={}'.format(dbname.DB_ROOM, room_id)
    dbexecute.execute(sql)


def check_room_price(user, room):
    if room.room_type in rule.GAME_LIST_POKER_PDK:
        price = rule.POKER_PER_PRICE
    elif room.room_type in rule.GAME_LIST_MAHJONG:
        price = rule.MAHJONG_PER_PRICE
    else:
        raise KeyError('[gate] check_room_price room_type: {} unexist'.format(room.room_type))

    price = int(price * room.room_rounds)
    if not user.check_gold(price):
        send.system_notice(user.dynamic_id, content.GOLD_LACK_PER.format(price))
        return False
    return True


def query_play_history(dynamic_id):
    user = UserManager().get_user_by_dynamic(dynamic_id)
    if not user:
        send.system_notice(dynamic_id, content.ENTER_DYNAMIC_LOGIN_EXPIRE)
        return
    send.send_play_history(user)


def online_match(dynamic_id, room_type):
    user_manager = UserManager()
    user = user_manager.get_user_by_dynamic(dynamic_id)
    if not user:
        send.system_notice(dynamic_id, content.ENTER_DYNAMIC_LOGIN_EXPIRE)
        return
    func.log_info('[gate] online_match account_id: {}, room_type: {}'.format(user.account_id, room_type))
    if not user.check_gold(rule.ONLINE_MATCH_MIN_GOLD):
        send.system_notice(dynamic_id, content.GOLD_LACK_ONLINE_MATCH.format(rule.ONLINE_MATCH_MIN_GOLD))
        return
    online_match_manager = OnlineMatchManager()
    send.allow_online_match(dynamic_id)

    if online_match_manager.is_match_success(room_type):
        all_match_list = online_match_manager.get_match_list(room_type)
        need_count = online_match_manager.get_match_need_count(room_type)
        dynamic_id_list = [dynamic_id]
        delete_id_list = []
        for _account_id in all_match_list:
            _user = user_manager.get_user(_account_id)
            delete_id_list.append(_account_id)
            if _user:
                if _user.dynamic_id not in dynamic_id_list:
                    dynamic_id_list.append(_user.dynamic_id)
                    if len(dynamic_id_list) >= need_count:
                        break
        if len(dynamic_id_list) >= need_count:
            room = _create_room(0, room_type, games.HELP_ONLINE_MATCH, 10)     # 固定10回合, 无房主
            if not room:
                send.system_notice(dynamic_id, content.ROOM_CREATE_FAILED)
                return
            RoomProxyManager().add_room(room)
            online_match_manager.remove_match_list(room_type, delete_id_list)
            send.online_match_success(dynamic_id_list, room.room_id)
            return
    online_match_manager.add_match_user(room_type, user.account_id)


def cancel_online_match(dynamic_id):
    user = UserManager().get_user_by_dynamic(dynamic_id)
    if not user:
        send.system_notice(dynamic_id, content.ENTER_DYNAMIC_LOGIN_EXPIRE)
        return
    func.log_info('[gate] cancel_online_match account_id: {}'.format(user.account_id))
    OnlineMatchManager().remove_user(user.account_id)
    send.cancel_online_match(dynamic_id)

