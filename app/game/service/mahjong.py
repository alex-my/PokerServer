# coding:utf8
from app.game.gameservice import game_service_handle
from app.game.action import mahjong, play
from app.util.proto import game_mahjong_pb2


@game_service_handle
def mahjong_publish_5203(dynamic_id, proto):
    argument = game_mahjong_pb2.m_5203_tos()
    argument.ParseFromString(proto)
    mahjong.mahjong_publish(dynamic_id, argument.card)
    return None


@game_service_handle
def mahjong_operator_5205(dynamic_id, proto):
    argument = game_mahjong_pb2.m_5205_tos()
    argument.ParseFromString(proto)
    mahjong.mahjong_operator(dynamic_id, argument.operator, argument.cards)
    return None


@game_service_handle
def mahjong_switch_5210(dynamic_id, proto):
    argument = game_mahjong_pb2.m_5210_tos()
    argument.ParseFromString(proto)
    play.mahjong_switch_over(dynamic_id, argument.craps)
    return None
