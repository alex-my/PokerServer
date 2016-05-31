# coding:utf8

from firefly.server.globalobject import GlobalObject
from app.util.common import protocol


def call_when_connect_lost(conn):
    dynamic_id = conn.transport.sessionno
    GlobalObject().remote['gate'].callRemote('net_connect_lost', dynamic_id)


GlobalObject().netfactory.doConnectionLost = call_when_connect_lost
data_pack_proto = protocol.DataPackProto()  # 协议头
GlobalObject().netfactory.setDataProtocl(data_pack_proto)


def load_module():
    import netforwarding
    import transporttonet
