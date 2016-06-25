# coding:utf8
from app.gate.timer.MarqueeTimer import MarqueeTimer
from app.gate.timer.HeartTickTimer import HeartTickTimer


def start_all_timer():
    MarqueeTimer().start(60)
    HeartTickTimer().start(120)


def stop_all_timer():
    MarqueeTimer().stop()
    HeartTickTimer().stop()


