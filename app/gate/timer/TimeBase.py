# coding:utf8
from twisted.internet import reactor
from firefly.utils.singleton import Singleton
from app.util.common import func


reactor = reactor


class ITimer(object):

    __metaclass__ = Singleton

    def __init__(self):
        self._timer = None

    def start(self, interval):
        if interval <= 0:
            raise ValueError('[gate] ITimer interval: {} mush big than zero.'.format(interval))
        self._timer = reactor.callLater(interval, self.do)

    def do(self):
        raise Exception('[gate] ITimer unable to come here.')

    def stop(self):
        if self._timer:
            try:
                self._timer.cancel()
            except Exception as e:
                func.log_error('[game] ITimer stop failed, error: {}'.format(e.message))
            finally:
                self._timer = None
