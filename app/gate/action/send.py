# coding:utf8
from app.gate.service import forward
from app.gate.core.RoomProxyManager import RoomProxyManager
from app.util.common import func
from app.util.proto import system_pb2, login_pb2, room_pb2, play_pb2


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
    forward.push_object_gate(3001, response.SerializeToString(), [dynamic_id])


def enter_room(dynamic_id, room_id, room_data):
    """
    enter/resume room
    :param dynamic_id:
    :param room_id:
    :param room_data:
    :return:
    """
    response = room_pb2.m_3002_toc()
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

