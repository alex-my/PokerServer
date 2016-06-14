# coding:utf8
from app.util.common import func


MAH_OPERATOR_NONE = 0               # 不操作
MAH_OPERATOR_CHOW = 1               # 吃
MAH_OPERATOR_PONG = 2               # 碰
MAH_OPERATOR_KONG_LIGHT = 3         # 明杠
MAH_OPERATOR_KONG_DARK = 4          # 暗杠
MAH_OPERATOR_WIN = 5                # 胡
MAH_OPERATOR_DRAWN = 6              # 自摸
MAH_OPERATOR_NO = 7                 # 平局


MAH_CONFIG = dict()     # {card: {pre_list: [], cur_list: [], next_list: []}, ...}
POKER_CONFIG = dict()   # {card: {cur_list: []}, ...}


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
            func.log_info('[game] mahjong: {} \t {}'.format(c, MAH_CONFIG[c]))


def _initialize_poker():

    for i in xrange(1):
        pass
    name_config = {1: 'HeiTao', 2: 'HongTao', 3: 'MeiHua', 4: 'FangKuai'}

    gen_card_id = 0
    for card_index in range(3, 13 + 1):
        for card_color in xrange(1, 4 + 1):
            card_id = gen_card_id + card_color
            POKER_CONFIG[card_id] = {
                'cur_list': range(gen_card_id + 1, gen_card_id + 4 + 1),
                'card_index': card_index,
                'name': '{}{}'.format(name_config[card_color], card_index),
                'card_color': card_color
            }
            # func.log_info('[game] poker: {} \t {}'.format(card_id, POKER_CONFIG[card_id]))
        gen_card_id += 4


_initialize_mahjong()
_initialize_poker()


test_mahjong_cards_list = [
    [1, 5, 9, 13, 17, 21, 25, 26, 37, 41, 45, 53, 57],
    [2, 6, 10, 14, 18, 22, 27, 28, 38, 42, 46, 61, 65],
    [3, 7, 11, 15, 19, 23, 29, 30, 39, 43, 47, 66, 69],
    [4, 8, 12, 16, 20, 24, 31, 32, 102, 103, 104, 92, 93]
]

test_mahjong_cards_flag = False


test_poker_16_cards_list = [
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
    [17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32],
    [33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48]
]

test_poker_16_cards_flag = True


