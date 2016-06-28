# coding:utf8
from app.gate.gateservice import request_all_game_node
from app.gate.core.UserManager import UserManager
from app.gate.core.User import User
from app.gate.action import send, change
from app.util.common import func
from app.util.common.config import i
from app.util.defines import content, dbname, origins, informations, constant
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
    contact = i(informations.INFOMATION_TYPE_CONTACT)
    if contact:
        send.marquee_to_user(dynamic_id, contact)
    else:
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
    proxy_stastics(proxy_id)
    change.award_gold(user, constant.GOLD_BIND_PROXY, origins.ORIGIN_PROXY_ACTIVE)
    # save
    user.user_save()
    send.bind_success(dynamic_id, proxy_id)
    send.system_notice(dynamic_id, content.PROXY_ID_SUCCESS)
    func.log_info('[gate] bind_proxy account_id: {} bind proxy_id: {}'.format(user.account_id, proxy_id))


def proxy_stastics(proxy_id):
    user = UserManager().get_user(proxy_id)
    if user:
        user.proxy_count = 1
        func.log_info('[gate] proxy_stastics proxy_id: {} online add one'.format(proxy_id))
    else:
        sql = 'update {} set proxy_count = proxy_count + {} where account_id = {}'.format(
            dbname.DB_ACCOUNT, 1, proxy_id
        )
        try:
            dbexecute.execute(sql)
            func.log_info('[gate] proxy_stastics proxy_id: {} offline add one'.format(proxy_id))
        except Exception as e:
            func.log_error('[gate] proxy_stastics proxy_id: {}, sql: {}, error: {}'.format(
                proxy_id, sql, e.message
            ))


def heart_tick(dynamic_id):
    user = UserManager().get_user_by_dynamic(dynamic_id)
    if not user:
        func.log_error('[gate] dynamic_id: {} not find'.format(dynamic_id))
        return
    UserManager().heart_tick(user.account_id)
    send.send_heart_tick(dynamic_id)


def check_heart_tick_time_out():
    t = func.time_get()
    user_manager = UserManager()
    all_heart_ticks = user_manager.all_heart_tick
    time_out_list = []
    for account_id, pre_t in all_heart_ticks.items():
        if t - pre_t >= 75:        # 客户端30秒上传1次，75秒没有检测到，则判断为离线
            time_out_list.append(account_id)
    if time_out_list:
        func.log_warn('[gate] check_heart_tick_time_out {} user time out, {}'.format(
            len(time_out_list), time_out_list
        ))
        user_manager.remove_heart_tick(time_out_list)
        request_all_game_node('heart_tick_time_out', time_out_list)
