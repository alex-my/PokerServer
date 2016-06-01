# coding:utf8
from app.util.common import func

MAH_OPERATOR_NONE = 0               # 不操作
MAH_OPERATOR_CHOW = 1               # 吃
MAH_OPERATOR_PONG = 2               # 碰
MAH_OPERATOR_KONG_LIGHT = 3         # 明杠
MAH_OPERATOR_KONG_DARK = 4          # 暗杠
MAH_OPERATOR_WIN = 5                # 胡
MAH_OPERATOR_DRAWN = 6              # 自摸


MAH_CONFIG = dict()     # {card: {pre_list: [], cur_list: [], next_list: []}, ...}


def _initialize_mahjong():

    def _gen_card(base):
        return [base + _card for _card in xrange(0, 4)]

    name_config = {1: 'Wang', 2: 'Tiao', 3: 'Tong'}
    begin = 1
    end = 108
    per_count = 36
    max_index = end / 4 - 1

    for index, i in enumerate(xrange(begin, end + 1, 4)):
        pre_list = _gen_card((index - 1) * 4 + 1) if index > 0 else []
        cur_list = _gen_card(index * 4 + 1)
        next_list = _gen_card((index + 1) * 4 + 1) if index < max_index else []
        card_index = index % 9 + 1
        card_type = i / per_count + 1
        name = '{}{}'.format(card_index, name_config.get(card_type, 'unknown'))
        for c in range(i, i + 4):
            MAH_CONFIG[c] = {
                'pre_list': pre_list,
                'cur_list': cur_list,
                'next_list': next_list,
                'name': name,
                'card_index': card_index,
                'card_type': card_type
            }
            func.log_info('[game] card: {} \t {}'.format(c, MAH_CONFIG[c]))

_initialize_mahjong()



