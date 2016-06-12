# coding:utf8
from app.gate.timer.MarqueeTimer import MarqueeTimer


def start_all_timer():
    MarqueeTimer().start(60)


def stop_all_timer():
    MarqueeTimer().stop()


