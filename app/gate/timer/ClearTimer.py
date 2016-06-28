# coding:utf8
from app.gate.timer.TimeBase import ITimer
from app.gate.core.RoomProxyManager import RoomProxyManager
from app.gate.action import system
from app.util.common import func


class ClearTimer(ITimer):

    def do(self):
        interval = func.next_interval(5, 0, 0)
        self.start(interval)
        func.log_info('[gate] ClearTimer check do, next: {}'.format(interval))
        system.clear_logs()
        system.clear_db_backup()
        system.backup_db()
        RoomProxyManager().clear_unvalid_room()

