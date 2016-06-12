# coding:utf8
from firefly.server.globalobject import GlobalObject
from firefly.utils.services import CommandService


class GateCommandService(CommandService):

    def is_target_local(self, target_key):
        return target_key in self._targets


gate_service = GateCommandService('GateService')


def gate_service_handle(target):
    gate_service.mapTarget(target)


def request_child_node(node_name, target_key, *args, **kwargs):
    return GlobalObject().root.callChild(node_name, target_key, *args, **kwargs)


def request_all_game_node(target_key, *args, **kwargs):
    result = dict()
    for node_name in GlobalObject().root.childsmanager._childs.keys():
        if 'game' in node_name:
            result[node_name] = request_child_node(node_name, target_key, *args, **kwargs)
    return result

