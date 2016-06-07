# coding:utf8
from firefly.server.globalobject import rootserviceHandle, GlobalObject
from app.auth.authservice import auth_service
from app.util.common import func


@rootserviceHandle
def forwarding(target_key, dynamic_id, address, data):
    """
    转发来自net消息
    :param target_key: 协议ID
    :param dynamic_id: 客户端动态ID
    :param address: IP地址/端口 ('127.0.0.132', 64801)
    :param data: 数据
    :return:
    """
    if auth_service.is_target_local(target_key):
        return auth_service.callTarget(target_key, dynamic_id, address, data)
    else:
        func.log_error('target_key: {} do not exist in auth'.format(target_key), func.__function_pos__())
        return None


def push_object(target_key, msg, send_list):
    """
    推送消息到net
    :param target_key: 协议ID
    :param msg:
    :param send_list: [dynamic_id, ...]
    :return:
    """
    GlobalObject().root.callChild('net', 'push_object_auth', target_key, msg, send_list)
