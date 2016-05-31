# coding:utf8
from firefly.server.globalobject import rootserviceHandle, GlobalObject
from app.gate.gateservice import gate_service
from app.gate.core.UserManager import UserManager


@rootserviceHandle
def forwarding(target_key, dynamic_id, data):
    """
    转发来自net消息
    :param target_key: 协议ID
    :param dynamic_id: 客户端动态ID
    :param data: 数据
    :return:
    """
    if gate_service.is_target_local(target_key):
        return gate_service.callTarget(target_key, dynamic_id, data)
    else:
        user = UserManager().get_user_by_dynamic(dynamic_id)
        if not user:
            return False
        if user.is_lock():
            return False
        # it bind when user enter the room
        # it clear when user get out
        node_name = user.node_name
        if node_name:
            return GlobalObject().root.callChild(node_name, 'forwarding_game', target_key, dynamic_id, data)
        return False


@rootserviceHandle
def push_object(target_key, msg, send_list):
    """
    推送消息到net
    :param target_key: 协议ID
    :param msg:
    :param send_list: [dynamic_id, ...]
    :return:
    """
    push_object_gate(target_key, msg, send_list)


def push_object_gate(target_key, msg, send_list):
    GlobalObject().root.callChild('net', 'push_object_gate', target_key, msg, send_list)

