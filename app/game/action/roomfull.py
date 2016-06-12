# coding:utf8
from app.game.gameservice import request_gate_node
from app.game.core.RoomManager import RoomManager
from app.game.action import send
from app.util.defines import rule


def remove_room(room):
    # 从gate节点移除该房间
    request_gate_node('remove_room', room.room_id)
    # 计算本论统计信息
    statistic_list = room.get_room_statistic()
    # 将统计信息下发玩家
    dynamic_id_list = room.get_room_dynamic_id_list()
    if room.room_type in rule.GAME_LIST_POKER_PDK:
        send.send_poker_room_full(dynamic_id_list, statistic_list)
    elif room.room_type in rule.GAME_LIST_MAHJONG:
        send.send_mahjong_room_full(dynamic_id_list, statistic_list)
    # 从RoomManager移除房间信息
    RoomManager().drop_room(room)
