# coding:utf8
from app.gate.core.UserManager import UserManager
from app.gate.action import send, change
from app.util.common import func, recharge_wechat
from app.util.defines import content, dbname, origins, recharges
from app.util.driver import dbexecute


def test_wechat_prepay_id(money, proxy_id, ip='127.0.0.1'):
    pay = recharge_wechat.WechatPay()
    pay.init(
        nonce_str=func.random_string_r(16, 30),
        attach=str(proxy_id),
        order_id=recharge_wechat.generator_unique_order_id(money),
        total_fee=money,
        spbill_create_ip=ip
    )
    pay.re_finall()


def get_wechat_prepay_info(dynamic_id, money):
    func.log_info('[gate] get_wechat_prepay_info money: {}'.format(money))
    # if not proxy_id:
    #     send.system_notice(dynamic_id, content.RECHARGE_PROXY_ID_NEED)
    #     return
    if not money or not isinstance(money, int):
        send.system_notice(dynamic_id, content.RECHARGE_MONEY_IS_NEED)
        return
    if money >= 10000000:     # 10W元
        send.system_notice(dynamic_id, content.RECHARGE_MONEY_TO_LARGE)
        return
    # Alex
    money = 1
    user = UserManager().get_user_by_dynamic(dynamic_id)
    if not user:
        send.system_notice(dynamic_id, content.ENTER_DYNAMIC_LOGIN_EXPIRE)
        return
    if not user.proxy_id:
        send.system_notice(dynamic_id, content.RECHARGE_PROXY_ID_NEED)
        return
    proxy_id = user.proxy_id
    pay = recharge_wechat.WechatPay()
    pay.init(
            nonce_str=func.random_string_r(16, 30),
            attach='{}/{}'.format(proxy_id, user.account_id),
            order_id=recharge_wechat.generator_unique_order_id(money),
            total_fee=money,
            spbill_create_ip=user.ip
    )
    prepay_info = pay.re_finall()
    func.log_info('[gate] get_wechat_prepay_info account_id: {}, order_id: {}, prepay_info: {}'.format(
        user.account_id, pay.order_id, prepay_info
    ))
    send.recharge_wechat_prepay_info(dynamic_id, money, proxy_id, prepay_info)


def wechat_recharge_success(notice_content):
    if not notice_content:
        return
    func.log_info('[gate] wechat_recharge_success content:\n {}'.format(notice_content))
    pay = recharge_wechat.WechatResponse(notice_content)
    func.log_info('[gate] wechat_recharge_success pay.xml_json:\n {}'.format(pay.xml_json))
    xml_json = pay.xml_json

    proxy_id, account_id = pay.attach
    if not proxy_id or not account_id:
        return

    user = UserManager().get_user(account_id)
    if not user:
        func.log_error('[gate] wechat_recharge_success account_id: {} un exist'.format(account_id))
        return

    pay.init(
        nonce_str=xml_json['nonce_str'],
        attach=xml_json['attach'],
        order_id=xml_json['out_trade_no'],
        total_fee=xml_json['total_fee'],
        spbill_create_ip=''     # IP不参与签名
    )

    if check_repeated_order_from_db(pay):
        func.log_error('[gate] wechat_recharge_success repeated order notice account_id: {}, proxy_id: {}'.format(
            account_id, proxy_id
        ))
        return

    money = pay.money
    if pay.verify():
        recharge_gold = calc_money_to_gold(money)
        save_order_to_db(pay, recharge_gold, origins.ORIGIN_RECHARGE_WECHAT)
        change.award_gold(user, recharge_gold, origins.ORIGIN_RECHARGE_MONEY)
        # statistic
        recharge_statistic_self(user, money)
        recharge_statistic_proxy(user.proxy_id, money)
        func.log_info('[gate] wechat_recharge_success account_id: {}, money: {} SUCCESS'.format(
            account_id, money
        ))
    else:
        func.log_info('[gate] wechat_recharge_success account_id: {}, money: {} FAILED'.format(
            account_id, money
        ))


def recharge_statistic_self(user, money):
    _month = func.month_now()
    if _month != user.month:
        user.month = _month
        user.month_recharge = -user.month_recharge
        user.month_proxy_recharge -= user.month_proxy_recharge
    user.month_recharge = money
    user.all_recharge = money


def recharge_statistic_proxy(proxy_id, money):
    if proxy_id > 0:
        proxy_user = UserManager().get_user(proxy_id)
        if proxy_user:
            recharge_statistic_proxy_online(proxy_user, money)
        else:
            recharge_statistic_proxy_offline(proxy_id, money)


def recharge_statistic_proxy_online(user, money):
    _month = func.month_now()
    if _month != user.month:
        user.month = _month
        user.month_recharge = -user.month_recharge
        user.month_proxy_recharge -= user.month_proxy_recharge
    user.month_proxy_recharge += money
    user.all_proxy_recharge += money
    recharge_statistic_proxy(user.proxy_id, money)


def recharge_statistic_proxy_offline(account_id, money):
    sql = 'select `proxy_id`, `month`, `month_recharge`, `all_recharge`, `month_proxy_recharge`, `all_proxy_recharge` from {} where account_id={}'.format(
        dbname.DB_ACCOUNT, account_id
    )
    result = dbexecute.query_one(sql)
    if not result:
        return
    proxy_id, month = result['proxy_id'], result['month']
    month_recharge, all_recharge = result['month_recharge'], result['all_recharge']
    month_proxy_recharge, all_proxy_recharge = result['month_proxy_recharge'], result['all_proxy_recharge']

    _month = func.month_now()
    if month != _month:
        month_recharge = 0
        month_proxy_recharge = 0
    month_proxy_recharge += money
    all_proxy_recharge += money
    dbexecute.update_record(
            table=dbname.DB_ACCOUNT,
            where={'account_id': account_id},
            data={
                'month': _month,
                'month_recharge': month_recharge,
                'all_recharge': all_recharge,
                'month_proxy_recharge': month_proxy_recharge,
                'all_proxy_recharge': all_proxy_recharge
            })
    recharge_statistic_proxy(proxy_id, money)


def calc_money_to_gold(money):
    ingot = recharges.recharges_information.get(money)
    if not ingot:
        ingot = money       # 1分钱1金币
    return ingot


def save_order_to_db(pay, ingot, recharge_origin):
    proxy_id, account_id = pay.attach
    insert_data = {
        'account_id': account_id,
        'proxy_id': proxy_id,
        'op_id': pay.order_id,
        'money': pay.money,
        'ingot': ingot,
        'origin': recharge_origin,
        'time': func.time_get()
    }
    _id = dbexecute.insert_auto_increment_record(**{
        'table': dbname.DB_RECHARGE,
        'data': insert_data
    })
    func.log_info('[gate] save_order_to_db _id: {}, account_id: {}, proxy_id: {}, money: {}, op_id: {}'.format(
        _id, account_id, proxy_id, pay.money, pay.order_id
    ))


def check_repeated_order_from_db(pay):
    order_id = pay.order_id
    sql = 'select id from {} where op_id={}'.format(dbname.DB_RECHARGE, order_id)
    if dbexecute.query_one(sql):
        func.log_error('[gate] check_repeated_order_from_db order_id: {} repeated'.format(order_id))
        return True
    else:
        return False

