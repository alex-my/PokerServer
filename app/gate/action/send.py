# coding:utf8
from app.gate.service import forward
from app.gate.core.RoomProxyManager import RoomProxyManager
from app.util.common.config import i
from app.util.common import func
from app.util.defines import informations
from app.util.defines import recharges as _recharges
from app.util.proto import system_pb2, recharge_pb2, login_pb2, room_pb2


def system_notice(dynamic_id, content):
    """
    系统通知
    :param dynamic_id: 客户端动态ID
    :param content: 内容
    :return:
    """
    response = system_pb2.m_9001_toc()
    response.content = content
    forward.push_object_gate(9001, response.SerializeToString(), [dynamic_id])


def user_change(dynamic_id, changes):
    """
    变化(整型版本)
    :param dynamic_id:
    :param changes:
    :return:
    """
    response = system_pb2.m_9003_toc()
    for change_type, change_value in changes.items():
        role_change = response.role_change.add()
        role_change.change_type = change_type
        role_change.change_value = change_value
    forward.push_object_gate(9003, response.SerializeToString(), [dynamic_id])


def marquee_to_all(content):
    response = system_pb2.m_9004_toc()
    response.content = content
    forward.push_object_gate_all(9004, response.SerializeToString())


def change_string(dynamic_id, changes):
    """
    变化(字符串版本)
    :param dynamic_id:
    :param changes:
    :return:
    """
    response = system_pb2.m_9005_toc()
    for change_type, change_value in changes.items():
        _changes = response.changes.add()
        _changes.change_type = change_type
        _changes.change_value = change_value
    forward.push_object_gate(9005, response.SerializeToString(), [dynamic_id])


def system_changes_string(changes):
    """
    系统变化
    :param changes:
    :return:
    """
    response = system_pb2.m_9005_toc()
    for change_type, change_value in changes.items():
        _changes = response.changes.add()
        _changes.change_type = change_type
        _changes.change_value = change_value
    forward.push_object_gate_all(9005, response.SerializeToString())


def recharge_wechat_prepay_info(dynamic_id, money, proxy_id, prepay_info):
    response = recharge_pb2.m_9101_toc()
    response.money = money
    response.proxy_id = proxy_id
    response.appid = prepay_info['appid']
    response.mch_id = prepay_info['mch_id']
    response.prepay_id = prepay_info['prepay_id']
    response._package = prepay_info['package']
    response.noncestr = prepay_info['nonce_str']
    response.timestamp = prepay_info['timestamp']
    response.sign = prepay_info['sign']
    forward.push_object_gate_all(9101, response.SerializeToString())


def login_success(dynamic_id, user):
    """
    推送玩家账号登陆成功信息
    :param dynamic_id:
    :param user: 玩家ID
    :return:
    """
    response = login_pb2.m_2001_toc()
    # 玩家信息
    user_info = response.user_info
    user_info.account_id = user.account_id
    user_info.uuid = user.uuid
    user_info.name = user.name
    user_info.head_frame = user.head_frame
    user_info.head_icon = user.head_icon
    user_info.sex = user.sex
    user_info.gold = user.gold
    user_info.point = user.point
    user_info.room_id = user.room_id
    user_info.room_type = user.room_type
    # 房间信息
    user_rooms = RoomProxyManager().get_user_rooms(user.account_id)
    rules = RoomProxyManager().get_all_rules()
    for game_type, rule in rules.iteritems():
        room_info = response.room_info.add()
        room_info.room_type = game_type
        room_info.room_id = user_rooms.get(game_type, 0)
        prices = rule['price']
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

    func.log_info('[game] 2001 account_id: {}, response: {}'.format(user.account_id, response))
    forward.push_object_gate(2001, response.SerializeToString(), [dynamic_id])


def create_room(dynamic_id, room_id, room_type, rounds):
    """
    create room success
    :param dynamic_id:
    :param room_id:
    :param room_type:
    :param rounds:
    :return:
    """
    response = room_pb2.m_3001_toc()
    response.room_id = room_id
    response.room_type = room_type
    response.rounds = rounds
    func.log_info('[gate] 3001 create_room response: {}'.format(response))
    forward.push_object_gate(3001, response.SerializeToString(), [dynamic_id])


def enter_poker_room(dynamic_id, room_id, room_type, room_data):
    """
    enter/resume room
    :param dynamic_id:
    :param room_id:
    :param room_data:
    :return:
    """
    response = room_pb2.m_3002_toc()
    response.room_id = room_id
    response.room_type = room_type
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
    """
    enter/resume room
    :param dynamic_id:
    :param room_id:
    :param room_data:
    :param operator_account_id:
    :param player_operators:
    :return:
    """
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
