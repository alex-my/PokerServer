# coding:utf8

from firefly.server.globalobject import GlobalObject
from app.util.common import protocol
from app.util.common import func


def do_when_stop():
    func.log_info('[net] ---------------------------> node do_when_stop <-----------------------')


GlobalObject().stophandler = do_when_stop


def call_when_connect_lost(conn):
    dynamic_id = conn.transport.sessionno
    GlobalObject().remote['gate'].callRemote('net_connect_lost', dynamic_id)


GlobalObject().netfactory.doConnectionLost = call_when_connect_lost
data_pack_proto = protocol.DataPackProto()  # 协议头
GlobalObject().netfactory.setDataProtocl(data_pack_proto)


def load_module():
    import netforwarding
    import transporttonet
