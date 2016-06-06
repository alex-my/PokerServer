# coding:utf8
from app.gate.action import log_record
from app.util.common import func


def award_gold(user, count, origin):
    if count < 0:
        return
    user.gold = count
    log_record.log_gold(user.account_id, count, origin)
    func.log_info('[gate] award_gold account_id: {}, count: {}, now: {}, origin: {}'.format(
        user.account_id, count, user.gold, origin
    ))


def spend_gold(user, count, origin):
    if count < 0:
        return
    user.spend_gold(count)
    log_record.log_gold(user.account_id, count, origin)
    func.log_info('[gate] spend_gold account_id: {}, count: {}, now: {}, origin: {}'.format(
        user.account_id, count, user.gold, origin
    ))

