# coding:utf8

from firefly.server.globalobject import remoteserviceHandle, rootserviceHandle, GlobalObject
from app.gate.core.UserManager import UserManager
from app.util.common import func


@remoteserviceHandle('auth')
def notice_user_login_verify(account_id, verify_key, address):
    """
    消息从gate推送到客户端
    :param account_id:
    :param verify_key:
    :param address: ('127.0.0.132', 64801)
    :return:
    """
    func.log_info('[user verify] account_id: {} \t verify_key: {}, address: {}'.format(
            account_id, verify_key, address))
    UserManager().record_verify_key(account_id, verify_key, address)
    return None


@rootserviceHandle
def net_connect_lost(dynamic_id):
    """
    客户端断开连接时处理
    :param dynamic_id:
    :return:
    """
    user = UserManager().get_user_by_dynamic(dynamic_id)
    if user:
        func.log_info('[gate] net_connect_lost dynamic_id: {}, account_id: {}, node_name: {}'.format(
            dynamic_id, user.account_id, user.node_name
        ))
        if user.node_name:
            GlobalObject().root.callChild(user.node_name, 'user_connect_lost', dynamic_id)
        UserManager().drop_user_dynamic(dynamic_id)
    return None

