# coding:utf8
from app.gate.core.UserManager import UserManager
from app.gate.action import send
from app.util.common.config import Config, i
from app.util.common import func
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
    if contact:
        send.system_changes_string({changes.CHANGE_GAME_CONTACT: contact})


def _information_marquee():
    func.log_info('[gate] _information_marquee')
    content = i(informations.INFOMATION_TYPE_MARQUEE)
    if not content:
        return
    send.marquee_to_all(content)


def output_server_information():
    info = dict()
    user_count = UserManager().get_user_count()
    info['user_count'] = user_count
    func.log_info('[gate] online user_count: {}'.format(user_count))

    return str(info)
