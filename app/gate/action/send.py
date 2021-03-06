# coding:utf8
from app.gate.service import forward
from app.gate.core.RoomProxyManager import RoomProxyManager
from app.util.common.config import i
from app.util.common import func
from app.util.defines import informations, rule
from app.util.defines import recharges as _recharges
from app.util.proto import system_pb2, recharge_pb2, login_pb2, room_pb2


def system_notice(dynamic_id, content):
    response = system_pb2.m_9001_toc()
    response.content = content
    forward.push_object_gate(9001, response.SerializeToString(), [dynamic_id])


def user_change(dynamic_id, changes):
    response = system_pb2.m_9003_toc()
    for change_type, change_value in changes.items():
        role_change = response.role_change.add()
        role_change.change_type = change_type
        role_change.change_value = change_value
    forward.push_object_gate(9003, response.SerializeToString(), [dynamic_id])


def marquee_to_all(content):
    response = system_pb2.m_9004_toc()
    response.content = content
    func.log_info('[gate] 9004 marquee_to_all response: {}'.format(response))
    forward.push_object_gate_all(9004, response.SerializeToString())


def marquee_to_user(dynamic_id, content):
    response = system_pb2.m_9004_toc()
    response.content = content
    func.log_info('[gate] 9004 marquee_to_user response: {}'.format(response))
    forward.push_object_gate(9004, response.SerializeToString(), [dynamic_id])


def change_string(dynamic_id, changes):
    response = system_pb2.m_9005_toc()
    for change_type, change_value in changes.items():
        _changes = response.changes.add()
        _changes.change_type = change_type
        _changes.change_value = change_value
    forward.push_object_gate(9005, response.SerializeToString(), [dynamic_id])


def system_changes_string(changes):
    response = system_pb2.m_9005_toc()
    for change_type, change_value in changes.items():
        _changes = response.changes.add()
        _changes.change_type = change_type
        _changes.change_value = change_value
    forward.push_object_gate_all(9005, response.SerializeToString())


def send_heart_tick(dynamic_id):
    response = system_pb2.m_9006_toc()
    forward.push_object_gate(9006, response.SerializeToString(), [dynamic_id])


def recharge_wechat_prepay_info(dynamic_id, money, proxy_id, prepay_info):
    response = recharge_pb2.m_9101_toc()
    response.money = money
    response.proxy_id = str(proxy_id)
    response.appid = prepay_info['appid']
    response.mch_id = prepay_info['mch_id']
    response.prepay_id = prepay_info['prepay_id']
    response._package = prepay_info['package']
    response.noncestr = prepay_info['nonce_str']
    response.timestamp = prepay_info['timestamp']
    response.sign = prepay_info['sign']
    forward.push_object_gate_all(9101, response.SerializeToString())


def login_success(dynamic_id, user):
    response = login_pb2.m_2001_toc()
    remove_room_id_list = []
    room_proxy_manager = RoomProxyManager()
    if user.room_id > 0 and room_proxy_manager.is_room_expire(user.room_id):
        remove_room_id_list.append(user.room_id)
        user.room_id = 0
        user.room_type = 0
    # 玩家信息
    user_info = response.user_info
    user_info.account_id = user.account_id
    user_info.uuid = user.uuid
    user_info.name = user.name
    user_info.head_frame = user.head_frame
    user_info.head_icon = user.head_icon
    user_info.sex = user.sex
    user_info.gold = user.gold
    user_info.point = 0
    user_info.room_id = user.room_id
    user_info.room_type = user.room_type
    user_info.proxy_id = user.proxy_id
    # 房间信息
    user_rooms = room_proxy_manager.get_user_rooms(user.account_id)
    rules = RoomProxyManager().get_all_rules()
    for game_type, _rule in rules.iteritems():
        room_info = response.room_info.add()
        room_info.room_type = game_type
        room_id = user_rooms.get(game_type, 0)
        if not room_proxy_manager.is_room_expire(room_id):
            room_info.room_id = room_id
        else:
            if room_id > 0:
                remove_room_id_list.append(room_id)
            room_info.room_id = 0
        prices = _rule['price']
        for rounds, price in prices.items():
            room_price = room_info.room_price.add()
            room_price.rounds = rounds
            room_price.gold_price = price
    # 游戏信息
    response.game_info.contact = i(informations.INFOMATION_TYPE_CONTACT, '')
    recharges_information = _recharges.recharges_information
    for _money, _ingot in recharges_information.items():
        recharges = response.game_info.recharges.add()
        recharges.money = _money
        recharges.ingot = _ingot
    response.game_info.poker_per_price = rule.POKER_PER_PRICE
    response.game_info.mahjong_per_price = rule.MAHJONG_PER_PRICE

    func.log_info('[game] 2001 account_id: {}, response: {}'.format(user.account_id, response))
    forward.push_object_gate(2001, response.SerializeToString(), [dynamic_id])
    # TODO: remove expired room


def bind_success(dynamic_id, proxy_id):
    response = login_pb2.m_2002_toc()
    response.proxy_id = proxy_id
    func.log_info('[game] 2002 dynamic_id: {}, response: {}'.format(dynamic_id, response))
    forward.push_object_gate(2002, response.SerializeToString(), [dynamic_id])


def create_room(dynamic_id, room_id, room_type, room_help, rounds):
    response = room_pb2.m_3001_toc()
    response.room_id = room_id
    response.room_type = room_type
    response.room_help = room_help
    response.rounds = rounds
    func.log_info('[gate] 3001 create_room response: {}'.format(response))
    forward.push_object_gate(3001, response.SerializeToString(), [dynamic_id])


def enter_poker_room(dynamic_id, room_id, room_type, room_help, room_data):
    response = room_pb2.m_3002_toc()
    response.room_id = room_id
    response.room_type = room_type
    response.room_help = room_help
    if room_data:
        for user_info in room_data['user_room']:
            user_room = response.user_room.add()
            user_room.position = user_info['position']
            user_room.account_id = user_info['account_id']
            user_room.name = user_info['name']
            user_room.head_frame = user_info['head_frame']
            user_room.head_icon = user_info['head_icon']
            user_room.sex = user_info['sex']
            user_room.ip = user_info['ip']
            user_room.point = user_info['point']
            user_room.status = user_info['status']

        for card_id in room_data['user_cards']:
            response.user_cards.append(card_id)
        response.execute_account_id = room_data['execute_account_id']
        response.last_account_id = room_data['last_account_id']
        for card_id in room_data['last_cards']:
            response.last_cards.append(card_id)
        response.user_id = room_data['user_id']
        response.rounds = room_data['rounds']
        response.max_rounds = room_data['max_rounds']

    func.log_info('[gate] 3002 response: {}'.format(response))
    forward.push_object_gate(3002, response.SerializeToString(), [dynamic_id])


def enter_mahjong_room(dynamic_id, room_id, room_data, operator_account_id, player_operators):
    response = room_pb2.m_3003_toc()
    response.room_id = room_id
    if room_data:
        for user_info in room_data['user_room']:
            user_room = response.user_room.add()
            user_room.position = user_info['position']
            user_room.account_id = user_info['account_id']
            user_room.name = user_info['name']
            user_room.head_frame = user_info['head_frame']
            user_room.head_icon = user_info['head_icon']
            user_room.sex = user_info['sex']
            user_room.ip = user_info['ip']
            user_room.point = user_info['point']
            user_room.status = user_info['status']
            for card_id in user_info.get('pre_cards', []):
                user_room.pre_cards.append(card_id)
            for card_list in user_info.get('award_cards', []):
                award_cards = user_room.award_cards.add()
                for card_id in card_list:
                    award_cards.cards.append(card_id)
            user_room.card_count = user_info['card_count']
            user_room.operator_able = user_info['account_id'] == operator_account_id
            _operator_list = player_operators.get(user_info['account_id'])
            if _operator_list:
                for operator_id in _operator_list:
                    user_room.operators.append(operator_id)

        for card_id in room_data['user_cards']:
            response.user_cards.append(card_id)
        response.execute_account_id = room_data['execute_account_id']
        response.last_account_id = room_data['last_account_id']
        for card_id in room_data['last_cards']:
            response.last_cards.append(card_id)
        response.user_id = room_data['user_id']
        response.rounds = room_data['rounds']
        response.max_rounds = room_data['max_rounds']
        craps = room_data.get('craps', [])
        for crap in craps:
            response.craps.append(crap)
        response.maker_account_id = room_data.get('maker_account_id', 0)
        response.mahjong_start_num = room_data.get('mahjong_start_num', 0)
        response.mahjong_end_num = room_data.get('mahjong_end_num', 0)
        response.operator_account_id = operator_account_id

    func.log_info('[gate] 3003 dynamic_id: {}, response: {}'.format(dynamic_id, response))
    forward.push_object_gate(3003, response.SerializeToString(), [dynamic_id])


def send_play_history(user):
    response = room_pb2.m_3201_toc()
    response.poker_point = user.poker_point
    response.mahjong_point = user.mahjong_point
    response.gold_point = user.gold_point
    history_list = user.get_play_history_list()
    # None
    if history_list:
        for info in history_list:
            history_info = response.history_info.add()
            history_info.room_id = info['room_id']
            history_info.room_type = info['room_type']
            history_info.win_account_id = info['win_account_id']
            history_info.server_t = info['server_t']
            history_info.round = info['round']
            history_info.max_round = info['max_round']
            player_info_list = info['history_player']
            for player_info in player_info_list:
                history_player = history_info.history_player.add()
                history_player.account_id = player_info['account_id']
                history_player.name = player_info['name']
                history_player.point_changes = player_info['point_changes']
                history_player.room_point = player_info['room_point']
                history_player.all_point = player_info['all_point']
    func.log_info('[gate] 3201 send_play_history dynamic_id: {}, response: {}'.format(user.dynamic_id, response))
    forward.push_object_gate(3201, response.SerializeToString(), [user.dynamic_id])


def allow_online_match(dynamic_id):
    response = room_pb2.m_3202_toc()
    func.log_info('[gate] 3202 allow_online_match dynamic_id: {}'.format(dynamic_id))
    forward.push_object_gate(3202, response.SerializeToString(), [dynamic_id])


def online_match_success(dynamic_id_list, room_id):
    response = room_pb2.m_3203_toc()
    response.room_id = room_id
    func.log_info('[gate] 3203 online_match_success dynamic_id_list: {}, room_id: {}'.format(
        dynamic_id_list, room_id
    ))
    forward.push_object_gate(3203, response.SerializeToString(), dynamic_id_list)


def cancel_online_match(dynamic_id):
    response = room_pb2.m_3204_toc()
    func.log_info('[gate] 3203 cancel_online_match dynamic_id: {}'.format(dynamic_id))
    forward.push_object_gate(3204, response.SerializeToString(), [dynamic_id])
