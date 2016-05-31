# coding:utf8
from app.gate.gateservice import gate_service_handle
from app.gate.action import login
from app.util.proto import login_pb2


@gate_service_handle
def user_login_2001(dynamic_id, proto):
    """
    玩家进入游戏
    :param dynamic_id:
    :param proto:
    :return:
    """
    argument = login_pb2.m_2001_tos()
    argument.ParseFromString(proto)
    login.user_login(dynamic_id, argument.account_id, argument.verify_key)
    return None
