# coding:utf8
from app.gate.gateservice import gate_service_handle
from app.gate.action import recharge
from app.util.proto import recharge_pb2


@gate_service_handle
def get_wechat_prepay_info_9101(dynamic_id, proto):
    """
    客户端获取微信预充值信息
    :param dynamic_id:
    :param proto:
    :return:
    """
    argument = recharge_pb2.m_9101_tos()
    argument.ParseFromString(proto)
    recharge.get_wechat_prepay_info(dynamic_id, argument.money)
    return None
