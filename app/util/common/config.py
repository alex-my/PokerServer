# coding:utf8

from firefly.utils.singleton import Singleton
from app.util.common import func
from app.util.defines import dbname
from app.util.driver import dbexecute


class Config:

    __metaclass__ = Singleton

    def __init__(self):
        self._infomations = dict()

    def load_configs(self):
        self.load_from_infomation()

    def load_from_infomation(self):
        self._infomations = dict()
        sql = 'select * from {}'.format(dbname.DB_INFORMATION)
        results = dbexecute.query_all(sql)
        if not results:
            return

        for result in results:
            self._parse_infomation(result)

    def load_special_infomation(self, info_id):
        sql = 'select * from {} where id={}'.format(dbname.DB_INFORMATION, info_id)
        result = dbexecute.query_one(sql)
        if result:
            self._parse_infomation(result)
        else:
            func.log_error('[config] load_special_infomation unfind info_id: {} in db'.format(info_id))

    def _parse_infomation(self, result):
        try:
            self._infomations[result['id']] = result['content']
        except Exception as e:
            func.log_info('[config] _load_from_infomation failed, error: {}, result: {}'.format(
                    e.message, result
            ))

    def get_infomation(self, info_id, default):
        return self._infomations.get(info_id, default)


def i(info_id, default=None):
    return Config().get_infomation(info_id, default)




