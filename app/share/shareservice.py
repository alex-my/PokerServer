# coding:utf8
from firefly.server.globalobject import GlobalObject
from firefly.utils.services import CommandService


class ShareCommandService(CommandService):

    def is_target_local(self, target_key):
        return target_key in self._targets


share_service = ShareCommandService('ShareService')


def share_service_handle(target):
    share_service.mapTarget(target)


def request_gate_node(target_key, *args, **kwargs):
    return GlobalObject().remote['gate'].callRemote(target_key, *args, **kwargs)


def request_child_node(node_name, target_key, *args, **kwargs):
    return GlobalObject().root.callChild(node_name, target_key, *args, **kwargs)


def request_all_game_node(target_key, *args, **kwargs):
    result = dict()
    for node_name in GlobalObject().root.childsmanager._childs.keys():
        if 'game' in node_name:
            result[node_name] = request_child_node(node_name, target_key, *args, **kwargs)
    return result
