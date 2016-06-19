# coding:utf8
from firefly.server.globalobject import rootserviceHandle
from app.gate.action import play


@rootserviceHandle
def game_add_play_history(account_id_list, history_data):
    play.add_play_history(account_id_list, history_data)
    return True

