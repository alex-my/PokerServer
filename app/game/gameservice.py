# coding:utf8
from twisted.internet import defer
from firefly.server.globalobject import GlobalObject
from firefly.utils.services import CommandService

from app.util.common import func


class GameCommandService(CommandService):

    def is_target_local(self, target_key):
        return target_key in self._targets


game_service = GameCommandService(str(func.random_get(1, func.time_get())))


def game_service_handle(target):
    game_service.mapTarget(target)


def push_object(target_key, msg, send_list):
    func.log_info('[push_object] target_key: {}, send_list: {}'.format(target_key, send_list))


def push_all_game(target_key, msg):
    pass    # TODO: gameservice: push_all_game


def request_gate_node(target_key, *args, **kwargs):
    return GlobalObject().remote['gate'].callRemote(target_key, *args, **kwargs)


def request_share_node(target_key, *args, **kwargs):
    return GlobalObject().remote['share'].callRemote(target_key, *args, **kwargs)

