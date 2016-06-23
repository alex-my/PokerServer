# coding:utf8
import hashlib
from app.auth.action import send
from app.auth.authservice import request_gate_node
from app.util.common import func
from app.util.defines import channel, content, dbname
from app.util.driver import dbexecute


def account_register(dynamic_id, address, user_name, password):
    """
    账号注册
    :param dynamic_id:
    :param address:
    :param user_name:
    :param password:
    :return:
    """
    if not user_name or not password:
        send.system_notice(dynamic_id, content.ACCOUNT_NULL)
        return
    if not func.check_english(user_name):
        send.system_notice(dynamic_id, content.ACCOUNT_ENGLISH)
        return
    sql = 'select * from {} where user_name="{}"'.format(dbname.DB_ACCOUNT, user_name)
    if dbexecute.query_one(sql):
        send.system_notice(dynamic_id, content.ACCOUNT_EXIST)
        return
    uuid = user_name
    sex = func.random_get(1, 2)
    name = user_name
    head_frame = ''
    head_icon = ''
    account_id = _register_process(user_name, password, name, uuid, channel.CHANNEL_ZERO, sex, head_frame, head_icon)
    if account_id:
        func.log_info('[Auth] user_name: {}, account_id: {}, address: {} register success'.format(
                user_name, account_id, address))
        send.account_register(dynamic_id, user_name, password, account_id)
    else:
        func.log_error('[Auth] user_name: {} register failed'.format(user_name))


def _create_token_key(user_name, password):
    m = hashlib.md5()
    m.update(str(user_name) + str(func.time_get()) + str(password) + str(func.random_get(100, 500000)))
    return m.hexdigest()


def account_verify_official(dynamic_id, address, user_name, password):
    """
    官方登陆
    :param dynamic_id:
    :param address: ('127.0.0.132', 64801)
    :param user_name:
    :param password:
    :return:
    """
    if not user_name or not password:
        send.system_notice(dynamic_id, content.ACCOUNT_NULL)
        return
    if not func.check_english(user_name):
        send.system_notice(dynamic_id, content.ACCOUNT_ENGLISH)
        return
    sql = 'select * from {} where user_name="{}"'.format(dbname.DB_ACCOUNT, user_name)
    result = dbexecute.query_one(sql)
    if not result:
        send.system_notice(dynamic_id, content.ACCOUNT_DO_NOT_EXIST)
        return
    encrypt_password = func.encrypt_password(user_name, password, result['token_key'])
    if encrypt_password != result['password']:
        send.system_notice(dynamic_id, content.ACCOUNT_PASSWORD_ERROR)
        return
    account_id = result['account_id']
    verify_key = _create_verify_key(account_id, result['token_key'])
    notice_gate_user_login(account_id, verify_key, address)
    t = func.time_get()
    send.account_verify_official(dynamic_id, t, account_id, verify_key)


def account_verify_channel(dynamic_id, address, user_name, channel_id, uuid, name, head_frame, head_icon, sex):
    """
    渠道登陆
    :param dynamic_id:
    :param address: ('127.0.0.132', 64801)
    :param user_name:
    :param channel_id:
    :param uuid:
    :param name:
    :param head_frame:
    :param head_icon:
    :param sex:
    :return:
    """
    func.log_info('[auth] account_verify_channel dynamic_id: {}, user_name: {}, channel_id: {}, uuid: {}, head_frame: {}, head_icon: {}, sex: {}'.format(
            dynamic_id, user_name, channel_id, uuid, head_frame, head_icon, sex
    ))
    if not user_name or not uuid or channel_id < 0:
        send.system_notice(dynamic_id, content.ACCOUNT_LOGIN_ARGUMENT)
        return
    password = uuid
    sql = 'select * from {} where user_name="{}"'.format(dbname.DB_ACCOUNT, user_name)
    result = dbexecute.query_one(sql)
    if not result:
        account_id = _register_process(user_name, password, name, uuid, channel_id, sex, head_frame, head_icon)
        if not account_id:
            send.system_notice(dynamic_id, content.LOGIN_USER_CREATE_FAILED_51)
            return
        result = dbexecute.query_one(sql)
        if not result:
            send.system_notice(dynamic_id, content.LOGIN_USER_CREATE_FAILED_52)
            return
    encrypt_password = func.encrypt_password(user_name, password, result['token_key'])
    if encrypt_password != result['password']:
        send.system_notice(dynamic_id, content.LOGIN_USER_CREATE_FAILED_53)
        return
    account_id = result['account_id']
    verify_key = _create_verify_key(account_id, result['token_key'])
    notice_gate_user_channel_login(account_id, verify_key, address,
                                   name=name, sex=sex, head_frame=head_frame, head_icon=head_icon)
    t = func.time_get()
    send.account_verify_channel(dynamic_id, t, account_id, verify_key)


def _create_verify_key(account_id, token_key):
    m = hashlib.md5()
    m.update(str(account_id) + str(token_key) + str(func.time_get()) + str(func.random_get(10000, 500000)))
    return m.hexdigest()


def notice_gate_user_login(account_id, verify_key, address):
    request_gate_node('notice_user_login_verify', account_id, verify_key, address)


def notice_gate_user_channel_login(account_id, verify_key, address, **kwargs):
    request_gate_node('notice_user_channel_login_verify', account_id, verify_key, address, **kwargs)


def _register_process(user_name, password, name, uuid, channel_id, sex, head_frame, head_icon):
    token_key = _create_token_key(user_name, password)
    encrypt_password = func.encrypt_password(user_name, password, token_key)
    t = func.time_get()
    # 实时搜索最大的account_id
    sql = 'select `account_id` from {} order by `account_id` desc'.format(dbname.DB_ACCOUNT)
    result = dbexecute.query_one(sql)
    if not result:
        account_id = 380001
    else:
        account_id = calc_account_id(result['account_id'])
    account_data = {
        'account_id': account_id,
        'uuid': uuid,
        'cid': channel_id,
        'user_name': user_name,
        'password': encrypt_password,
        'token_key': token_key,
        'create_time': t,
        'last_login': t,
        'last_logout': t,
        'name': name,
        'sex': sex,
        'head_frame': head_frame,
        'head_icon': head_icon,
        'gold': 20000
    }
    if dbexecute.insert_record(**{'table': dbname.DB_ACCOUNT, 'data': account_data}) > 0:
        return account_id
    else:
        return 0


def calc_account_id(cur_account_id):
    for account_id in xrange(cur_account_id + 1, 99999999):
        str_account_id = str(account_id)
        if '4' in str_account_id:
            continue
        flag = True
        for c in str_account_id:
            if str_account_id.count(c) >= 5:
                flag = False
                break
        if flag:
            return account_id
    return cur_account_id + 1

