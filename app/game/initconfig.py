# coding:utf8
from firefly.server.globalobject import GlobalObject
from app.game.core.RoomManager import RoomManager
from app.util.common.config import Config
from app.util.common import func


def do_when_stop():
    func.log_info('[game] ---------------------------> node do_when_stop begin')
    for room_id, room in RoomManager().rooms.items():
        try:
            if not room:
                continue
            room.room_save()
        except Exception as e:
            func.log_error('[game] room save room_id: {}, error: {} room_data: {}'.format(
                room_id, e.message, room.get_save_data()
            ))
    func.log_info('[game] node do_when_stop end <-----------------------')


GlobalObject().stophandler = do_when_stop


def load_module():
    import gameservice
    import service
    import app.util.defines.games

    Config().load_configs()
