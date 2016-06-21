# coding:utf8
from app.gate.core.UserManager import UserManager
from app.gate.action import send, change
from app.util.common.config import Config, i
from app.util.common import func
from app.util.defines import informations, changes, origins, dbname
from app.util.driver import dbexecute


def information_execute(info_id):
    # 重新载入信息配置
    Config().load_special_infomation(info_id)

    if info_id == informations.INFOMATION_TYPE_MARQUEE:
        _information_marquee()
    elif info_id == informations.INFOMATION_TYPE_CONTACT:
        _information_contact()
    else:
        raise KeyError('[gate] information_execute info_id: {} un exist'.format(info_id))


def _information_contact():
    contact = i(informations.INFOMATION_TYPE_CONTACT)
    if contact:
        send.system_changes_string({changes.CHANGE_GAME_CONTACT: contact})


def _information_marquee():
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


def gm_award_gold(account_id, gold_count):
    if account_id != 0:
        change.award_gold_by_account(account_id, gold_count, origins.ORIGIN_RECHARGE_GM)
        return 'account_id: {}, add gold: {} SUCCESS'.format(account_id, gold_count)
    else:
        try:
            gm_award_gold_all(gold_count)
            return 'add all user gold: {} SUCCESS'.format(gold_count)
        except Exception as e:
            func.log_error('[gate] gm_award_gold award all gold_count: {}, failed: {}'.format(
                gold_count, e.message
            ))
    return 'failed.'


def gm_award_gold_all(gold_count):
    sql = 'select `account_id` from {}'.format(dbname.DB_ACCOUNT)
    results = dbexecute.query_all(sql)
    if results:
        for result in results:
            account_id = result['account_id']
            change.award_gold_by_account(account_id, gold_count, origins.ORIGIN_RECHARGE_GM_ALL)
    else:
        func.log_info('[gate] gm_award_gold_all no account here.')


