# coding:utf8
from firefly.server.globalobject import remoteserviceHandle
from app.game.gameservice import game_service, request_gate_node
from app.util.common import func


def push_object_game(target_key, msg, send_list):
    request_gate_node('push_object', target_key, msg, send_list)


@remoteserviceHandle('gate')
def forwarding_game(target_key, dynamic_id, data):
    """
    dispatch
    :param target_key:
    :param dynamic_id:
    :param data:
    :return:
    """
    func.log_info('[game] forwarding_game, target_key: {}, dynamic_id: {}'.format(target_key, dynamic_id))
    if game_service.is_target_local(target_key):
        game_service.callTarget(target_key, dynamic_id, data)
    else:
        func.log_exception('[game] target_key: {} not in game service'.format(target_key))
