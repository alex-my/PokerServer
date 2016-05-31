# coding:utf8
from app.game.gameservice import game_service_handle
from app.game.action import mahjong
from app.util.proto import game_mahjong_pb2


@game_service_handle
def mahjong_publish_5202(dynamic_id, proto):
    """
    user publish
    :param dynamic_id:
    :param proto:
    :return:
    """
    argument = game_mahjong_pb2.m_5202_tos()
    argument.ParseFromString(proto)
    mahjong.mahjong_publish(dynamic_id, argument.card)
    return None
