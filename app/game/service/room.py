# coding:utf8
from firefly.server.globalobject import remoteserviceHandle
from app.game.gameservice import game_service_handle
from app.game.action import room
from app.util.proto import room_pb2


@remoteserviceHandle('gate')
def enter_room_game(**kwargs):
    """
    enter or resume room
    :param kwargs:
    :return:
    """
    room.enter_room(**kwargs)
    return None


@remoteserviceHandle('gate')
def user_connect_lost(dynamic_id):
    """
    player go offline
    :param dynamic_id:
    :return:
    """
    room.leave_room(dynamic_id)
    return None


@remoteserviceHandle('gate')
def remove_unvalid_room(delete_id_list):
    """
    remove unvalid room
    :param delete_id_list:
    :return:
    """
    room.remove_unvalid_room(delete_id_list)
    return None


@game_service_handle
def room_short_message_3101(dynamic_id, proto):
    """
    player send short message
    :param dynamic_id:
    :param proto:
    :return:
    """
    argument = room_pb2.m_3101_tos()
    argument.ParseFromString(proto)
    room.room_short_message(dynamic_id, argument.message)
    return None


@game_service_handle
def room_voice_message_3103(dynamic_id, proto):
    """
    dispatch voice url
    :param dynamic_id:
    :param proto:
    :return:
    """
    argument = room_pb2.m_3103_tos()
    argument.ParseFromString(proto)
    room.room_voice_message(dynamic_id, argument.voice_url)
    return None


@remoteserviceHandle('gate')
def heart_tick_time_out(time_out_list):
    """
    heart tick time out
    :param time_out_list:
    :return:
    """
    room.game_heart_tick_time_out(time_out_list)
    return None

