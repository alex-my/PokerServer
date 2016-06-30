# coding:utf8
from firefly.server.globalobject import GlobalObject
from firefly.utils.services import CommandService
from twisted.internet import defer

from app.util.common import func


class NetCommandService(CommandService):

    def callTargetSingle(self, target_key, *args, **kw):
        self._lock.acquire()
        target = self.getTarget(0)
        try:
            if not target:
                func.log_info('[Net callTargetSingle] the command ' + str(target_key) + ' not Found on service')
                return None
            if target_key not in self.unDisplay:
                func.log_info('[Net] call method {} on service'.format(target.__name__))
            defer_data = target(target_key, *args, **kw)
            if not defer_data:
                return None
            if isinstance(defer_data, defer.Deferred):
                return defer_data
            d = defer.Deferred()
            d.callback(defer_data)
        finally:
            self._lock.release()
        return d


net_service = NetCommandService('NetService')
GlobalObject().netfactory.addServiceChannel(net_service)


def network_service_handle(target):
    net_service.mapTarget(target)


@network_service_handle
def forwarding_0(target_key, _conn, data):
    if target_key >= 2000:
        return GlobalObject().remote['gate'].callRemote("forwarding",
                                                        target_key,
                                                        _conn.transport.sessionno,
                                                        data)
    else:
        return GlobalObject().remote['auth'].callRemote("forwarding",
                                                        target_key,
                                                        _conn.transport.sessionno,
                                                        _conn.transport.client,
                                                        data)
