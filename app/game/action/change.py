# coding:utf8
from app.game.gameservice import request_gate_node


def award_gold(account_id, count, origin):
    if count < 0:
        return
    request_gate_node('game_award_gold', account_id, count, origin)


def spend_gold(account_id, count, origin):
    if count < 0:
        return
    request_gate_node('game_spend_gold', account_id, count, origin)

