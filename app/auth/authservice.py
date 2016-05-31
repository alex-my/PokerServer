# coding:utf8
from firefly.server.globalobject import GlobalObject
from firefly.utils.services import CommandService


class AuthCommandService(CommandService):

    def is_target_local(self, target_key):
        return target_key in self._targets


auth_service = AuthCommandService('AuthService')


def auth_service_handle(target):
    auth_service.mapTarget(target)


def request_gate_node(target_key, *args, **kwargs):
    GlobalObject().root.callChild('gate', target_key, *args, **kwargs)
