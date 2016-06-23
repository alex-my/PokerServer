# coding:utf8

from firefly.server.globalobject import remoteserviceHandle, rootserviceHandle, GlobalObject
from app.gate.core.UserManager import UserManager
from app.util.common import func
from app.util.defines import dbname
from app.util.driver import dbexecute


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


@remoteserviceHandle('auth')
def notice_user_channel_login_verify(account_id, verify_key, address, **kwargs):
    """
    消息从gate推送到客户端
    :param account_id:
    :param verify_key:
    :param address: ('127.0.0.132', 64801)
    :param kwargs:
    :return:
    """
    func.log_info('[user channel verify] account_id: {} \t verify_key: {}, address: {}'.format(
            account_id, verify_key, address))
    UserManager().record_verify_key(account_id, verify_key, address)
    user = UserManager().get_user(account_id)
    if user:
        user.sync_information(**kwargs)
    else:
        try:
            change_info = dict()
            if kwargs.get('name'):
                change_info['name'] = kwargs.get('name')
            if kwargs.get('sex'):
                change_info['sex'] = kwargs.get('sex')
            if kwargs.get('head_frame'):
                change_info['head_frame'] = kwargs.get('head_frame')
            if kwargs.get('head_icon'):
                change_info['head_icon'] = kwargs.get('head_icon')
            if change_info:
                dbexecute.update_record(
                    table=dbname.DB_ACCOUNT,
                    where={'account_id': account_id},
                    data=change_info
                )
        except Exception as e:
            func.log_error('[gate] notice_user_channel_login_verify account_id: {}, failed: {}'.format(
                    account_id, e.message))
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
        user.user_lost()
        if user.node_name:
            GlobalObject().root.callChild(user.node_name, 'user_connect_lost', dynamic_id)
        UserManager().drop_user_dynamic(dynamic_id)
    return None

