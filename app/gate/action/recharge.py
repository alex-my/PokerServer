# coding:utf8
from app.gate.core.UserManager import UserManager
from app.gate.action import send
from app.util.common import func, recharge_wechat
from app.util.defines import content


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


def get_wechat_prepay_info(dynamic_id, money, proxy_id):
    func.log_info('[gate] get_wechat_prepay_info money: {}, proxy_id: {}'.format(money, proxy_id))
    if money >= 10000000:     # 10W元
        send.system_notice(dynamic_id, content.RECHARGE_MONEY_TO_LARGE)
        return
    user = UserManager().get_user_by_dynamic(dynamic_id)
    if not user:
        send.system_notice(dynamic_id, content.ENTER_DYNAMIC_LOGIN_EXPIRE)
        return
    # Alex
    money = 1
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
    import xmltodict
    import json
    if not notice_content:
        return
    func.log_info('[gate] wechat_recharge_success content:\n {}'.format(notice_content))

    s = xmltodict.parse(notice_content)
    print 'Alex s: ', type(s)
    try:
        j0 = json.loads(s)
        print 'Alex j0: ', type(j0)
        print 'Alex j0: ', j0
    except Exception as e0:
        print 'Alex j0 error: ', e0.message
    try:
        j1 = json.dumps(s)
        print 'Alex j1: ', type(j1)
        print 'Alex j1: ', j1
    except Exception as e1:
        print 'Alex j1 error: ', e1.message

    # pay = recharge_wechat.WechatResponse(notice_content)
    # func.log_info('[gate] wechat_recharge_success pay.xml_json:\n {}'.format(pay.xml_json))


