# coding:utf8
from app.gate.timer.TimeBase import ITimer
from app.gate.action import send
from app.util.common.config import i
from app.util.common import func
from app.util.defines import informations


class MarqueeTimer(ITimer):

    def do(self):
        self.start(30 * 60)

        func.log_info('[gate] MarqueeTimer do')
        content = i(informations.INFOMATION_TYPE_MARQUEE)
        if not content:
            return
        send.marquee_to_all(content)
