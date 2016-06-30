# coding:utf8
from firefly.server.globalobject import GlobalObject, remoteserviceHandle


@remoteserviceHandle('auth')
def push_object_auth(target_key, data, send_list):
    GlobalObject().netfactory.pushObject(target_key, data, send_list)


@remoteserviceHandle('gate')
def push_object_gate(target_key, data, send_list):
    GlobalObject().netfactory.pushObject(target_key, data, send_list)

