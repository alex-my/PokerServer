# coding:utf8
from app.gate.timer.TimeBase import ITimer
from app.gate.action import system
from app.util.common import func


class ClearTimer(ITimer):

    def do(self):
        self.start(12 * 3600)
        func.log_info('[gate] ClearTimer check do')
        system.clear_logs()
        system.clear_db_backup()
        system.backup_db()

