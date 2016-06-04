# coding:utf8
from app.auth.authservice import auth_service_handle
from app.auth.action import account
from app.util.proto import login_pb2


@auth_service_handle
def account_register_1001(dynamic_id, proto):
    """
    账号注册
    :param dynamic_id:
    :param proto:
    :return:
    """
    argument = login_pb2.m_1001_tos()
    argument.ParseFromString(proto)
    account.account_register(dynamic_id, argument.user_name, argument.password)


@auth_service_handle
def account_verify_1002(dynamic_id, proto):
    """
    官方裸包登陆游戏
    :param dynamic_id:
    :param proto:
    :return:
    """
    argument = login_pb2.m_1002_tos()
    argument.ParseFromString(proto)
    account.account_verify_official(dynamic_id, argument.user_name, argument.password)


@auth_service_handle
def account_channel_verify_1003(dynamic_id, proto):
    """
    渠道包登陆游戏
    :param dynamic_id:
    :param proto:
    :return:
    """
    argument = login_pb2.m_1003_tos()
    argument.ParseFromString(proto)
    account.account_verify_channel(dynamic_id, argument.user_name, argument.channel_id, argument.uuid,
                                   argument.name, argument.head_frame, argument.head_icon, argument.sex)

