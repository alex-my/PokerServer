# coding:utf8
from app.util.common import func
from app.util.defines import dbname
from app.util.driver import dbexecute


def log_gold(account_id, count, remain, origin_id):
    t = func.time_get()
    insert_data = {
        'account_id': account_id,
        'count': count,
        'remain': remain,
        'origin_id': origin_id,
        'time': t
    }
    result = dbexecute.insert_record(**{'table': dbname.DB_LOG_GOLD, 'data': insert_data})
    if not result:
        func.log_error('[gate] log_gold account_id: {}, count: {}, remain: {}, origin_id: {}, time: {}'.format(
            account_id, count, remain, origin_id, t
        ))



