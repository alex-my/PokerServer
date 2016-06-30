# coding:utf8
from firefly.server.globalobject import rootserviceHandle
from app.gate.gateservice import gate_service_handle
from app.gate.action import room
from app.util.proto import room_pb2


@gate_service_handle
def create_room_3001(dynamic_id, proto):
    argument = room_pb2.m_3001_tos()
    argument.ParseFromString(proto)
    room.create_room(dynamic_id, argument.room_type, argument.rounds, argument.help)
    return None


@gate_service_handle
def enter_room_3002(dynamic_id, proto):
    """
    enter/resume room
    :param dynamic_id:
    :param proto:
    :return:
    """
    argument = room_pb2.m_3002_tos()
    argument.ParseFromString(proto)
    room.enter_room(dynamic_id, argument.room_id)
    return None


@rootserviceHandle
def enter_room_gate(account_id, dynamic_id, node_name, room_id, room_data, operator_account_id, player_operators):
    room.enter_room_confirm(account_id, dynamic_id, node_name, room_id, room_data,
                            operator_account_id, player_operators)
    return None


@rootserviceHandle
def remove_room_id(account_id, room_id):
    room.remove_room_id(account_id, room_id)
    return None


@rootserviceHandle
def remove_room(room_id):
    room.remove_room(room_id)
    return None


@gate_service_handle
def query_play_history_3201(dynamic_id, proto):
    room.query_play_history(dynamic_id)
    return None


@gate_service_handle
def online_match_3202(dynamic_id, proto):
    argument = room_pb2.m_3202_tos()
    argument.ParseFromString(proto)
    room.online_match(dynamic_id, argument.room_type)
    return None


@gate_service_handle
def cancel_online_match_3204(dynamic_id, proto):
    room.cancel_online_match(dynamic_id)
    return None

