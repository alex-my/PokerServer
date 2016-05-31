# coding:utf8

from firefly.server.globalobject import GlobalObject, remoteserviceHandle


@remoteserviceHandle('auth')
def push_object_auth(target_key, data, send_list):
    """
    消息从auth推送到客户端
    :param target_key: 协议ID
    :param data:
    :param send_list: [dynamic_id, ...]
    :return:
    """
    GlobalObject().netfactory.pushObject(target_key, data, send_list)


@remoteserviceHandle('gate')
def push_object_gate(target_key, data, send_list):
    """
    消息从gate推送到客户端
    :param target_key: 协议ID
    :param data:
    :param send_list: [dynamic_id, ...]
    :return:
    """
    GlobalObject().netfactory.pushObject(target_key, data, send_list)

