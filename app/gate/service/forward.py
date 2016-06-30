# coding:utf8
from firefly.server.globalobject import rootserviceHandle, GlobalObject
from app.gate.gateservice import gate_service
from app.gate.core.UserManager import UserManager


@rootserviceHandle
def forwarding(target_key, dynamic_id, data):
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
    push_object_gate(target_key, msg, send_list)


def push_object_gate(target_key, msg, send_list):
    GlobalObject().root.callChild('net', 'push_object_gate', target_key, msg, send_list)


def push_object_gate_all(target_key, msg):
    send_list = UserManager().get_all_dynamic_id()
    push_object_gate(target_key, msg, send_list)

