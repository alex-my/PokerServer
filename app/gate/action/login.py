# coding:utf8
from app.gate.core.UserManager import UserManager
from app.gate.core.User import User
from app.gate.action import send, change
from app.util.common import func
from app.util.defines import content, dbname, origins
from app.util.driver import dbexecute


def user_login(dynamic_id, account_id, verify_key):
    """
    玩家登陆
    :param dynamic_id:
    :param account_id:
    :param verify_key:
    :return:
    """
    if not account_id or not verify_key:
        send.system_notice(dynamic_id, content.ACCOUNT_NULL)
        return
    func.log_info('[user_login] account_id: {}, verify_key: {}'.format(account_id, verify_key))
    if not UserManager().check_verify_key(account_id, verify_key):
        send.system_notice(dynamic_id, content.LOGIN_VERIFY_FAILED)
        return
    sql = 'select * from {} where `account_id`={}'.format(dbname.DB_ACCOUNT, account_id)
    result = dbexecute.query_one(sql)
    if not result:
        send.system_notice(dynamic_id, content.ACCOUNT_REGISTER_FIRST)
        return
    user = User()
    if not user.init_user(result):
        send.system_notice(dynamic_id, content.LOGIN_USER_INIT_FAILED)
        return
    if user.is_lock():
        _user_lock_tips(user)
        return
    # load play history
    load_play_history(user)

    address = UserManager().get_user_address(account_id)
    user.record_address(address)
    user.dynamic_id = dynamic_id
    UserManager().add_user(user)
    send.login_success(dynamic_id, user)
    # 清理最后的房间
    user.room_id, user.room_type = 0, 0
    user.record_room_id, user.record_room_type = 0, 0
    # 推送信息
    send.marquee_to_user(dynamic_id, content.LOGIN_NOTICE)


def _user_lock_tips(user):
    if user.is_lock_forever():
        send.system_notice(user.dynamic_id, content.LOGIN_USER_LOCKED_FOREVER)
    else:
        send.system_notice(user.dynamic_id, content.LOGIN_USER_LOCKED_TIME.format(user.lock_expire))


def load_play_history(user):
    sql = 'select * from {} where `account_id`={}'.format(dbname.DB_HISTORY, user.account_id)
    result = dbexecute.query_one(sql)
    if result:
        if result['data']:
            result['data'] = func.parse_pickle_to_object(result['data'])
        user.init_history(result['data'])
    else:
        insert_data = {
            'account_id': user.account_id,
            'data': func.transform_object_to_pickle(dict())
        }
        dbexecute.insert_update_record(**{'table': dbname.DB_HISTORY, 'data': insert_data})


def bind_proxy(dynamic_id, proxy_id):
    if not proxy_id:
        send.system_notice(dynamic_id, content.PROXY_ID_LACK)
        return
    sql = 'select account_id from {} where account_id = {}'.format(dbname.DB_ACCOUNT, proxy_id)
    if not dbexecute.query_one(sql):
        send.system_notice(dynamic_id, content.PROXY_ID_ERROR)
        return
    user = UserManager().get_user_by_dynamic(dynamic_id)
    if not user:
        send.system_notice(dynamic_id, content.ENTER_DYNAMIC_LOGIN_EXPIRE)
        return
    if user.proxy_id > 0:
        send.system_notice(dynamic_id, content.PROXY_ID_EXIST)
        return
    user.proxy_id = proxy_id
    change.award_gold(user, 1000, origins.ORIGIN_PROXY_ACTIVE)
    func.log_info('[gate] bind_proxy account_id: {} bind proxy_id: {}'.format(user.account_id, proxy_id))

