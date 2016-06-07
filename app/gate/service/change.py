# coding:utf8
from firefly.server.globalobject import rootserviceHandle
from app.gate.action import change


@rootserviceHandle
def game_award_gold(account_id, count, origin):
    change.award_gold_by_account(account_id, count, origin)


@rootserviceHandle
def game_spend_gold(account_id, count, origin):
    change.spend_gold_by_account(account_id, count, origin)





