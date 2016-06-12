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
        self._load_from_infomation()

    def _load_from_infomation(self):
        self._infomations = dict()
        sql = 'select * from {}'.format(dbname.DB_INFOMATION)
        results = dbexecute.query_all(sql)
        if not results:
            return

        for result in results:
            try:
                if result['content']:
                    result['content'] = func.unpack_data(result['content'])
                self._infomations[result['id']] = result['content']
            except Exception as e:
                func.log_info('[config] _load_from_infomation failed, error: {}, result: {}'.format(
                    e.message, result
                ))

    def get_infomation(self, info_id, default):
        return self._infomations.get(info_id, default)


def i(info_id, default=None):
    return Config().get_infomation(info_id, default)




