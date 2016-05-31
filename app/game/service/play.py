# coding:utf8
from app.game.gameservice import game_service_handle
from app.game.action import play
from app.util.proto import play_pb2


@game_service_handle
def user_ready_4001(dynamic_id, proto):
    """
    user ready for game
    :param dynamic_id:
    :param proto:
    :return:
    """
    argument = play_pb2.m_4001_tos()
    argument.ParseFromString(proto)
    play.user_operator(dynamic_id, argument.operate)
    return None
