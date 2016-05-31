# coding:utf8
from app.game.gameservice import game_service_handle
from app.game.action import poker
from app.util.proto import game_poker_pb2


@game_service_handle
def poker_publish_5101(dynamic_id, proto):
    """
    user publish
    :param dynamic_id:
    :param proto:
    :return:
    """
    argument = game_poker_pb2.m_5101_tos()
    argument.ParseFromString(proto)
    poker.poker_publish(dynamic_id, argument.cards)
    return None
