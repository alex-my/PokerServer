# coding:utf8
from app.game.core.PlayerManager import PlayerManager
from app.game.core.RoomManager import RoomManager
from app.game.action import send, play
from app.util.common import func
from app.util.defines import content


def dispatch_mahjong_card(dynamic_id, card):
    send.dispatch_mahjong_card(dynamic_id, card)


def mahjong_publish(dynamic_id, card):
    pass
