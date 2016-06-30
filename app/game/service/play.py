# coding:utf8
from app.game.gameservice import game_service_handle
from app.game.action import play
from app.util.proto import play_pb2


@game_service_handle
def user_ready_4001(dynamic_id, proto):
    argument = play_pb2.m_4001_tos()
    argument.ParseFromString(proto)
    play.user_operator(dynamic_id, argument.operate)
    return None


@game_service_handle
def user_switch_over_4005(dynamic_id, proto):
    play.user_switch_over(dynamic_id)
    return None
