# coding:utf8
from app.game.gameservice import request_gate_node
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


def system_notice_room(room, content):
    """
    通知全房间
    :param room:
    :param content:
    :return:
    """
    dynamic_id_list = room.get_room_dynamic_id_list()
    response = system_pb2.m_9001_toc()
    response.content = content
    func.log_warn('[game] system_notice_room dynamic_id: {}'.format(dynamic_id_list))
    forward.push_object_game(9001, response.SerializeToString(), dynamic_id_list)


def broad_player_enter_poker(dynamic_id_list, user_info):
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
    func.log_info('[game] 3005 broad_player_enter_poker dynamic_id_list: {}, response: {}'.format(
        dynamic_id_list, response))
    forward.push_object_game(3005, response.SerializeToString(), dynamic_id_list)


def broad_player_enter_mahjong(dynamic_id_list, user_info, operator_account_id, operators_list):
    response = room_pb2.m_3007_toc()
    response.user_room.position = user_info['position']
    response.user_room.account_id = user_info['account_id']
    response.user_room.name = user_info['name']
    response.user_room.head_frame = user_info['head_frame']
    response.user_room.head_icon = user_info['head_icon']
    response.user_room.sex = user_info['sex']
    response.user_room.ip = user_info['ip']
    response.user_room.point = user_info['point']
    response.user_room.status = user_info['status']
    for card_id in user_info.get('pre_cards', []):
        response.user_room.pre_cards.append(card_id)
    for card_list in user_info.get('award_cards', []):
        award_cards = response.user_room.award_cards.add()
        for card_id in card_list:
            award_cards.cards.append(card_id)
    response.user_room.card_count = user_info['card_count']
    response.user_room.operator_able = user_info['account_id'] == operator_account_id
    if operators_list:
        for operator_id in operators_list:
            response.user_room.operators.append(operator_id)
    func.log_info('[game] 3007 broad_player_enter_mahjong dynamic_id_list: {}, response: {}'.format(
        dynamic_id_list, response))
    forward.push_object_game(3007, response.SerializeToString(), dynamic_id_list)


def broad_player_leave(dynamic_id_list, account_id):
    response = room_pb2.m_3006_toc()
    response.account_id = account_id
    func.log_info('[game] 3006 broad_player_leave dynamic_id_list: {},  response: {}'.format(
        dynamic_id_list, account_id, response))
    forward.push_object_game(3006, response.SerializeToString(), dynamic_id_list)


def broad_room_all_in(dynamic_id_list, room_type):
    response = room_pb2.m_3008_toc()
    response.room_type = room_type
    func.log_info('[game] 3008 broad_room_all_in dynamic_id_list: {}, response: {}'.format(
        dynamic_id_list, response
    ))
    forward.push_object_game(3008, response.SerializeToString(), dynamic_id_list)


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
    for account_id, info in all_player_info:
        close_info = response.close_info.add()
        close_info.account_id = account_id
        close_info.card_count = info['left_card_count']
        close_info.point_change = info['change_point']
        _disptach_cards = info['disptach_cards']
        for _dispatch_list in _disptach_cards:
            dispatch_cards = close_info.dispatch_cards.add()
            for _card_id in _dispatch_list:
                dispatch_cards.card_id.append(_card_id)
    func.log_info('[game] 4004 game_over dynamic_id_list: {}, response: {}'.format(
        dynamic_id_list, response))
    forward.push_object_game(4004, response.SerializeToString(), dynamic_id_list)


def game_over_mahjong(win_account_id, lose_account_id, win_card_id, win_status, all_player_info, dynamic_id_list):
    response = play_pb2.m_4006_toc()
    response.win_account_id = win_account_id
    response.win_card_id = win_card_id
    response.win_status = win_status
    response.lose_account_id = lose_account_id
    for account_id, info in all_player_info.items():
        close_info = response.close_info.add()
        close_info.account_id = account_id
        for _award_card_list in info.get('award_cards', []):
            award_card_list = close_info.award_card.add()
            for _award_card_id in _award_card_list:
                award_card_list.card_id.append(_award_card_id)
        for _card_id in info.get('cards', []):
            close_info.card_id.append(_card_id)
        close_info.point_change = info.get('point_change', 0)
        close_info.current_point = info.get('current_point', 0)
        func.log_info('[game] 4006 game_over_mahjong dynamic_id_list: {}, response: {}'.format(
             dynamic_id_list, response
        ))
    forward.push_object_game(4006, response.SerializeToString(), dynamic_id_list)


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


def send_poker_room_full(dynamic_id_list, statistic_list):
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
    func.log_info('[game] 5105 send_poker_room_full dynamic_id_list: {}, response: {}'.format(
        dynamic_id_list, response
    ))
    forward.push_object_game(5105, response.SerializeToString(), dynamic_id_list)


def send_mahjong_craps(dynamic_id, **kwargs):
    response = game_mahjong_pb2.m_5201_toc()
    response.maker_account_id = kwargs.get('maker_account_id', 0)
    craps = kwargs.get('craps', [])
    for crap in craps:
        response.craps.append(crap)
    response.mahjong_start_num = kwargs.get('mahjong_start_num', 0)
    response.mahjong_end_num = kwargs.get('mahjong_end_num', 0)
    func.log_info('[game] 5201 send_mahjong_craps dynamic_id: {}, response: {}'.format(
        dynamic_id, response
    ))
    forward.push_object_game(5201, response.SerializeToString(), [dynamic_id])


def dispatch_mahjong_card(dynamic_id, card, operator_list):
    response = game_mahjong_pb2.m_5202_toc()
    response.card = card
    for operator in operator_list:
        response.operator.append(operator)
    func.log_info('[game] 5202 dispatch_mahjong_card dynamic_id: {}, response: {}'.format(
        dynamic_id, response
    ))
    forward.push_object_game(5202, response.SerializeToString(), [dynamic_id])


def publish_mahjong_to_self(dynamic_id):
    response = game_mahjong_pb2.m_5203_toc()
    func.log_info('[game] 5203 publish_mahjong_to_self dynamic_id: {}, response: {}'.format(
            dynamic_id, response))
    forward.push_object_game(5203, response.SerializeToString(), [dynamic_id])


def publish_mahjong_to_room(player, execute_account_id, card_list, card_id, operator_account_id, operator_list):
    response = game_mahjong_pb2.m_5204_toc()
    response.execute_account_id = execute_account_id
    response.card = card_id
    for _card_id in card_list:
        response.card_list.append(_card_id)
    response.operator_able = player.account_id == operator_account_id
    for operator in operator_list:
        response.operator.append(operator)
    func.log_info('[game] 5204 publish_mahjong_to_room dynamic_id: {}, account_id: {}, response: {}'.format(
        player.dynamic_id, player.account_id, response
    ))
    forward.push_object_game(5204, response.SerializeToString(), [player.dynamic_id])


def send_mahjong_operator(dynamic_id_list, execute_account_id, operator, card_list):
    response = game_mahjong_pb2.m_5205_toc()
    response.execute_account_id = execute_account_id
    response.operator = operator
    for card_id in card_list:
        response.cards.append(card_id)
    func.log_info('[game] 5205 send_mahjong_operator dynamic_id_list: {}, response: {}'.format(
            dynamic_id_list, response
    ))
    forward.push_object_game(5205, response.SerializeToString(), dynamic_id_list)


def send_mahjong_operator_select(dynamic_id, operator_able, operators):
    response = game_mahjong_pb2.m_5206_toc()
    response.operator_able = operator_able
    for operator in operators:
        response.operator.append(operator)
    func.log_info('[game] 5206 send_mahjong_operator_select dynamic_id: {}, response: {}'.format(
        dynamic_id, response
    ))
    forward.push_object_game(5206, response.SerializeToString(), [dynamic_id])


def send_mahjong_room_full(dynamic_id_list, statistic_list):
    response = game_mahjong_pb2.m_5207_toc()
    response.server_t = func.time_get()
    for info in statistic_list:
        room_fulls = response.room_fulls.add()
        room_fulls.account_id = info['account_id']
        room_fulls.rank = info['rank']
        room_fulls.point_change = info['point_change']
        room_fulls.max_point = info['max_point']
        room_fulls.max_point = info['drawn_count']
        room_fulls.win_count = info['win_count']
        room_fulls.lose_count = info['lose_count']
        room_fulls.lose_count = info['help_count']
    func.log_info('[game] 5207 send_mahjong_room_full dynamic_id_list: {}, response: {}'.format(
         dynamic_id_list, response
    ))
    forward.push_object_game(5207, response.SerializeToString(), dynamic_id_list)


def broad_mahjong_dispatch_card(dynamic_id_list, account_id):
    response = game_mahjong_pb2.m_5208_toc()
    response.account_id = account_id
    func.log_info('[game] 5208 broad_mahjong_dispatch_card dynamic_id_list: {}, account_id: {}'.format(
        dynamic_id_list, account_id
    ))
    forward.push_object_game(5208, response.SerializeToString(), dynamic_id_list)


def sync_play_history(room):
    history_data = room.get_per_play_history()
    read_list = room.room_ready_list
    request_gate_node('game_add_play_history', read_list, history_data)


