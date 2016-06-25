# coding:utf8
from app.gate.timer.TimeBase import ITimer
from app.gate.action import login
from app.util.common import func


class HeartTickTimer(ITimer):

    def do(self):
        self.start(60)
        login.check_heart_tick_time_out()
        func.log_info('[gate] HeartTimer check do')

