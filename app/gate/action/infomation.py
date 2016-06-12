# coding:utf8
from app.util.common.config import Config
from app.util.defines import informations


def infomation_execute(info_id):
    # 重新载入信息配置
    Config().load_special_infomation(info_id)

    if info_id == informations.INFOMATION_TYPE_CONTACT:
        pass
    elif info_id == informations.INFOMATION_TYPE_MARQUEE:
        pass
    else:
        raise KeyError('[gate] infomation_execute info_id: {} un exist'.format(info_id))

