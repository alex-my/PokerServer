# coding:utf8
from app.game.service import forward
from app.util.common import func
from app.util.proto import system_pb2, room_pb2, play_pb2, game_poker_pb2, game_mahjong_pb2


def system_notice(dynamic_id, content):
    """
    系统通知
    :param dynamic_id: 客户端动态ID
    :param content: 内容
    :return:
    """
    response = system_pb2.m_9001_toc()
    response.content = content
    func.log_warn('[game] system_notice dynamic_id: {}'.format(dynamic_id))
    forward.push_object_game(9001, response.SerializeToString(), [dynamic_id])


def broad_player_enter(dynamic_id_list, user_info):
    response = room_pb2.m_3005_toc()
    response.user_room.position = user_info['position']
    response.user_room.account_id = user_info['account_id']
    response.user_room.name = user_info['name']
    response.user_room.head_frame = user_info['head_frame']
    response.user_room.head_icon = user_info['head_icon']
    response.user_room.sex = user_info['sex']
    response.user_room.ip = user_info['ip']
    response.user_room.point = user_info['point']
    response.user_room.status = user_info['status']
    func.log_info('[game] 3005 broad_player_enter dynamic_id_list: {}, response: {}'.format(
        dynamic_id_list, response))
    forward.push_object_game(3005, response.SerializeToString(), dynamic_id_list)


def broad_player_leave(dynamic_id_list, account_id):
    response = room_pb2.m_3006_toc()
    response.account_id = account_id
    func.log_info('[game] 3006 broad_player_leave dynamic_id_list: {},  response: {}'.format(
        dynamic_id_list, account_id, response))
    forward.push_object_game(3006, response.SerializeToString(), dynamic_id_list)


def short_message_to_self(dynamic_id, message):
    response = room_pb2.m_3101_toc()
    response.message = message
    func.log_info('[game] 3101 short_message_to_self dynamic_id: {}, message: {}'.format(
        dynamic_id, message
    ))
    forward.push_object_game(3101, response.SerializeToString(), [dynamic_id])


def short_message_to_all(dynamic_id_list, account_id, message):
    response = room_pb2.m_3102_toc()
    response.account_id = account_id
    response.message = message
    func.log_info('[game] 3102 short_message_to_all dynamic_id_list: {}, message: {}'.format(
        dynamic_id_list, message
    ))
    forward.push_object_game(3102, response.SerializeToString(), dynamic_id_list)


def voice_message_to_self(dynamic_id, voice_url):
    response = room_pb2.m_3103_toc()
    response.voice_url = voice_url
    func.log_info('[game] 3103 voice_message_to_self dynamic_id: {}, voice_url: {}'.format(
        dynamic_id, voice_url
    ))
    forward.push_object_game(3103, response.SerializeToString(), [dynamic_id])


def voice_message_to_all(dynamic_id_list, account_id, voice_url):
    response = room_pb2.m_3104_toc()
    response.account_id = account_id
    response.voice_url = voice_url
    func.log_info('[game] 3104 voice_message_to_all dynamic_id_list: {}, voice_url: {}'.format(
        dynamic_id_list, voice_url
    ))
    forward.push_object_game(3104, response.SerializeToString(), dynamic_id_list)


def user_operator(dynamic_id, operator):
    """
    user operator
    :param dynamic_id:
    :param operator:
    :return:
    """
    response = play_pb2.m_4001_toc()
    response.operate = operator
    func.log_info('[game] 4001 user_operator dynamic_id: {}, response: {}'.format(dynamic_id, response))
    forward.push_object_game(4001, response.SerializeToString(), [dynamic_id])


def dispatch_user_operator(account_id, operator, dynamic_id_list):
    response = play_pb2.m_4002_toc()
    response.account_id = account_id
    response.operate = operator
    func.log_info('[game] 4002 dispatch_user_operator dynamic_id_list: {}, response: {}'.format(
        dynamic_id_list, response))
    forward.push_object_game(4002, response.SerializeToString(), dynamic_id_list)


def player_dispatch_cards(execute_account_id, player):
    response = play_pb2.m_4003_toc()
    response.execute_account_id = execute_account_id
    for card_id in player.card_list:
        response.cards.append(card_id)
    func.log_info('[game] 4003, dynamic_id: {}, response: {}'.format(
        player.dynamic_id, response))
    forward.push_object_game(4003, response.SerializeToString(), [player.dynamic_id])


def game_over(win_account_id, all_player_info, dynamic_id_list):
    response = play_pb2.m_4004_toc()
    response.win_account_id = win_account_id
    for account_id, card_count in all_player_info.items():
        close_info = response.close_info.add()
        close_info.account_id = account_id
        close_info.card_count = card_count
    func.log_info('[game] 4004 game_over dynamic_id_list: {}, response: {}'.format(
        dynamic_id_list, response))
    forward.push_object_game(4004, response.SerializeToString(), dynamic_id_list)


def publish_poker_to_self(dynamic_id):
    response = game_poker_pb2.m_5101_toc()
    func.log_info('[game] 5101 publish_poker_to_self dynamic_id: {}, response: {}'.format(
        dynamic_id, response))
    forward.push_object_game(5101, response.SerializeToString(), [dynamic_id])


def publish_poker_to_room(dynamic_id, account_id, next_account_id, cards, self_cards):
    response = game_poker_pb2.m_5102_toc()
    response.execute_account_id = account_id
    response.next_account_id = next_account_id
    for card_id in cards:
        response.cards.append(card_id)
    for card_id in self_cards:
        response.card_list.append(card_id)
    func.log_info('[game] 5102 publish_poker_to_room dynamic_id: {}, response: {}'.format(
            dynamic_id, response))
    forward.push_object_game(5102, response.SerializeToString(), [dynamic_id])


def send_poker_bomb(account_id, point, dynamic_id_list):
    response = game_poker_pb2.m_5103_toc()
    response.account_id = account_id
    response.point = point
    func.log_info('[game] 5103 send_poker_bomb dynamic_id_list: {}, response: {}'.format(
        dynamic_id_list, response
    ))
    forward.push_object_game(5103, response.SerializeToString(), dynamic_id_list)


def send_few_card_count(dynamic_id_list, account_id, card_count):
    response = game_poker_pb2.m_5104_toc()
    response.account_id = account_id
    response.card_count = card_count
    func.log_info('[game] 5104 send_few_card_count dynamic_id_list: {}, response: {}'.format(
        dynamic_id_list, response
    ))
    forward.push_object_game(5104, response.SerializeToString(), dynamic_id_list)


def send_room_full(dynamic_id_list, statistic_list):
    response = game_poker_pb2.m_5105_toc()
    response.server_t = func.time_get()
    for info in statistic_list:
        room_fulls = response.room_fulls.add()
        room_fulls.account_id = info['account_id']
        room_fulls.rank = info['rank']
        room_fulls.point_change = info['point_change']
        room_fulls.win_count = info['win_count']
        room_fulls.lose_count = info['lose_count']
        room_fulls.bomb_count = info['bomb_count']
        room_fulls.max_point = info['max_point']
    func.log_info('[game] 5105 send_room_full dynamic_id_list: {}, response: {}'.format(
        dynamic_id_list, response
    ))
    forward.push_object_game(5105, response.SerializeToString(), dynamic_id_list)


def dispatch_mahjong_card(dynamic_id, card):
    response = game_mahjong_pb2.m_5201_toc()
    response.card = card
    func.log_info('[game] 5201 dispatch_mahjong_card dynamic_id: {}, response: {}'.format(
        dynamic_id, response
    ))


def publish_mahjong_to_self(dynamic_id):
    response = game_mahjong_pb2.m_5202_toc()
    func.log_info('[game] 5202 publish_mahjong_to_self dynamic_id: {}, response: {}'.format(
            dynamic_id, response))
    forward.push_object_game(5202, response.SerializeToString(), [dynamic_id])


def publish_mahjong_to_room(player, execute_account_id, cards):
    response = game_mahjong_pb2.m_5203_toc()
    # TODO: publish_mahjong_to_room



