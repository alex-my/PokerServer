# coding:utf8
from app.gate.core.UserManager import UserManager
from app.gate.action import log_record, send
from app.util.common import func
from app.util.defines import changes, dbname
from app.util.driver import dbexecute


def award_gold(user, count, origin):
    if count < 0:
        return
    user.award_gold(count)
    send.user_change(user.dynamic_id, {changes.CHANGE_USER_GOLD: user.gold})
    log_record.log_gold(user.account_id, count, user.gold, origin)
    func.log_info('[gate] award_gold account_id: {}, count: {}, now: {}, origin: {}'.format(
        user.account_id, count, user.gold, origin
    ))


def spend_gold(user, count, origin):
    if count < 0:
        return
    user.spend_gold(count)
    send.user_change(user.dynamic_id, {changes.CHANGE_USER_GOLD: user.gold})
    log_record.log_gold(user.account_id, count, user.gold, origin)
    func.log_info('[gate] spend_gold account_id: {}, count: {}, now: {}, origin: {}'.format(
        user.account_id, count, user.gold, origin
    ))


def award_gold_by_account(account_id, count, origin):
    if count < 0:
        return
    user = UserManager().get_user(account_id)
    if user:
        award_gold(user, count, origin)
    else:
        try:
            sql = 'update {} set gold = gold + {} where account_id = {}'.format(
                    dbname.DB_ACCOUNT, int(count), account_id)
            dbexecute.execute(sql)
            func.log_info('[gate] award_gold_by_account account_id: {}, add gold: {}, origin: {} offline'.format(
                account_id, count, origin
            ))
        except Exception as e:
            func.log_error('[gate] award_gold_by_account account_id: {}, count: {}, origin: {}, failed: {}'.format(
                account_id, count, origin, e.message
            ))


def spend_gold_by_account(account_id, count, origin):
    if count < 0:
        return
    user = UserManager().get_user(account_id)
    if user:
        spend_gold(user, count, origin)


def award_point(user, count, origin):
    if count < 0:
        return
    user.award_point(count)
    send.user_change(user.dynamic_id, {changes.CHANGE_USER_POINT: user.point})
    func.log_info('[gate] award_point account_id: {}, count: {}, now: {}, origin: {}'.format(
            user.account_id, count, user.gold, origin
    ))


def spend_point(user, count, origin):
    if count < 0:
        return
    user.spend_point(count)
    send.user_change(user.dynamic_id, {changes.CHANGE_USER_POINT: user.point})
    func.log_info('[gate] spend_point account_id: {}, count: {}, now: {}, origin: {}'.format(
            user.account_id, count, user.gold, origin
    ))

