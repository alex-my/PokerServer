# coding:utf8
from app.gate.core.UserManager import UserManager
from app.gate.action import send, change
from app.util.common import func, recharge_wechat
from app.util.defines import content, origins


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
    if not proxy_id:
        send.system_notice(dynamic_id, content.RECHARGE_PROXY_ID_NEED)
        return
    if not money or not isinstance(money, int):
        send.system_notice(dynamic_id, content.RECHARGE_MONEY_IS_NEED)
        return
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
    if not notice_content:
        return
    func.log_info('[gate] wechat_recharge_success content:\n {}'.format(notice_content))
    pay = recharge_wechat.WechatResponse(notice_content)
    func.log_info('[gate] wechat_recharge_success pay.xml_json:\n {}'.format(pay.xml_json))
    # TODO: check repeat notice from db
    xml_json = pay.xml_json
    attch = pay.attach
    if len(attch) != 2:
        func.log_error('[gate] wechat_recharge_success attach is unvalid: {}'.format(attch))
        return
    proxy_id, account_id = int(attch[0]), int(attch[1])
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

    money = pay.money
    if pay.verify():
        recharge_gold = calc_money_to_gold(money)
        change.award_gold(user, recharge_gold, origins.ORIGIN_RECHARGE_MONEY)
        # TODO: save information to db
        func.log_info('[gate] wechat_recharge_success account_id: {}, money: {} SUCCESS'.format(
            account_id, money
        ))
    else:
        func.log_info('[gate] wechat_recharge_success account_id: {}, money: {} FAILED'.format(
            account_id, money
        ))


def calc_money_to_gold(money):
    return int(money * 10)

