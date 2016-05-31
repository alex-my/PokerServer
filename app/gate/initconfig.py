# coding:utf8
from app.gate.core.RoomProxyManager import RoomProxyManager


def load_module():
    import gateservice
    import service

    RoomProxyManager().load_all_room()
    RoomProxyManager().load_configs()
