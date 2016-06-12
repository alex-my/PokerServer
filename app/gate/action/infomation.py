# coding:utf8
from app.gate.action import send
from app.util.common.config import Config, i
from app.util.defines import informations, changes


def information_execute(info_id):
    # 重新载入信息配置
    Config().load_special_infomation(info_id)

    if info_id == informations.INFOMATION_TYPE_CONTACT:
        _information_contact()
    elif info_id == informations.INFOMATION_TYPE_MARQUEE:
        _information_marquee()
    else:
        raise KeyError('[gate] information_execute info_id: {} un exist'.format(info_id))


def _information_contact():
    contact = i(informations.INFOMATION_TYPE_CONTACT)
    send.system_changes_string({changes.CHANGE_GAME_CONTACT: contact})


def _information_marquee():
    content = i(informations.INFOMATION_TYPE_MARQUEE)
    if not content:
        return
    send.marquee_to_all(content)
